# PP911 Operations

Private, installable owner dashboard for Plumbing Paramedic 911.

## Current modules
- Dashboard
- Leads
- Customers
- Schedule
- Work orders
- Emergency dispatch
- Darla/Vapi call history
- Flat-rate price book
- Estimates and field calculators
- Invoices

## Backend
Supabase project `wuwgvtjktppjueiykcww` is the system of record. Public website forms, AI receptionist workflows, dispatch, and the operations app are intended to converge on the canonical field-service tables: `customers`, `properties`, `leads`, `appointments`, `work_orders`, `estimates`, `invoices`, plus dispatch/call tables.

## Security
The app uses Supabase Auth and RLS. The publishable browser key is intentionally public; privileged database credentials are never shipped to the browser. Initial owner activation is protected by a one-time server-side setup code. Future staff accounts remain inactive until approved by an owner/admin.

## Install
Open `/ops/` in a supported mobile browser and use **Add to Home screen** / **Install app**. The PWA shell is cached, while live CRM data still requires a network connection.

## Browser dependency and validation

Supabase JS 2.117.3 is served from `ops/vendor/`, because the production CSP permits same-origin scripts and blocks third-party CDNs. `vendor/supabase-lock.json` records the official npm tarball, its verified SHA-512 integrity, and the browser file SHA-256. The upstream MIT license is included. Updates must pin a version, verify npm integrity, update the HTML/service-worker paths, and rerun validation.

Run `node --test tools/test_ops.cjs` plus the repository release checks. Browser verification should use the production CSP and confirm that empty signup shows validation feedback without creating an account. Owner signup and setup-code entry must be completed by the owner; do not put their credentials in logs or test fixtures.

## Operations workflow release

Apply `docs/ops-workflow.sql` to the production database **before** merging/deploying the workflow UI. The SQL has not been applied merely by adding it to this repository. It adds lead acknowledgment fields and six `SECURITY INVOKER` RPCs. They explicitly require CRM staff and retain existing RLS. Anonymous callers cannot execute them. Invoice INSERT and identity-sequence USAGE are granted to authenticated callers subject to the existing staff-only invoice policy. No DELETE permission is added.

The Dashboard shows urgent and emergency leads awaiting acknowledgment. On-screen reminders become overdue at 15 minutes for emergencies and 60 minutes for urgent requests. These are review thresholds, not promised service arrival times. The tab refreshes once per minute while visible and no form is open. This release does not send SMS/email alerts, notify technicians, or auto-dispatch historical leads.

Booking an active lead atomically links/reuses its customer and property, creates an appointment and job, and marks the lead booked. Repeated submissions return the existing booking. Assigned staff overlap is checked during booking. Eastern-time conversion rejects ambiguous or nonexistent daylight-saving times. Booking safely replaces an `Unknown Caller` customer name when the linked lead supplies a known name. Existing named customers are preserved.

Jobs support technician, status, diagnosis and work notes. Technician changes also update the linked appointment and check for scheduling conflicts. Appointment statuses remain separately editable. Draft invoices are created from jobs with validated subtotal and tax; repeats return the existing non-void invoice. This release does not send invoices or collect payments.

Search is available on Leads, Customers, and Price Book. Active lists exclude test records and spam-only customers without deleting them; All records restores visibility. The customer editor flags possible phone duplicates. Data is paged rather than silently truncated at 50/100 records; a section reports an error above the 20,000-record safety limit. A failed query leaves other sections usable and provides a retry button.

## Estimates and field calculators

The Estimates tab builds a customer-ready estimate and prints it. It writes nothing to the database: the estimate lives in the page until it is printed, so a mis-typed line cannot reach a customer record, and the `estimates` table keeps its current meaning until line-item storage is designed for it.

Lines come from three places: the production price book (searched from `price_book_items`, loaded the first time the tab is opened), the field calculators, or a custom line.

Pricing basis is automatic. Book lines price from the book's own `standard_price`, `member_price`, `standard_ot_price` and `member_ot_price` columns. Custom and calculator lines fall back to the published VIP Diamond Plan rate of 15% and the book's 1.40x after-hours factor. The service/diagnostic call is a flat $79 / $99 / $158 fee by time of day and is never discounted or upcharged, because the time is already priced into the fee. The printed arithmetic reconciles on paper: standard subtotal plus the after-hours adjustment minus plan savings equals what is charged. A manual discount is capped at the work and spread across the taxable share, so tax is never charged on money the customer does not pay.

Calculators cover pipe runs (material and labor by material, size, length and working conditions), trenching (depth, surface cut and restoration), whole-home repipes (fixtures, stories, material) and water heater sizing (peak-hour demand). Their figures are starting points for the estimate, not published prices.

Printing uses the browser's own print dialog rather than a PDF library: no dependency, works offline, and on a phone it is Share -> Print -> Save to Files with selectable text. The sheet is `display:none` on screen and is the only visible element in print media.

Estimate validation: `node --test tools/test_estimator.cjs` covers the pricing basis, the reconciliation, the discount cap, each calculator, and HTML escaping of customer-supplied text.

Validation: `node --test tools/test_ops.cjs tools/test_ops_workflows.cjs tools/test_estimator.cjs`, production release build, internal links, redirects, desktop/mobile browser preview with fictional records, booking/job/invoice flow, and a simulated failed invoice query. Before live deployment also run a rollback-only database integration test under an authenticated staff role and a denied nonstaff role.
