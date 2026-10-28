const { test } = require("node:test");
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const vm = require("node:vm");
const { stripTypeScriptTypes } = require("node:module");

// Execute the real handler with an in-memory Supabase client; no live writes.
const source = fs.readFileSync(path.join(__dirname, "../supabase/functions/darla-lead-capture/index.ts"), "utf8");
const code = stripTypeScriptTypes(source.replace(/^import .*;\n/gm, ""));
const payload = { phone: "8645550100", service: "Leak / Water Line", message: "Kitchen pipe leaking", address: "1 Test Lane" };
const boundary = Date.parse("2026-10-26T10:10:00Z");

function harness() {
  let now = boundary - 1000, handler, failProcessing = false;
  const sessions = new Map(), intakes = [], processed = [];
  const sb = {
    from(table) {
      const filters = [];
      let operation = "select", value, newestFirst = false, limit = Infinity;
      const query = {
        select() { return query; },
        eq(key, expected) { filters.push(row => row[key] === expected); return query; },
        in(key, values) { filters.push(row => values.includes(row[key])); return query; },
        gte(key, minimum) { filters.push(row => row[key] >= minimum); return query; },
        order(key, options) { assert.equal(key, "created_at"); newestFirst = !options.ascending; return query; },
        limit(count) { limit = count; return query; },
        upsert(row) { operation = "upsert"; value = row; return query; },
        insert(row) { operation = "insert"; value = row; return query; },
        maybeSingle() { return query.single(); },
        async single() {
          if (table === "integration_credentials") return { data: { id: "credential" }, error: null };
          if (table === "organizations") return { data: { id: "org" }, error: null };
          if (table === "call_sessions" && operation === "upsert") {
            if (!sessions.has(value.external_call_id)) sessions.set(value.external_call_id, { ...value, id: `session-${sessions.size + 1}` });
            return { data: sessions.get(value.external_call_id), error: null };
          }
          assert.equal(table, "receptionist_intake");
          if (operation === "insert") {
            if (intakes.some(row => row.request_key === value.request_key)) return { data: null, error: { code: "23505" } };
            const row = { ...value, id: `intake-${intakes.length + 1}`, created_at: new Date(now).toISOString() };
            intakes.push(row);
            return { data: row, error: null };
          }
          let rows = intakes.filter(row => filters.every(filter => filter(row)));
          if (newestFirst) rows = rows.sort((a, b) => b.created_at.localeCompare(a.created_at));
          rows = rows.slice(0, limit);
          assert.ok(rows.length <= 1, "maybeSingle must receive at most one row");
          return { data: rows[0] || null, error: null };
        }
      };
      return query;
    },
    async rpc(name, args) {
      assert.equal(name, "process_receptionist_intake");
      processed.push(args.p_intake_id);
      return failProcessing ? { data: null, error: { code: "TEST_FAILURE" } } : { data: { lead_id: `lead-${args.p_intake_id}` }, error: null };
    }
  };
  vm.runInNewContext(code, {
    Deno: { serve(fn) { handler = fn; }, env: { get(name) { return { SUPABASE_SERVICE_ROLE_KEY: "test-only", SUPABASE_URL: "https://example.invalid" }[name]; } } },
    createClient: () => sb, crypto: globalThis.crypto, TextEncoder, Response,
    Date: class extends Date { static now() { return now; } }, console: { error() {} }
  });
  return {
    sessions, intakes, processed,
    setTime(value) { now = value; },
    failProcessing(value) { failProcessing = value; },
    async send(body = payload) {
      const response = await handler(new Request("https://example.invalid", {
        method: "POST", headers: { authorization: "Bearer test-only" }, body: JSON.stringify(body)
      }));
      return { status: response.status, body: await response.json() };
    }
  };
}

for (const failsFirst of [false, true]) {
  test(`retry across clock boundary reuses saved intake (${failsFirst ? "CRM 503" : "successful response"})`, async () => {
    const h = harness();
    h.failProcessing(failsFirst);
    const first = await h.send();
    assert.equal(first.status, failsFirst ? 503 : 200);
    h.setTime(boundary + 1000);
    h.failProcessing(false);
    const retry = await h.send();
    assert.equal(retry.status, 200);
    assert.equal(retry.body.request_id, first.body.request_id);
    assert.equal(h.intakes.length, 1);
    assert.equal(h.sessions.size, 1);
    assert.deepEqual(h.processed, [first.body.request_id, first.body.request_id]);
  });
}

test("formatted callback and whitespace normalize to the same recent request", async () => {
  const h = harness(), first = await h.send();
  h.setTime(boundary + 1000);
  const retry = await h.send({ ...payload, phone: "+1 (864) 555-0100", message: ` ${payload.message} ` });
  assert.equal(retry.body.request_id, first.body.request_id);
  assert.equal(h.intakes.length, 1);
});

test("an intake outside the rolling ten-minute window is a separate request", async () => {
  const h = harness();
  h.setTime(boundary - 599000);
  const first = await h.send();
  h.setTime(boundary + 2000);
  const later = await h.send();
  assert.equal(later.status, 200);
  assert.notEqual(later.body.request_id, first.body.request_id);
  assert.equal(h.intakes.length, 2);
});

test("retries keep the saved key throughout the rolling window", async () => {
  const h = harness(), first = await h.send();
  for (const offset of [1000, 300000, 598000]) {
    h.setTime(boundary + offset);
    const retry = await h.send();
    assert.equal(retry.status, 200);
    assert.equal(retry.body.request_id, first.body.request_id);
  }
  assert.equal(h.intakes.length, 1);
  assert.equal(h.sessions.size, 1);
});

test("different issue, address, and caller do not reuse the original intake", async () => {
  const h = harness();
  const first = await h.send();
  h.setTime(boundary + 1000);
  for (const change of [{ message: "Bathroom drain blocked" }, { address: "2 Test Lane" }, { phone: "8645550101" }]) {
    const next = await h.send({ ...payload, ...change });
    assert.equal(next.status, 200);
    assert.notEqual(next.body.request_id, first.body.request_id);
  }
  assert.equal(h.intakes.length, 4);
});
