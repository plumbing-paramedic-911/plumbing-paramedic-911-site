# Recovered business data

The authenticated operations hub reads historical source records from `legacy_import_records`. These records are separate from live work orders, appointments, invoices, and priced catalog entries. Staff can search Imported history, filter by type or review status, inspect original fields, and open a source file. Customer rows link to their associated job history.

The October 31, 2026 import added 123 source customer names without invented phone numbers, emails, person/company classifications, or name splitting. Empty phone numbers do not constitute duplicate matches. Historic display names occupy `first_name`, with `last_name` left empty until reviewed. Existing customer records were preserved.

The archive contains 575 jobs from the June 30, 2025 export, 206 cleanup item entries, 4 historical staff configurations, 50 accounting entities, and 27 company settings. Of the jobs, 156 link to named customer records; 419 have numeric customer names and remain unlinked. Review flags also identify missing job addresses. Source amounts lack an explicit currency code and are rendered as original text, without totals or current-debt claims. No active work orders or invoices were generated.

The table is RLS protected and readable only by the existing CRM staff authorization function. Signed-out users have no table grant. Browser clients cannot write archive records. It follows the existing single-organization staff access model. Source data is stored only in the private database, never in repository files or public website assets.

Import IDs derive from a fixed namespace and source keys; re-running the same batch inserts no duplicate rows. The archive key is `drive-recovery-20261031-v1`. Before any later imports, check for existing customers using verified contact/address identifiers; do not merge different people solely on a similar name. Backups and source CSVs remain separately available.

Schema is recorded in `docs/legacy-import.sql`, applied using Supabase migration `legacy_import_archive`. UI rollback is a code revert; it does not remove source data. The deployed database import was verified with counts, linked/unlinked totals, an authenticated owner read, a nonstaff read denial, and anonymous grant checks.
