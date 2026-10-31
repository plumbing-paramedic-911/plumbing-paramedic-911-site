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

// Exercise the real controller and price-book loader together; helper-only tests
// cannot catch a page that silently stops using either module.
function pricingWorkspace(rows,history=[]){
  const vm=require('node:vm'),fs=require('node:fs'),path=require('node:path');
  const nodes=new Map(),calls=[];
  const node=s=>{
    if(!nodes.has(s))nodes.set(s,{innerHTML:'',textContent:'',value:'',disabled:false,events:{},classList:{contains:()=>false,add(){},remove(){},toggle(){}},insertAdjacentHTML(){},addEventListener(k,fn){this.events[k]=fn;}});
    return nodes.get(s);
  };
  const document={querySelector:node,querySelectorAll:()=>[],body:node('body')};
  const window={PP911PriceBook:require('../ops/pricebook.js')};
  vm.runInNewContext(fs.readFileSync(path.join(__dirname,'../ops/workflows.js'),'utf8'),{window,document,setInterval(){},console});
  let fail=false;
  const sb={from(table){const query={select(){return this;},eq(k,v){assert.equal(k,'active');assert.equal(v,true);return this;},order(){return this;},async range(a,b){
    if(table==='price_book_items'){calls.push([a,b]);return fail?{error:{message:'Pricing offline'}}:{data:rows.filter(x=>x.active).slice(a,b+1)};}
    return {data:table==='legacy_import_records'?history.slice(a,b+1):[]};
  }};return query;}};
  return {workspace:window.PP911Operations.create(sb),node,calls,fail:v=>{fail=v;}};
}
test('workflow displays all active services, four rates, source pages and combined filters',async()=>{
  const rows=Array.from({length:1062},(_,i)=>({id:String(i),active:true,sku:`S-${i}`,category:i===1061?'Pumps':'Drains',service_name:i===1061?'Well <pump>':'Drain service',description:'Service details',standard_price:100,standard_ot_price:140,member_price:85,member_ot_price:119,source_page:42}));
  rows.push({...rows[0],active:false,sku:'INACTIVE'});
  const {workspace,node,calls}=pricingWorkspace(rows);
  await workspace.refresh();
  assert.deepEqual(calls,[[0,499],[500,999],[1000,1499]]);
  const host=node('#pricingTable');
  assert.match(host.innerHTML,/1,062 of 1,062 services/);
  assert.doesNotMatch(host.innerHTML,/INACTIVE/);
  for(const value of ['Standard OT','Member OT','$100.00','$140.00','$85.00','$119.00','Book page','42','Well &lt;pump&gt;'])assert.ok(host.innerHTML.includes(value),value);
  const events=node('#appView').events;
  events.input({target:{dataset:{search:'prices'},value:' S-1061 '}});
  assert.match(host.innerHTML,/1 of 1,062 services/);
  events.change({target:{dataset:{filter:'prices'},value:'Drains'}});
  assert.match(host.innerHTML,/0 of 1,062 services/);
  events.change({target:{dataset:{filter:'prices'},value:'Pumps'}});
  assert.match(host.innerHTML,/1 of 1,062 services/);
  await workspace.refresh();
  assert.equal(node('[data-filter="prices"]').value,'Pumps');
  assert.match(host.innerHTML,/1 of 1,062 services/);
});
test('imported history paginates, escapes source fields, and filters nested payloads',async()=>{
  const history=Array.from({length:575},(_,i)=>({id:String(i),record_kind:'job',customer_id:i===574?'c1':null,review_required:i!==574,source_url:'https://docs.google.com/spreadsheets/d/source/edit',payload:{'Customer name':i===574?'Cameron <McCoy>':'1979.0','Service address':i===574?'Horseshoe Rd':'','Description':'<script>unsafe</script>'}}));
  const {workspace,node}=pricingWorkspace([],history);await workspace.refresh();
  assert.match(node('#historyTable').innerHTML,/575 records/);
  assert.match(node('#historyTable').innerHTML,/Page 1 of 12/);
  assert.doesNotMatch(node('#historyTable').innerHTML,/<script>/);
  node('#historySearch').value='horseshoe';node('#historySearch').events.input();
  assert.match(node('#historyTable').innerHTML,/1 records/);
  assert.match(node('#historyTable').innerHTML,/Cameron &lt;McCoy&gt;/);
  node('#historyReview').checked=true;node('#historyReview').events.change();
  assert.match(node('#historyTable').innerHTML,/0 records/);
  assert.equal(ops.legacyRows(history,'','job',false,'c1').length,1);
});
test('pricing failures leave other workflows available and recover on refresh',async()=>{
  const {workspace,node,fail}=pricingWorkspace([{active:true,sku:'P-1',category:'Pumps',service_name:'Pump',standard_price:0,standard_ot_price:null,member_price:null,member_ot_price:null}]);
  fail(true);await workspace.refresh();
  assert.match(node('#pricingTable').innerHTML,/Pricing offline/);
  assert.match(node('#scheduleTable').innerHTML,/Book appointment/);
  assert.match(node('#invoicesTable').innerHTML,/Create a draft from a job/);
  fail(false);await workspace.refresh();
  assert.match(node('#pricingTable').innerHTML,/1 of 1 services/);
  assert.match(node('#pricingTable').innerHTML,/\$0\.00/);
  assert.doesNotMatch(node('#pricingTable').innerHTML,/Pricing offline/);
});

