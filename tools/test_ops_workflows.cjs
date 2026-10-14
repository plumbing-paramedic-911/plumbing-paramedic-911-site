const {test}=require('node:test');
const assert=require('node:assert/strict');
const ops=require('../ops/workflows.js');
test('urgent reminders exclude test, spam, lost, and booked leads',()=>{
  const lead={caller_name:'Customer',status:'new',urgency:'emergency',created_at:'2026-10-13T10:00:00Z'};
  assert.equal(ops.followup(lead,Date.parse('2026-10-13T10:14:59Z')),'Awaiting acknowledgment');
  assert.equal(ops.followup(lead,Date.parse('2026-10-13T10:15:00Z')),'Overdue acknowledgment');
  for(const status of ['spam','lost','booked'])assert.equal(ops.followup({...lead,status}),null);
  assert.equal(ops.followup({...lead,caller_name:'SYSTEM TEST — DO NOT DISPATCH'}),null);
  assert.equal(ops.followup({...lead,acknowledged_at:'2026-10-13T10:05:00Z'}),'Acknowledged');
});
test('active customers hide spam-only and test records but retain real customers',()=>{
  const customers=[{id:'a',active:true,first_name:'Real'},{id:'b',active:true,first_name:'Spam'},{id:'c',active:true,first_name:'SYSTEM TEST'},{id:'d',active:true,first_name:'Mixed'}];
  const leads=[{customer_id:'b',status:'spam'},{customer_id:'d',status:'spam'},{customer_id:'d',status:'booked'}];
  assert.deepEqual(ops.visibleCustomers(customers,leads).map(x=>x.id),['a','d']);
});
test('phone matching normalizes US country codes',()=>assert.equal(ops.phoneKey('+1 (864) 555-0123'),ops.phoneKey('8645550123')));
test('Eastern appointments are independent of device timezone and reject DST gaps/ambiguity',()=>{
  assert.equal(ops.easternISO('2026-10-14T09:00'),'2026-10-14T13:00:00.000Z');
  assert.equal(ops.easternISO('2026-12-14T09:00'),'2026-12-14T14:00:00.000Z');
  assert.equal(ops.easternISO('2027-03-14T02:30'),null);
  assert.equal(ops.easternISO('2026-11-01T01:30'),null);
  assert.equal(ops.easternISO('invalid'),null);
});
test('transcript summaries use caller excerpts and escape hostile text',()=>{
  assert.match(ops.excerpt({issue_summary:'AI: Hello, how can I help? User: My basement is flooding and I need help immediately. AI: We can help.'}),/^Caller excerpt: My basement/);
  assert.equal(ops.esc('<img onerror="x">'),'&lt;img onerror=&quot;x&quot;&gt;');
});
