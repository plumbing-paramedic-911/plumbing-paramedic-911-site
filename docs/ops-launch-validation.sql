-- Rollback-only integration test. Requires an existing active owner.
begin;

select set_config('request.jwt.claim.sub',(select id::text from public.crm_users where active and role='owner' limit 1),true);
set local role authenticated;
do $test$
declare l uuid; l2 uuid; result jsonb; repeated jsonb; inv uuid; total_value numeric; rejected boolean;
begin
  if not private.is_crm_staff() then raise exception 'Owner role check failed'; end if;
  insert into public.leads(caller_name,phone,issue_summary,source) values('Launch validation fixture','+12025550199','Fictional plumbing inspection','launch_validation') returning id into l;
  perform public.ops_acknowledge_lead(l);
  if not exists(select 1 from public.leads where id=l and acknowledged_at is not null and status='contacted') then raise exception 'Acknowledgment failed'; end if;
  result:=public.ops_book_lead(l,now()+interval '1 day',60,'100 Fictional Test Lane','Abbeville','29620',auth.uid(),'Fictional inspection');
  repeated:=public.ops_book_lead(l,now()+interval '1 day',60,'100 Fictional Test Lane','Abbeville','29620',auth.uid(),'Fictional inspection');
  if result->>'appointment_id' <> repeated->>'appointment_id' or repeated->>'existing' <> 'true' then raise exception 'Booking duplicate protection failed'; end if;
  insert into public.leads(caller_name,phone,issue_summary) values('Launch overlap fixture','+12025550198','Fictional inspection') returning id into l2;
  rejected:=false;
  begin
    perform public.ops_book_lead(l2,now()+interval '1 day 30 minutes',60,'101 Fictional Test Lane','Abbeville','29620',auth.uid(),'Fictional inspection');
  exception when others then
    if sqlerrm not like '%overlapping%' then raise; end if; rejected:=true;
  end;
  if not rejected then raise exception 'Overlap protection failed'; end if;
  perform public.ops_update_job((result->>'work_order_id')::uuid,'completed',auth.uid(),'Fictional diagnosis','Fictional repair');
  if not exists(select 1 from public.work_orders where id=(result->>'work_order_id')::uuid and status='completed' and completed_at is not null) then raise exception 'Job update failed'; end if;
  inv:=public.ops_draft_invoice((result->>'work_order_id')::uuid,'Fictional invoice',100,6,current_date+1);
  select total into total_value from public.invoices where id=inv;
  if total_value<>106 then raise exception 'Invoice calculation failed'; end if;
  if inv<>public.ops_draft_invoice((result->>'work_order_id')::uuid,'Fictional invoice',100,6,current_date+1) then raise exception 'Invoice duplicate protection failed'; end if;
end $test$;
reset role;
select set_config('request.jwt.claim.sub','00000000-0000-0000-0000-000000000001',true);
set local role authenticated;
do $test$
declare rejected boolean:=false;
begin
  begin perform public.ops_acknowledge_lead('00000000-0000-0000-0000-000000000001');
  exception when others then if sqlerrm<>'Staff access required' then raise; end if; rejected:=true; end;
  if not rejected then raise exception 'Nonstaff was allowed'; end if;
  if exists(select 1 from public.leads) then raise exception 'Nonstaff can see staff leads'; end if;
end $test$;
reset role;
select 'passed' as booking_invoice_staff_access_checks;
rollback;