-- PP911 Operations workflow. Apply before deploying the matching UI.
-- All RPCs run as the caller and retain existing staff-only RLS checks.
begin;
alter table public.leads add column if not exists acknowledged_at timestamptz;
alter table public.leads add column if not exists acknowledged_by uuid references public.crm_users(id);
grant select on public.dispatch_tickets, public.invoices to authenticated;
grant insert on public.invoices to authenticated;
grant usage on sequence public.invoices_invoice_number_seq to authenticated;

create or replace function public.ops_acknowledge_lead(p_lead_id uuid)
returns void language plpgsql security invoker set search_path = '' as $$
begin
  if not private.is_crm_staff() then raise exception 'Staff access required'; end if;
  update public.leads set acknowledged_at=coalesce(acknowledged_at,now()),
    acknowledged_by=coalesce(acknowledged_by,auth.uid()),
    assigned_to=coalesce(assigned_to,auth.uid()),
    status=case when status='new' then 'contacted' else status end
  where id=p_lead_id and status not in ('lost','spam');
  if not found then raise exception 'Active lead not found'; end if;
end $$;

create or replace function public.ops_book_lead(
  p_lead_id uuid, p_start timestamptz, p_minutes integer,
  p_address text, p_city text, p_postal text, p_staff_id uuid, p_summary text
) returns jsonb language plpgsql security invoker set search_path = '' as $$
declare
  l public.leads%rowtype; c public.customers%rowtype; p public.properties%rowtype;
  a public.appointments%rowtype; j public.work_orders%rowtype; matches integer;
begin
  if not private.is_crm_staff() then raise exception 'Staff access required'; end if;
  select * into l from public.leads where id=p_lead_id for update;
  if not found or l.status in ('spam','lost') or l.caller_name ilike 'SYSTEM TEST%' then raise exception 'Choose an active, non-test lead'; end if;
  select * into a from public.appointments where lead_id=l.id and status<>'cancelled' order by created_at desc limit 1;
  if found then
    select * into j from public.work_orders where appointment_id=a.id order by created_at limit 1;
    return jsonb_build_object('appointment_id',a.id,'work_order_id',j.id,'existing',true);
  end if;
  if p_start is null or p_start<now()-interval '5 minutes' or p_start>now()+interval '2 years' then raise exception 'Choose a future appointment time'; end if;
  if p_minutes is null or p_minutes<15 or p_minutes>480 then raise exception 'Duration must be 15 to 480 minutes'; end if;
  if nullif(trim(p_address),'') is null or nullif(trim(p_city),'') is null or nullif(trim(p_summary),'') is null then raise exception 'Address, city and issue summary are required'; end if;
  if p_staff_id is not null then
    perform 1 from public.crm_users where id=p_staff_id and active for update;
    if not found then raise exception 'Choose an active staff member'; end if;
    if exists(select 1 from public.appointments where assigned_to=p_staff_id and status not in ('cancelled','no_show','completed') and scheduled_start<p_start+make_interval(mins=>p_minutes) and coalesce(scheduled_end,scheduled_start+interval '1 hour')>p_start) then raise exception 'This staff member already has an overlapping appointment'; end if;
  end if;
  if l.customer_id is not null then
    select * into c from public.customers where id=l.customer_id;
    if not found then raise exception 'Linked customer is unavailable'; end if;
  else
    perform pg_advisory_xact_lock(hashtextextended(right(regexp_replace(l.phone,'[^0-9]','','g'),10),0));
    select count(*) into matches from public.customers where right(regexp_replace(phone,'[^0-9]','','g'),10)=right(regexp_replace(l.phone,'[^0-9]','','g'),10);
    if matches>1 then raise exception 'Multiple customers match this phone. Link the correct customer before booking'; end if;
    if matches=1 then select * into c from public.customers where right(regexp_replace(phone,'[^0-9]','','g'),10)=right(regexp_replace(l.phone,'[^0-9]','','g'),10);
    else
      insert into public.customers(first_name,last_name,phone,email,source,organization_id)
      values(coalesce(nullif(trim(l.caller_name),''),'Unknown Caller'),'',l.phone,l.email,l.source,l.organization_id) returning * into c;
    end if;
  end if;
  if (trim(c.first_name||' '||c.last_name) ilike 'unknown%') and nullif(trim(l.caller_name),'') is not null and l.caller_name not ilike 'unknown%' then
    update public.customers set first_name=trim(l.caller_name),last_name='' where id=c.id;
  end if;
  select * into p from public.properties where customer_id=c.id and lower(trim(address_line1))=lower(trim(p_address)) and lower(trim(city))=lower(trim(p_city)) and state='SC' order by created_at limit 1;
  if not found then
    insert into public.properties(customer_id,address_line1,city,state,postal_code,organization_id)
    values(c.id,trim(p_address),trim(p_city),'SC',nullif(trim(p_postal),''),l.organization_id) returning * into p;
  end if;
  insert into public.appointments(customer_id,property_id,lead_id,assigned_to,scheduled_start,scheduled_end,problem_description,organization_id)
  values(c.id,p.id,l.id,p_staff_id,p_start,p_start+make_interval(mins=>p_minutes),trim(p_summary),l.organization_id) returning * into a;
  insert into public.work_orders(appointment_id,customer_id,property_id,technician_id,complaint,organization_id)
  values(a.id,c.id,p.id,p_staff_id,trim(p_summary),l.organization_id) returning * into j;
  update public.leads set customer_id=c.id,property_id=p.id,status='booked',assigned_to=p_staff_id where id=l.id;
  return jsonb_build_object('appointment_id',a.id,'work_order_id',j.id,'existing',false);
