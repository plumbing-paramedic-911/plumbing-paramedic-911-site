(() => {
const startupMessage=document.querySelector('#authMsg');
if(typeof window.supabase?.createClient!=='function'){
  startupMessage.textContent='Sign-in could not load. Check your connection and refresh the page.';
  startupMessage.classList.add('error');
  return;
}
try {
const SUPABASE_URL='https://wuwgvtjktppjueiykcww.supabase.co';
const SUPABASE_KEY='sb_publishable_GDRVKaxxwvFuV7jhldebYA_6GjUszub';
const sb=window.supabase.createClient(SUPABASE_URL,SUPABASE_KEY,{auth:{persistSession:true,autoRefreshToken:true,detectSessionInUrl:true}});

const $=s=>document.querySelector(s), $$=s=>[...document.querySelectorAll(s)];
const fmtDate=v=>v?new Date(v).toLocaleString([], {month:'short',day:'numeric',hour:'numeric',minute:'2-digit'}):'—';
const esc=v=>String(v??'').replace(/[&<>'"]/g,m=>({'&':'&amp;','<':'&lt;','>':'&gt;',"'":'&#39;','"':'&quot;'}[m]));
function msg(text,error=false){const el=$('#authMsg');el.textContent=text;el.classList.remove('hidden','error');if(error)el.classList.add('error')}
function empty(text='Nothing here yet.'){return `<div class="empty">${esc(text)}</div>`}
function pill(v){return `<span class="pill ${esc(v)}">${esc(v||'—')}</span>`}
function table(headers,rows){if(!rows.length)return empty();return `<div class="table-wrap"><table class="data-table"><thead><tr>${headers.map(h=>`<th>${esc(h)}</th>`).join('')}</tr></thead><tbody>${rows.join('')}</tbody></table></div>`}

async function profile(){const {data:{user}}=await sb.auth.getUser();if(!user)return null;const {data,error}=await sb.from('crm_users').select('*').eq('id',user.id).maybeSingle();if(error)throw error;return data}
async function boot(){const {data:{session}}=await sb.auth.getSession();if(!session){showAuth();return}try{const p=await profile();if(!p||!p.active){showAuth();$('#claimForm').classList.remove('hidden');msg('Your login exists. Enter the owner setup code to activate PP911 Operations.');return}showApp();await refreshAll()}catch(e){console.error(e);showAuth();msg(e.message||'Could not load account',true)}}
function showAuth(){$('#authView').classList.remove('hidden');$('#appView').classList.add('hidden')}
function showApp(){$('#authView').classList.add('hidden');$('#appView').classList.remove('hidden')}

let authBusy=false;
async function authAction(action){
  if(authBusy)return;
  authBusy=true;
  const buttons=$$('#authForm button, #claimForm button');
  buttons.forEach(b=>b.disabled=true);
  try{await action()}catch(e){msg(e.message||'Could not connect. Check your connection and try again.',true)}
  finally{authBusy=false;buttons.forEach(b=>b.disabled=false)}
}
$('#authForm').addEventListener('submit',e=>{e.preventDefault();authAction(async()=>{msg('Signing in…');const email=$('#email').value.trim(),password=$('#password').value;const {error}=await sb.auth.signInWithPassword({email,password});if(error)throw error;await boot()})});
$('#signupBtn').addEventListener('click',()=>{authAction(async()=>{const email=$('#email').value.trim(),password=$('#password').value,full_name=$('#fullName').value.trim()||'Owner';if(!email||password.length<8)return msg('Enter your email and a password of at least 8 characters.',true);if(!$('#authForm').reportValidity())return;msg('Creating your login…');const {data,error}=await sb.auth.signUp({email,password,options:{emailRedirectTo:location.origin+'/ops/',data:{full_name}}});if(error)throw error;if(!data.session)return msg('Login created. Check your email for the confirmation link, then come back and sign in.');$('#claimForm').classList.remove('hidden');msg('Login created. Enter the owner setup code below.')})});
$('#claimForm').addEventListener('submit',e=>{e.preventDefault();authAction(async()=>{msg('Activating owner access…');const code=$('#claimCode').value.trim();const {error}=await sb.rpc('claim_ops_owner',{p_code:code});if(error)throw error;$('#claimCode').value='';$('#claimForm').classList.add('hidden');msg('Owner access activated. Loading PP911 Operations…');await boot()})});
$('#signOutBtn').addEventListener('click',async()=>{await sb.auth.signOut();location.reload()});
$('#refreshBtn').addEventListener('click',refreshAll);

$$('#tabs button').forEach(b=>b.addEventListener('click',()=>{$$('#tabs button').forEach(x=>x.classList.remove('active'));b.classList.add('active');$$('.view').forEach(v=>v.classList.remove('active'));$('#'+b.dataset.view).classList.add('active')}));
$$('[data-modal]').forEach(b=>b.addEventListener('click',()=>document.getElementById(b.dataset.modal).showModal()));

async function q(tableName,select='*',opts={}){let r=sb.from(tableName).select(select);if(opts.order)r=r.order(opts.order,{ascending:opts.asc??false});if(opts.limit)r=r.limit(opts.limit);const {data,error}=await r;if(error)throw error;return data||[]}
async function count(tableName){const {count,error}=await sb.from(tableName).select('*',{count:'exact',head:true});if(error)throw error;return count||0}

let refreshInProgress=false;
async function refreshAll(){
 if(refreshInProgress)return;
 refreshInProgress=true;
 const button=$('#refreshBtn');if(button)button.disabled=true;
 const tasks=[
 ['leadCount',()=>count('leads')],['customerCount',()=>count('customers')],['jobCount',()=>count('work_orders')],['dispatchCount',()=>count('dispatch_tickets')],
 ['leads',()=>q('leads','*',{order:'created_at',limit:50})],['calls',()=>q('call_sessions','*',{order:'created_at',limit:50})],
 ['customers',()=>q('customers','*',{order:'created_at',limit:100})],['appointments',()=>q('appointments','*',{order:'scheduled_start',asc:true,limit:100})],
 ['jobs',()=>q('work_orders','*',{order:'created_at',limit:100})],['dispatch',()=>q('dispatch_tickets','*',{order:'created_at',limit:100})],
 ['prices',()=>q('price_book_items','*',{order:'category',asc:true,limit:500})],['invoices',()=>q('invoices','*',{order:'created_at',limit:100})]
 ];
 try{
  const results=await Promise.allSettled(tasks.map(([,run])=>run()));
  const values={},failures=[];
  results.forEach((r,i)=>{const name=tasks[i][0];if(r.status==='fulfilled')values[name]=r.value;else{failures.push(name);console.error('Refresh failed: '+name,r.reason)}});
  const renderers={leads:renderLeads,calls:renderCalls,customers:renderCustomers,appointments:renderSchedule,jobs:renderJobs,dispatch:renderDispatch,prices:renderPricing,invoices:renderInvoices};
  Object.entries(renderers).forEach(([name,render])=>{if(name in values){try{render(values[name])}catch(e){failures.push(name+' display');console.error('Render failed: '+name,e)}}});
  if(['leadCount','customerCount','jobCount','dispatchCount'].every(k=>k in values))renderStats(values);
  if(failures.length)msg('Some sections could not refresh: '+failures.join(', ')+'. Other sections remain available. Try again.',true);
  else{const notice=$('#authMsg');if(notice){notice.classList.add('hidden');notice.classList.remove('error')}}
 }finally{refreshInProgress=false;if(button)button.disabled=false}
}

function renderStats(s){$('#stats').innerHTML=[['Leads',s.leadCount],['Customers',s.customerCount],['Open jobs',s.jobCount],['Dispatch tickets',s.dispatchCount]].map(([l,n])=>`<div class="stat"><div class="num">${n}</div><div class="label">${l}</div></div>`).join('')}
function renderLeads(data){$('#dashboardLeads').innerHTML=data.slice(0,6).length?`<div class="mini-list">${data.slice(0,6).map(x=>`<div class="mini-item"><div class="mini-title">${esc(x.caller_name||x.phone)}</div><div>${esc(x.issue_summary)}</div><div class="mini-meta">${pill(x.urgency)} · ${fmtDate(x.created_at)}</div></div>`).join('')}</div>`:empty('No leads yet.');$('#leadsTable').innerHTML=table(['Customer','Phone','Issue','Urgency','Status','Created'],data.map(x=>`<tr><td>${esc(x.caller_name||'—')}</td><td>${esc(x.phone)}</td><td>${esc(x.issue_summary)}</td><td>${pill(x.urgency)}</td><td><select class="status-select lead-status" data-id="${x.id}">${['new','contacted','qualified','booked','lost','spam'].map(v=>`<option ${x.status===v?'selected':''}>${v}</option>`).join('')}</select></td><td>${fmtDate(x.created_at)}</td></tr>`));$$('.lead-status').forEach(s=>s.addEventListener('change',async()=>{const {error}=await sb.from('leads').update({status:s.value}).eq('id',s.dataset.id);if(error)alert(error.message)}))}
function renderCalls(data){$('#dashboardCalls').innerHTML=data.slice(0,6).length?`<div class="mini-list">${data.slice(0,6).map(x=>`<div class="mini-item"><div class="mini-title">${esc(x.caller_name||x.caller_phone||'Unknown caller')}</div><div>${esc(x.ai_summary||x.disposition||'Call recorded')}</div><div class="mini-meta">${pill(x.status)} · ${fmtDate(x.created_at)}</div></div>`).join('')}</div>`:empty('No calls recorded yet.');$('#callsTable').innerHTML=table(['Caller','Phone','Status','Emergency','Summary','Started'],data.map(x=>`<tr><td>${esc(x.caller_name||'—')}</td><td>${esc(x.caller_phone||'—')}</td><td>${pill(x.status)}</td><td>${x.emergency?'Yes':'No'}</td><td>${esc(x.ai_summary||x.disposition||'—')}</td><td>${fmtDate(x.started_at||x.created_at)}</td></tr>`))}
function renderCustomers(data){$('#customersTable').innerHTML=table(['Name','Company','Phone','Email','Source','Created'],data.map(x=>`<tr><td><strong>${esc(x.first_name)} ${esc(x.last_name)}</strong></td><td>${esc(x.company_name||'—')}</td><td>${esc(x.phone)}</td><td>${esc(x.email||'—')}</td><td>${esc(x.source||'—')}</td><td>${fmtDate(x.created_at)}</td></tr>`))}
function renderSchedule(data){$('#scheduleTable').innerHTML=table(['Start','Status','Service','Problem','Arrival window'],data.map(x=>`<tr><td>${fmtDate(x.scheduled_start)}</td><td>${pill(x.status)}</td><td>${esc(x.service_category||'—')}</td><td>${esc(x.problem_description||'—')}</td><td>${esc(x.arrival_window_minutes)} min</td></tr>`))}
function renderJobs(data){$('#jobsTable').innerHTML=table(['WO #','Status','Complaint','Diagnosis','Work performed','Created'],data.map(x=>`<tr><td><strong>#${esc(x.work_order_number)}</strong></td><td><select class="status-select job-status" data-id="${x.id}">${['open','diagnosing','quoted','approved','in_progress','completed','cancelled'].map(v=>`<option ${x.status===v?'selected':''}>${v}</option>`).join('')}</select></td><td>${esc(x.complaint||'—')}</td><td>${esc(x.diagnosis||'—')}</td><td>${esc(x.work_performed||'—')}</td><td>${fmtDate(x.created_at)}</td></tr>`));$$('.job-status').forEach(s=>s.addEventListener('change',async()=>{const patch={status:s.value};if(s.value==='completed')patch.completed_at=new Date().toISOString();const {error}=await sb.from('work_orders').update(patch).eq('id',s.dataset.id);if(error)alert(error.message)}))}
function renderDispatch(data){$('#dispatchTable').innerHTML=table(['Ticket','Urgency','Status','Caller','Phone','City','Issue','Created'],data.map(x=>`<tr><td>#${esc(x.ticket_number)}</td><td>${pill(x.urgency)}</td><td>${pill(x.status)}</td><td>${esc(x.caller_name||'—')}</td><td>${esc(x.caller_phone)}</td><td>${esc(x.city)}</td><td>${esc(x.issue_summary)}</td><td>${fmtDate(x.created_at)}</td></tr>`))}
function renderPricing(data){$('#pricingTable').innerHTML=table(['Category','Service','Option','Standard','Member','Minutes'],data.map(x=>`<tr><td>${esc(x.category)}</td><td><strong>${esc(x.service_name)}</strong><br><span class="muted">${esc(x.description||'')}</span></td><td>${esc(x.option_level)}</td><td>$${Number(x.standard_price||0).toLocaleString()}</td><td>${x.member_price!=null?'$'+Number(x.member_price).toLocaleString():'—'}</td><td>${esc(x.estimated_minutes||'—')}</td></tr>`))}
function renderInvoices(data){$('#invoicesTable').innerHTML=table(['Invoice','Title','Status','Total','Paid','Due'],data.map(x=>`<tr><td>#${esc(x.invoice_number)}</td><td>${esc(x.title)}</td><td>${pill(x.status)}</td><td>$${Number(x.total||0).toFixed(2)}</td><td>$${Number(x.amount_paid||0).toFixed(2)}</td><td>${esc(x.due_date||'—')}</td></tr>`))}

$('#saveLeadBtn').addEventListener('click',async()=>{const fd=new FormData($('#leadForm')),row=Object.fromEntries(fd.entries());row.source='office_manual';row.status='new';const {error}=await sb.from('leads').insert(row);if(error)return alert(error.message);$('#leadModal').close();$('#leadForm').reset();await refreshAll()});
$('#saveCustomerBtn').addEventListener('click',async()=>{const fd=new FormData($('#customerForm'));const row=Object.fromEntries(fd.entries());const address=row.address_line1,city=row.city,postal=row.postal_code;delete row.address_line1;delete row.city;delete row.postal_code;row.source='office_manual';const {data,error}=await sb.from('customers').insert(row).select('id').single();if(error)return alert(error.message);if(address&&city){const {error:pe}=await sb.from('properties').insert({customer_id:data.id,address_line1:address,city,state:'SC',postal_code:postal||null});if(pe)alert('Customer saved, but address could not be saved: '+pe.message)}$('#customerModal').close();$('#customerForm').reset();await refreshAll()});

if('serviceWorker' in navigator)navigator.serviceWorker.register('/ops/sw.js').catch(()=>{});
sb.auth.onAuthStateChange(()=>setTimeout(()=>boot().catch(e=>msg(e.message||'Could not load account',true)),0));
$('#authMsg').classList.add('hidden');
$$('#authForm button').forEach(b=>b.disabled=false);
boot().catch(e=>msg(e.message||'Could not load account',true));
}catch(e){
  startupMessage.textContent='Sign-in could not start. Refresh the page and try again.';
  startupMessage.classList.remove('hidden');
  startupMessage.classList.add('error');
  document.querySelectorAll('#authForm button').forEach(b=>b.disabled=true);
  console.error('PP911 Operations startup failed',e);
}
})();
