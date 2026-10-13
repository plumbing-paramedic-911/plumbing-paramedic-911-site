const {test}=require('node:test');
const assert=require('node:assert/strict');
const fs=require('node:fs');
const vm=require('node:vm');
const path=require('node:path');
const crypto=require('node:crypto');
const root=path.join(__dirname,'..');
const source=fs.readFileSync(path.join(root,'ops/app.js'),'utf8');
const priceBook=require('../ops/pricebook.js');
test('price book loads all 1062 services rather than stopping at API limits',async()=>{
  const rows=Array.from({length:1062},(_,i)=>({sku:String(i)}));
  const calls=[];
  const query={select(){return this},eq(){return this},order(){return this},async range(start,end){calls.push([start,end]);return {data:rows.slice(start,end+1),error:null}}};
  const result=await priceBook.loadAll({from:name=>{assert.equal(name,'price_book_items');return query}});
  assert.deepEqual(result,rows);assert.deepEqual(calls,[[0,499],[500,999],[1000,1499]]);
});
test('price book searches codes and descriptions and combines category filters',()=>{
  const rows=[{sku:'01-01',service_name:'Clear Main Drain',category:'Drain Cleaning'},{sku:'25-01',service_name:'Well pump',category:'Well Pumps'}];
  assert.deepEqual(priceBook.filter(rows,'25-01',''),[rows[1]]);
  assert.deepEqual(priceBook.filter(rows,' MAIN ','Drain Cleaning'),[rows[0]]);
  assert.deepEqual(priceBook.filter(rows,'pump','Drain Cleaning'),[]);
});
function setup(client,missing=false){
  const nodes=new Map();
  function node(id){
    if(!nodes.has(id)){
      const classes=new Set(['hidden']);
      nodes.set(id,{value:'',textContent:'',disabled:true,events:{},classList:{add:(...xs)=>xs.forEach(x=>classes.add(x)),remove:(...xs)=>xs.forEach(x=>classes.delete(x)),contains:x=>classes.has(x)},addEventListener(event,fn){this.events[event]=fn},reportValidity:()=>true});
    }
    return nodes.get(id);
  }
  const buttons=[node('signin'),node('#signupBtn')];
  const document={querySelector:node,querySelectorAll:s=>s.includes('button')&&s.includes('authForm')?buttons:[]};
  const sb={auth:{getSession:async()=>({data:{session:null}}),onAuthStateChange:()=>{},...client?.auth},...client};
  vm.runInNewContext(source,{window:missing?{}:{supabase:{createClient:()=>sb}},document,navigator:{},location:{origin:'https://plumbingparamedic911.com'},console,setTimeout});
  return {node,buttons};
}
const settled=()=>new Promise(resolve=>setImmediate(resolve));
test('missing library shows a useful error and leaves auth disabled',()=>{
  const {node,buttons}=setup(null,true);
  assert.match(node('#authMsg').textContent,/could not load/);
  assert.ok(buttons.every(b=>b.disabled));
});
test('empty signup responds without contacting Auth',async()=>{
  const {node}=setup();
  node('#signupBtn').events.click();await settled();
  assert.match(node('#authMsg').textContent,/at least 8 characters/);
});
test('network failure is visible, duplicate submissions suppressed, retry enabled',async()=>{
  let rejectRequest,calls=0;
  const {node,buttons}=setup({auth:{getSession:async()=>({data:{session:null}}),onAuthStateChange:()=>{},signUp:()=>{calls++;return new Promise((_,reject)=>rejectRequest=reject)}}});
  node('#email').value='test@example.com';node('#password').value='test-only-password';
  node('#signupBtn').events.click();node('#signupBtn').events.click();
  assert.equal(calls,1);assert.ok(buttons.every(b=>b.disabled));
  rejectRequest(new Error('Failed to fetch'));await settled();
  assert.equal(node('#authMsg').textContent,'Failed to fetch');assert.ok(buttons.every(b=>!b.disabled));
});
test('confirmation-required signup explains the next step',async()=>{
  const {node}=setup({auth:{getSession:async()=>({data:{session:null}}),onAuthStateChange:()=>{},signUp:async options=>{assert.equal(options.options.emailRedirectTo,'https://plumbingparamedic911.com/ops/');return {data:{session:null},error:null}}}});
  node('#email').value='test@example.com';node('#password').value='test-only-password';
  node('#signupBtn').events.click();await settled();
  assert.match(node('#authMsg').textContent,/Check your email/);
});
test('pinned browser library matches its recorded checksum and CSP',()=>{
  const lock=JSON.parse(fs.readFileSync(path.join(root,'ops/vendor/supabase-lock.json')));
  const bytes=fs.readFileSync(path.join(root,'ops/vendor',lock.file));
  assert.equal(crypto.createHash('sha256').update(bytes).digest('hex'),lock.sha256);
  const html=fs.readFileSync(path.join(root,'ops/index.html'),'utf8');
  const scripts=[...html.matchAll(/<script[^>]+src="([^"]+)"/g)].map(m=>m[1]);
  assert.ok(scripts.every(src=>src.startsWith('/ops/')));
  assert.ok(scripts[0].endsWith(lock.file));
  for(const src of scripts)assert.ok(fs.existsSync(path.join(root,src.split('?')[0])));
});