end $$;

create or replace function public.ops_job_from_appointment(p_appointment_id uuid)
returns uuid language plpgsql security invoker set search_path = '' as $$
declare a public.appointments%rowtype; job_id uuid;
begin
  if not private.is_crm_staff() then raise exception 'Staff access required'; end if;
  select * into a from public.appointments where id=p_appointment_id for update;
  if not found or a.status='cancelled' then raise exception 'Active appointment not found'; end if;
  select id into job_id from public.work_orders where appointment_id=a.id order by created_at limit 1;
  if job_id is null then
    insert into public.work_orders(appointment_id,customer_id,property_id,technician_id,complaint,organization_id)
    values(a.id,a.customer_id,a.property_id,a.assigned_to,a.problem_description,a.organization_id) returning id into job_id;
  end if;
  return job_id;
end $$;

create or replace function public.ops_draft_invoice(p_work_order_id uuid,p_title text,p_subtotal numeric,p_tax numeric,p_due date)
returns uuid language plpgsql security invoker set search_path = '' as $$
declare j public.work_orders%rowtype; invoice_id uuid;
begin
  if not private.is_crm_staff() then raise exception 'Staff access required'; end if;
  select * into j from public.work_orders where id=p_work_order_id for update;
  if not found or j.status='cancelled' then raise exception 'Active job not found'; end if;
  select id into invoice_id from public.invoices where work_order_id=j.id and status<>'void' order by created_at limit 1;
  if invoice_id is not null then return invoice_id; end if;
  if nullif(trim(p_title),'') is null or p_subtotal is null or p_tax is null or p_subtotal<0 or p_tax<0 or p_subtotal>1000000 or p_tax>1000000 then raise exception 'Enter a title and valid nonnegative amounts'; end if;
  insert into public.invoices(customer_id,property_id,appointment_id,work_order_id,title,subtotal,tax,total,due_date,organization_id)
  values(j.customer_id,j.property_id,j.appointment_id,j.id,trim(p_title),round(p_subtotal,2),round(p_tax,2),round(p_subtotal,2)+round(p_tax,2),p_due,j.organization_id) returning id into invoice_id;
  return invoice_id;
end $$;

