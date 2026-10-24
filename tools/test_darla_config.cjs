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
  assert.match(script, /website-lead-capture/);
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
