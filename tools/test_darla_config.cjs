const { test } = require("node:test");
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");

const root = path.resolve(__dirname, "..");
const prompt = fs.readFileSync(path.join(root, "integrations/vapi/darla-system-prompt.md"), "utf8");
const script = fs.readFileSync(path.join(root, "integrations/vapi/create-darla-assistant.mjs"), "utf8");

test("Darla carries the current PP911 service-call policy", () => {
  assert.match(prompt, /\$79[^\n]*Monday through Friday[^\n]*9:00 AM.?5:00 PM/i);
  assert.match(prompt, /\$99[^\n]*after-hours and weekends/i);
  assert.match(prompt, /\$158[^\n]*after midnight/i);
  assert.match(prompt, /\$158[^\n]*holiday/i);
});

test("Darla keeps the service call outside percentage discounts", () => {
  assert.match(prompt, /10% off eligible repair\/install work/i);
  assert.match(prompt, /does \*\*not\*\* reduce the \$79 \/ \$99 \/ \$158 service-call charge/i);
  assert.match(prompt, /discounts do not stack/i);
});

test("Darla does not restore retired pricing language", () => {
  const lower = prompt.toLowerCase();
  for (const stale of [
    "$150 after-hours surcharge",
    "service call fee is waived",
    "free diagnostic",
    "free on-site estimates"
  ]) {
    assert.ok(!lower.includes(stale), `Darla prompt must not contain retired wording: ${stale}`);
  }
});

test("Darla never routes the forwarded public line back into itself", () => {
  assert.match(script, /ON_CALL_TRANSFER_NUMBER/);
  assert.match(script, /ON_CALL === "\+18644468911"/);
  assert.match(script, /create a forwarding loop/i);
  assert.match(prompt, /must never point back to the public business number/i);
});


test("Darla uses recoverable assistant-based warm transfer", () => {
  assert.match(script, /mode: "warm-transfer-experimental"/);
  assert.doesNotMatch(script, /mode: "blind-transfer"/);
  assert.match(script, /transferAssistant/);
  assert.match(script, /transferSuccessful/);
  assert.match(script, /transferCancel/);
  assert.match(script, /fallbackPlan/);
  assert.match(script, /endCallEnabled: false/);
  assert.match(script, /voicemail|IVR/i);
});

test("Darla captures leads before emergency transfer when practical", () => {
  assert.match(script, /type: "apiRequest"/);
  assert.match(script, /name: "capture_plumbing_lead"/);
  assert.match(script, /darla-lead-capture/);
  assert.match(script, /type: "transferCall"/);
  assert.match(prompt, /save the lead \*\*before transfer when practical\*\*/i);
});

test("Darla uses the current Vapi model and a female Vapi voice", () => {
  assert.match(script, /"gpt-6-luna"/);
  assert.match(script, /voiceId: "Clara"/);
  assert.match(script, /version: 2/);
});

test("Darla discloses automation and recording", () => {
  assert.match(script, /automated receptionist/i);
  assert.match(script, /call may be recorded/i);
  assert.match(script, /recordingEnabled: true/);
  assert.match(script, /transcriptPlan/);
});

const { pathToFileURL } = require("node:url");

async function runProvision(overrides = {}) {
  const env = {
    VAPI_API_KEY: "test-private-key",
    ON_CALL_TRANSFER_NUMBER: "+18649408453",
    VAPI_INTAKE_CREDENTIAL_ID: "11111111-2222-4333-8444-555555555555",
    ...overrides
  };
  const requests = [];
  const logs = [];
  const run = new (Object.getPrototypeOf(async function () {}).constructor)(
    "process", "fetch", "console", "readFile", "moduleUrl",
    script.replace('import { readFile } from "node:fs/promises";', "").replaceAll("import.meta.url", "moduleUrl")
  );
  await run({ env }, async (url, options) => {
    requests.push({ url, options, body: JSON.parse(options.body) });
    return { ok: true, json: async () => ({ id: "test-assistant", name: "Darla" }) };
  }, { log: value => logs.push(value) }, async () => prompt,
  pathToFileURL(path.join(root, "integrations/vapi/create-darla-assistant.mjs")).href);
  return { requests, logs };
}

test("provisioned intake authenticates with a stored credential on the dedicated endpoint", async () => {
  const { requests, logs } = await runProvision();
  assert.equal(requests.length, 1);
  const tool = requests[0].body.model.tools.find(tool => tool.name === "capture_plumbing_lead");
  assert.equal(tool.url, "https://wuwgvtjktppjueiykcww.supabase.co/functions/v1/darla-lead-capture");
  assert.equal(tool.credentialId, "11111111-2222-4333-8444-555555555555");
  assert.equal(tool.method, "POST");
  assert.equal(tool.body.additionalProperties, false);
  assert.ok(tool.body.properties.address);
  assert.ok(!JSON.stringify(tool).includes("test-private-key"));
  assert.ok(!JSON.stringify(logs).includes("test-private-key"));
  assert.equal(tool.headers?.Authorization, undefined);
});

test("provisioning rejects missing intake authentication and untrusted endpoints before network access", async () => {
  await assert.rejects(runProvision({ VAPI_INTAKE_CREDENTIAL_ID: "" }), /Missing required environment variable/);
  await assert.rejects(runProvision({ VAPI_INTAKE_CREDENTIAL_ID: "invalid" }), /existing Vapi Custom Credential/);
  await assert.rejects(runProvision({ PP911_LEAD_ENDPOINT: "https://example.com/collect" }), /authenticated PP911 Darla endpoint/);
  await assert.rejects(runProvision({ ON_CALL_TRANSFER_NUMBER: "+18644468911" }), /forwarding loop/);
});

test("manual workflow uses the dedicated intake endpoint and requires its credential", () => {
  const workflow = fs.readFileSync(path.join(root, ".github/workflows/provision-darla.yml"), "utf8");
  assert.match(workflow, /functions\/v1\/darla-lead-capture/);
  assert.doesNotMatch(workflow, /website-lead-capture/);
  assert.equal((workflow.match(/VAPI_INTAKE_CREDENTIAL_ID: \$\{\{ secrets\.VAPI_INTAKE_CREDENTIAL_ID \}\}/g) || []).length, 2);
});