create or replace function public.ops_update_job(p_job_id uuid,p_status text,p_staff_id uuid,p_diagnosis text,p_work text)
returns void language plpgsql security invoker set search_path = '' as $$
declare j public.work_orders%rowtype; a public.appointments%rowtype;
begin
  if not private.is_crm_staff() then raise exception 'Staff access required'; end if;
  select * into j from public.work_orders where id=p_job_id for update;
  if not found then raise exception 'Job not found'; end if;
  if p_staff_id is not null then
    perform 1 from public.crm_users where id=p_staff_id and active for update;
    if not found then raise exception 'Choose an active staff member'; end if;
  end if;
  if j.appointment_id is not null then
    select * into a from public.appointments where id=j.appointment_id for update;
    if p_staff_id is not null and a.status not in ('completed','cancelled','no_show') and exists(select 1 from public.appointments where id<>a.id and assigned_to=p_staff_id and status not in ('completed','cancelled','no_show') and scheduled_start<coalesce(a.scheduled_end,a.scheduled_start+interval '1 hour') and coalesce(scheduled_end,scheduled_start+interval '1 hour')>a.scheduled_start) then raise exception 'This staff member has an overlapping appointment'; end if;
    update public.appointments set assigned_to=p_staff_id where id=a.id;
  end if;
  update public.work_orders set status=p_status,technician_id=p_staff_id,diagnosis=p_diagnosis,work_performed=p_work,
    completed_at=case when p_status='completed' then coalesce(completed_at,now()) else null end where id=j.id;
end $$;
revoke all on function public.ops_update_job(uuid,text,uuid,text,text) from public, anon;
grant execute on function public.ops_update_job(uuid,text,uuid,text,text) to authenticated;

create or replace function public.ops_create_customer(p_first text,p_last text,p_phone text,p_email text,p_address text,p_city text,p_postal text)
returns uuid language plpgsql security invoker set search_path = '' as $$
declare customer_id uuid; phone_normal text;
begin
  if not private.is_crm_staff() then raise exception 'Staff access required'; end if;
  phone_normal=regexp_replace(p_phone,'[^0-9]','','g');
  if length(phone_normal)=11 and left(phone_normal,1)='1' then phone_normal=substr(phone_normal,2); end if;
  if nullif(trim(p_first),'') is null or length(phone_normal)<10 then raise exception 'Name and valid phone number are required'; end if;
  if (nullif(trim(p_address),'') is null) <> (nullif(trim(p_city),'') is null) then raise exception 'Enter both service address and city'; end if;
  perform pg_advisory_xact_lock(hashtextextended(phone_normal,0));
  if exists(select 1 from public.customers where right(regexp_replace(phone,'[^0-9]','','g'),10)=right(phone_normal,10)) then raise exception 'A customer with this phone already exists. Find and edit that customer instead'; end if;
  insert into public.customers(first_name,last_name,phone,email,source)
  values(trim(p_first),coalesce(trim(p_last),''),trim(p_phone),nullif(trim(p_email),''),'office_manual') returning id into customer_id;
  if nullif(trim(p_address),'') is not null then
    insert into public.properties(customer_id,address_line1,city,state,postal_code)
    values(customer_id,trim(p_address),trim(p_city),'SC',nullif(trim(p_postal),''));
  end if;
  return customer_id;
end $$;
revoke all on function public.ops_create_customer(text,text,text,text,text,text,text) from public, anon;
grant execute on function public.ops_create_customer(text,text,text,text,text,text,text) to authenticated;
revoke all on function public.ops_acknowledge_lead(uuid) from public, anon;
revoke all on function public.ops_book_lead(uuid,timestamptz,integer,text,text,text,uuid,text) from public, anon;
revoke all on function public.ops_job_from_appointment(uuid) from public, anon;
revoke all on function public.ops_draft_invoice(uuid,text,numeric,numeric,date) from public, anon;
grant execute on function public.ops_acknowledge_lead(uuid),public.ops_book_lead(uuid,timestamptz,integer,text,text,text,uuid,text),public.ops_job_from_appointment(uuid),public.ops_draft_invoice(uuid,text,numeric,numeric,date) to authenticated;
commit;
