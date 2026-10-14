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

let workspace;
async function refreshAll(){
  workspace ||= window.PP911Operations.create(sb);
  return workspace.refresh();
}
async function saveForm(formId,buttonId,modalId,action){
  const form=$(formId),button=$(buttonId);
  if(button.disabled||!form.reportValidity())return;
  button.disabled=true;
  try{await action(Object.fromEntries(new FormData(form)));$(modalId).close();form.reset();await refreshAll();workspace.info('Saved.');}
  catch(e){let error=form.querySelector('.save-error');if(!error){error=document.createElement('p');error.className='msg error save-error';error.setAttribute('role','alert');form.append(error);}error.textContent=e.message||'Could not save. Try again.';}
  finally{button.disabled=false;}
}
let newLeadId;
$('#saveLeadBtn').addEventListener('click',()=>saveForm('#leadForm','#saveLeadBtn','#leadModal',async row=>{
  newLeadId ||= crypto.randomUUID();
  const {error}=await sb.from('leads').upsert({...row,id:newLeadId,source:'office_manual',status:'new'},{onConflict:'id'});
  if(error)throw error;newLeadId=null;
}));
$('#leadModal').addEventListener('close',()=>{newLeadId=null;});
$('#saveCustomerBtn').addEventListener('click',()=>saveForm('#customerForm','#saveCustomerBtn','#customerModal',async row=>{
  const {error}=await sb.rpc('ops_create_customer',{p_first:row.first_name,p_last:row.last_name,p_phone:row.phone,p_email:row.email,p_address:row.address_line1,p_city:row.city,p_postal:row.postal_code});
  if(error)throw error;
}));

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
