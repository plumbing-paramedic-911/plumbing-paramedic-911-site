create table public.legacy_import_records (
 id uuid primary key,
 organization_id uuid not null references public.organizations(id),
 batch_key text not null,
 record_kind text not null check(record_kind in ('job','item','staff','accounting','setting')),
 source_key text not null,
 source_url text not null,
 source_as_of date,
 customer_id uuid references public.customers(id),
 review_required boolean not null default false,
 payload jsonb not null,
 imported_at timestamptz not null default now(),
 unique(organization_id,batch_key,record_kind,source_key)
);
alter table public.legacy_import_records enable row level security;
revoke all on public.legacy_import_records from public, anon, authenticated;
grant select on public.legacy_import_records to authenticated;
grant all on public.legacy_import_records to service_role;
create policy "CRM staff read legacy imports" on public.legacy_import_records for select to authenticated using ((select private.is_crm_staff()));
create index legacy_import_customer_idx on public.legacy_import_records(customer_id);
comment on table public.legacy_import_records is 'Historical source records for staff review; not live appointments, invoices, balances, or price-book entries.';
