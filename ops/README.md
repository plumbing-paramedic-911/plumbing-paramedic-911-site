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
