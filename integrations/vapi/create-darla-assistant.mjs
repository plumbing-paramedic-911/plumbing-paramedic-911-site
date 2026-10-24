import { readFile } from "node:fs/promises";

const required = ["VAPI_API_KEY", "ON_CALL_TRANSFER_NUMBER"];
for (const name of required) {
  if (!process.env[name]) throw new Error(`Missing required environment variable: ${name}`);
}

const API_KEY = process.env.VAPI_API_KEY;
const ON_CALL = process.env.ON_CALL_TRANSFER_NUMBER;
const LEAD_ENDPOINT =
  process.env.PP911_LEAD_ENDPOINT ||
  "https://wuwgvtjktppjueiykcww.supabase.co/functions/v1/website-lead-capture";
const MODEL = process.env.VAPI_MODEL || "gpt-6-luna";

if (!/^\+\d{8,15}$/.test(ON_CALL)) {
  throw new Error("ON_CALL_TRANSFER_NUMBER must be E.164 format, e.g. +18645551234");
}
if (ON_CALL === "+18644468911") {
  throw new Error(
    "ON_CALL_TRANSFER_NUMBER must be a separate on-call destination, not the public 864-446-8911 number. Using the public number can create a forwarding loop."
  );
}

const promptUrl = new URL("./darla-system-prompt.md", import.meta.url);
const systemPrompt = await readFile(promptUrl, "utf8");

const captureLeadTool = {
  type: "apiRequest",
  name: "capture_plumbing_lead",
  description:
    "Save a confirmed Plumbing Paramedic 911 caller request. Use after collecting a callback number and enough issue detail to identify the service. For urgent calls, save before transfer when practical.",
  method: "POST",
  url: LEAD_ENDPOINT,
  timeoutSeconds: 10,
  body: {
    type: "object",
    properties: {
      name: {
        type: "string",
        description: "Caller's first and last name if provided. Do not invent a name."
      },
      phone: {
        type: "string",
        description: "Best callback number confirmed by the caller."
      },
      city: {
        type: "string",
        description: "Service city or service address if the caller provided it."
      },
      service: {
        type: "string",
        enum: [
          "Emergency Plumbing",
          "Well Pump",
          "Water Heater",
          "Drain / Sewer",
          "Leak / Water Line",
          "Fixture / Toilet",
          "Septic / Pump",
          "Commercial",
          "Other"
        ],
        description: "Best matching service category."
      },
      message: {
        type: "string",
        description:
          "Concise call summary including the plumbing problem, urgency, service location, safety facts, access notes, and preferred timing when known."
      }
    },
    required: ["phone", "service", "message"],
    additionalProperties: false
  },
  parameters: [
    { key: "email", value: "" },
    { key: "website", value: "" },
    { key: "source_page", value: "vapi://darla-inbound" },
    { key: "form_id", value: "darla_vapi_receptionist" }
  ]
};

const transferTool = {
  type: "transferCall",
  destinations: [
    {
      type: "number",
      number: ON_CALL,
      description:
        "Plumbing Paramedic 911 on-call plumber. Use only for a true urgent plumbing need or when the caller specifically asks for a person now, after the caller clearly agrees to be transferred.",
      message: "I’m connecting you with the on-call plumber now.",
      transferPlan: { mode: "blind-transfer" }
    }
  ]
};

const assistant = {
  name: "Darla - Plumbing Paramedic 911",
  firstMessage:
    "Thanks for calling Plumbing Paramedic 911. This is Darla, the automated receptionist. This call may be recorded for service quality. Are you dealing with an active plumbing emergency, or do you need routine service?",
  firstMessageInterruptionsEnabled: true,
  model: {
    provider: "openai",
    model: MODEL,
    reasoningEffort: "none",
    messages: [{ role: "system", content: systemPrompt }],
    tools: [captureLeadTool, transferTool, { type: "endCall" }]
  },
  voice: {
    provider: "vapi",
    voiceId: "Clara",
    version: 2,
    language: "en"
  },
  artifactPlan: {
    recordingEnabled: true,
    loggingEnabled: true,
    transcriptPlan: {
      enabled: true,
      assistantName: "Darla",
      userName: "Caller"
    }
  },
  endCallMessage:
    "Thanks for calling Plumbing Paramedic 911. We’ll be in touch. Goodbye."
};

const response = await fetch("https://api.vapi.ai/assistant", {
  method: "POST",
  headers: {
    Authorization: `Bearer ${API_KEY}`,
    "Content-Type": "application/json"
  },
  body: JSON.stringify(assistant)
});

if (!response.ok) {
  throw new Error(
    `Darla assistant creation failed (${response.status}): ${await response.text()}`
  );
}

const created = await response.json();
console.log(JSON.stringify({
  ok: true,
  assistantId: created.id,
  name: created.name,
  next: "Assign this assistant to a TEST Vapi/Twilio number first. Do not forward the public business number until emergency transfer and lead capture tests pass."
}, null, 2));
