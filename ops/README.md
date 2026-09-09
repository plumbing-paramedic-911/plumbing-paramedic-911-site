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