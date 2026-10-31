(function(root){
'use strict';
const esc=v=>String(v??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const isTest=x=>/^SYSTEM TEST\b/i.test(x.caller_name||`${x.first_name||''} ${x.last_name||''}`)||(x.tags||[]).includes('test');
const activeLead=x=>!isTest(x)&&!['spam','lost','booked'].includes(x.status);
const phoneKey=v=>{const n=String(v||'').replace(/\D/g,'');return n.length===11&&n[0]==='1'?n.slice(1):n;};
const followup=(x,now=Date.now())=>{
  if(!activeLead(x)||!['urgent','emergency'].includes(x.urgency))return null;
  if(x.acknowledged_at)return 'Acknowledged';
  const minutes=x.urgency==='emergency'?15:60;
  return now-new Date(x.created_at).getTime()>=minutes*60000?'Overdue acknowledgment':'Awaiting acknowledgment';
};
function excerpt(x){
  if(x.ai_summary)return x.ai_summary;
  const text=x.issue_summary||x.problem_description||x.complaint||'';
  if(/\bAI:.*\bUser:/s.test(text)){
    const turns=[...text.matchAll(/User:\s*(.*?)(?=\s*AI:|$)/gs)].map(m=>m[1].trim());
    return 'Caller excerpt: '+(turns.find(t=>t.length>35)||turns[0]||'Open transcript for details.').slice(0,220);
  }
  return text.length>220?text.slice(0,217)+'…':text;
}
function visibleCustomers(customers,leads){return customers.filter(c=>{
  if(!c.active||isTest(c))return false;
  const related=leads.filter(l=>l.customer_id===c.id);
  return !related.length||related.some(l=>!isTest(l)&&l.status!=='spam');
});}
function legacyRows(rows,term='',kind='',review=false,customerId=null){
  const q=term.trim().toLowerCase();
  return rows.filter(r=>(!kind||r.record_kind===kind)&&(!review||r.review_required)&&(!customerId||r.customer_id===customerId)&&(!q||JSON.stringify(r.payload).toLowerCase().includes(q)));
}
function create(sb){
  const $=s=>document.querySelector(s);
  const state={},errors={},filters={leads:'active',customers:'active',prices:''},search={};
  let refreshPromise,currentAction=null;
  const names={leads:'Leads',customers:'Customers',appointments:'Schedule',jobs:'Jobs',dispatch:'Dispatch',calls:'Calls',prices:'Price Book',invoices:'Invoices',staff:'Staff',properties:'Addresses',history:'Imported history'};
  const tables={leads:'leads',customers:'customers',appointments:'appointments',jobs:'work_orders',dispatch:'dispatch_tickets',calls:'call_sessions',prices:'price_book_items',invoices:'invoices',staff:'crm_users',properties:'properties',history:'legacy_import_records'};
  const sections={leads:'leadsTable',customers:'customersTable',appointments:'scheduleTable',jobs:'jobsTable',dispatch:'dispatchTable',calls:'callsTable',prices:'pricingTable',invoices:'invoicesTable',history:'historyTable'};
  let historyPage=0,historyCustomer=null;
  const date=v=>v?new Date(v).toLocaleString('en-US',{timeZone:'America/New_York',month:'short',day:'numeric',hour:'numeric',minute:'2-digit'}):'—';
  const money=v=>Number(v||0).toLocaleString('en-US',{style:'currency',currency:'USD'});
  const pill=v=>`<span class="pill ${esc(v)}">${esc(v||'—')}</span>`;
  const button=(action,id,label)=>`<button type="button" class="btn secondary compact" data-action="${action}" data-id="${esc(id)}">${esc(label)}</button>`;
  const staffName=id=>(state.staff||[]).find(s=>s.id===id)?.full_name||'Unassigned';
  const customerName=id=>{const c=(state.customers||[]).find(c=>c.id===id);return c?`${c.first_name} ${c.last_name}`.trim():'Customer unavailable';};
  function grid(headers,rows,empty='Nothing here yet.'){
    return rows.length?`<div class="table-wrap"><table class="data-table"><thead><tr>${headers.map(h=>`<th scope="col">${esc(h)}</th>`).join('')}</tr></thead><tbody>${rows.map(cells=>`<tr>${cells.map((v,i)=>`<td data-label="${esc(headers[i])}">${v}</td>`).join('')}</tr>`).join('')}</tbody></table></div>`:`<p class="empty">${esc(empty)}</p>`;
  }
  function info(text,error=false){const n=$('#opsNotice');n.textContent=text;n.className='msg'+(error?' error':'');}
  function show(view){document.querySelectorAll('.view').forEach(x=>x.classList.toggle('active',x.id===view));document.querySelectorAll('#tabs button').forEach(b=>b.classList.toggle('active',b.dataset.view===view));$('#mobileView').value=view;}
  function details(x){const text=x.issue_summary||x.problem_description||x.complaint||x.ai_summary||x.disposition||'';return `<div>${esc(excerpt(x)||text.slice(0,220)||'—')}</div>${text.length>220?`<details><summary>${/AI:/.test(text)?'View transcript':'View full details'}</summary><p class="transcript">${esc(text)}</p></details>`:''}`;}
  const phone=v=>phoneKey(v)?`<a href="tel:${esc(String(v).replace(/[^+0-9]/g,''))}">${esc(v)}</a>`:'<span>Missing phone</span>';
  $('#tabs').insertAdjacentHTML('beforeend','<button data-view="history">Imported history</button>');
  $('#appView main').insertAdjacentHTML('beforeend','<section id="history" class="view"><div class="page-head"><h2>Imported history</h2></div><p class="muted">Historical job export as of June 30, 2025. Due amounts and statuses are unverified historical values, not current debt or scheduled work. Item names have no prices. Staff and settings are historical references.</p><div class="panel"><label>Search imported records<input id="historySearch" type="search" placeholder="Customer, address, job number, service"></label><label>Record type<select id="historyKind"><option value="">All types</option><option value="job">Jobs</option><option value="item">Service items</option><option value="staff">Staff</option><option value="accounting">Accounting</option><option value="setting">Settings</option></select></label><label><input type="checkbox" id="historyReview"> Needs review only</label><button id="historyClear" class="btn secondary" type="button">Clear filters</button><div id="historyTable"></div></div></section>');
  $('#tabs [data-view="history"]').addEventListener('click',()=>show('history'));
  for(const id of ['historySearch','historyKind','historyReview'])$('#'+id).addEventListener(id==='historySearch'?'input':'change',()=>{historyPage=0;render('history');});
  $('#historyClear').addEventListener('click',()=>{historyCustomer=null;historyPage=0;$('#historySearch').value='';$('#historyKind').value='';$('#historyReview').checked=false;render('history');});
  $('#historyTable').addEventListener('click',e=>{const b=e.target.closest('[data-history-page]');if(b){historyPage=Number(b.dataset.historyPage);render('history');}});
  function toolbar(key,options){return `<div class="filter-bar"><label>Search ${esc(names[key].toLowerCase())}<input type="search" data-search="${key}" placeholder="Name, phone, or keyword"></label>${options?`<label>Show<select data-filter="${key}">${options.map(([v,t])=>`<option value="${v}">${t}</option>`).join('')}</select></label>`:''}</div>`;}
  for(const key of ['leads','customers','prices'])$('#'+sections[key]).insertAdjacentHTML('beforebegin',toolbar(key,key==='leads'?[['active','Active leads'],['all','All leads'],['urgent','Urgent / emergency'],['spam','Spam'],['lost','Lost']]:key==='customers'?[['active','Active customers'],['all','All records']]:null));
  $('#pricingTable').insertAdjacentHTML('beforebegin','<label>Category<select data-filter="prices"><option value="">All categories</option></select></label><p class="muted">Edition 2026.1. OT means after-hours pricing. Code 30-27: for parts costing more than $400, multiply vendor cost by 1.4; this is a quoted amount, not a fixed-price item.</p>');
  $('#stats').insertAdjacentHTML('afterend','<section id="followupQueue" class="panel" aria-label="Urgent follow-up"></section>');
  $('#appView main').insertAdjacentHTML('afterbegin','<div id="opsNotice" class="msg hidden" role="status" aria-live="polite"></div>');
  $('#tabs').insertAdjacentHTML('beforebegin','<label class="mobile-nav">Go to<select id="mobileView">'+[...document.querySelectorAll('#tabs button')].map(b=>`<option value="${b.dataset.view}">${b.textContent}</option>`).join('')+'</select></label>');
  $('#mobileView').addEventListener('change',e=>show(e.target.value));
  document.querySelectorAll('#tabs button').forEach(b=>b.addEventListener('click',()=>{$('#mobileView').value=b.dataset.view;}));
  for(const view of ['schedule','jobs'])$('#'+view+' .page-head').insertAdjacentHTML('beforeend',button('book-choose','',view==='schedule'?'+ Book appointment':'+ Book job'));
  $('#invoices .page-head').insertAdjacentHTML('beforeend',button('invoice-choose','','+ Draft invoice'));
  $('#dispatch .page-head').insertAdjacentHTML('afterend','<p class="muted">Urgent leads needing follow-up appear on the Dashboard. Dispatch tickets below come from the dispatch system.</p>');
  document.body.insertAdjacentHTML('beforeend','<dialog id="workflowModal" aria-labelledby="workflowTitle"><form id="workflowForm" class="modal-card"><div class="modal-head"><h3 id="workflowTitle"></h3><button type="button" class="icon-btn" data-close aria-label="Close">×</button></div><div id="workflowFields"></div><p id="workflowError" class="msg error hidden" role="alert"></p><div class="row gap"><button type="button" data-close class="btn secondary">Cancel</button><button type="submit" class="btn primary" id="workflowSave">Save</button></div></form></dialog>');
  async function load(key){
    if(key==='prices')return root.PP911PriceBook.loadAll(sb);
    const rows=[];
    for(let from=0;from<20000;from+=500){
      const {data,error}=await sb.from(tables[key]).select('*').order('id',{ascending:true}).range(from,from+499);
      if(error)throw error;
      rows.push(...(data||[]));if((data||[]).length<500)return rows;
    }
    throw new Error('This list exceeds 20,000 records. Ask the administrator to enable server-side filtering.');
  }
  async function refresh(){
    if(refreshPromise)return refreshPromise;
    $('#refreshBtn').disabled=true;
    refreshPromise=(async()=>{
      await Promise.all(Object.keys(tables).map(async key=>{try{state[key]=await load(key);delete errors[key];}catch(e){errors[key]=e.message||'Connection failed';}}));
      renderAll();
      const failed=Object.keys(errors);
      info(failed.length?`${failed.map(k=>names[k]).join(', ')} could not refresh. Other sections remain available. Failed sections show a retry button.`:`Updated ${date(new Date())} Eastern.`,!!failed.length);
    })().finally(()=>{refreshPromise=null;$('#refreshBtn').disabled=false;});
    return refreshPromise;
  }
  function filtered(key,rows){const term=(search[key]||'').toLowerCase();return term?rows.filter(x=>Object.values(x).some(v=>typeof v==='string'&&v.toLowerCase().includes(term))):rows;}
  function errorPanel(key){return `<div class="msg error" role="alert">${esc(names[key])} could not load: ${esc(errors[key])}. ${button('retry',key,'Retry')}</div>`;}
  function renderAll(){
    const leads=state.leads||[], customers=state.customers||[];
    const counts=[['Active leads',errors.leads?null:leads.filter(activeLead).length],['Active customers',errors.customers||errors.leads?null:visibleCustomers(customers,leads).length],['Open jobs',errors.jobs?null:(state.jobs||[]).filter(j=>!['completed','cancelled'].includes(j.status)).length],['Open dispatch',errors.dispatch?null:(state.dispatch||[]).filter(j=>!['completed','cancelled'].includes(j.status)).length]];
    $('#stats').innerHTML=counts.map(([l,n])=>`<div class="stat"><div class="num">${n??'—'}</div><div class="label">${l}</div></div>`).join('');
    for(const key of Object.keys(sections))render(key);
    renderQueue();
    $('#dashboardLeads').innerHTML=errors.leads?errorPanel('leads'):leads.filter(activeLead).sort((a,b)=>b.created_at.localeCompare(a.created_at)).slice(0,6).map(x=>`<article class="mini-item"><strong>${esc(x.caller_name||x.phone)}</strong>${details(x)}<p>${pill(x.urgency)} · ${date(x.created_at)}</p>${button('book',x.id,'Book appointment')}</article>`).join('')||'<p>No active leads.</p>';
    $('#dashboardCalls').innerHTML=errors.calls?errorPanel('calls'):(state.calls||[]).sort((a,b)=>b.created_at.localeCompare(a.created_at)).slice(0,6).map(x=>`<article class="mini-item"><strong>${esc(x.caller_name||x.caller_phone||'Unknown caller')}</strong><p>${esc((x.ai_summary||x.disposition||'Call recorded').slice(0,220))}</p><small>${date(x.created_at)}</small></article>`).join('')||'<p>No calls yet.</p>';
  }
  function renderQueue(){
    const queue=(state.leads||[]).filter(x=>followup(x)&&!x.acknowledged_at).sort((a,b)=>a.created_at.localeCompare(b.created_at));
    $('#followupQueue').innerHTML='<h3>Urgent follow-up</h3><p class="muted">On-screen acknowledgment reminders: emergency after 15 minutes; urgent after 60 minutes. Times are Eastern. Acknowledgment records staff review; it does not confirm dispatch.</p>'+(errors.leads?errorPanel('leads'):queue.map(x=>`<article class="attention-card"><strong>${esc(x.caller_name||x.phone)}</strong> ${pill(x.urgency)}<p class="${followup(x).startsWith('Overdue')?'overdue':''}">${followup(x)} · Received ${date(x.created_at)}</p>${details(x)}<p>Assigned: ${esc(staffName(x.assigned_to))}</p><div class="row gap">${phone(x.phone)}${button('ack',x.id,'Acknowledge')}${button('assign',x.id,'Assign staff')}${button('book',x.id,'Book appointment')}</div></article>`).join('')||'<p>No urgent leads awaiting acknowledgment.</p>');
  }
  function render(key){
    const host=$('#'+sections[key]);if(errors[key]){host.innerHTML=errorPanel(key);return;}
    let rows=[...(state[key]||[])];
    if(key==='leads'){
      rows=rows.filter(x=>filters.leads==='all'||filters.leads==='active'&&activeLead(x)||filters.leads==='urgent'&&!!followup(x)||x.status===filters.leads);
      rows=filtered(key,rows).sort((a,b)=>b.created_at.localeCompare(a.created_at));
      host.innerHTML=grid(['Customer','Phone','Issue','Urgency','Follow-up','Status','Actions'],rows.map(x=>[esc(x.caller_name||'Unknown caller'),phone(x.phone),details(x),pill(x.urgency),`${esc(followup(x)||'—')}<br>${esc(staffName(x.assigned_to))}${x.acknowledged_at?`<br><small>${date(x.acknowledged_at)} by ${esc(staffName(x.acknowledged_by))}</small>`:''}`,pill(x.status),`<div class="row gap">${button('lead-status',x.id,'Change status')}${button('assign',x.id,'Assign')}${activeLead(x)?button('book',x.id,'Book appointment'):''}${activeLead(x)&&!x.acknowledged_at?button('ack',x.id,'Acknowledge'):''}</div>`]),'No matching leads.');
    }else if(key==='customers'){
      if(filters.customers!=='all'&&!errors.leads)rows=visibleCustomers(rows,state.leads||[]);
      rows=filtered(key,rows);
      host.innerHTML=(errors.leads?'<p class="msg error">Lead classifications are unavailable; showing all customer records.</p>':'')+grid(['Name','Phone','Email','Record checks','Actions'],rows.map(c=>{
        const linked=(state.leads||[]).find(l=>l.customer_id===c.id&&l.caller_name&&!/unknown|system test/i.test(l.caller_name));
        const unknown=/unknown/i.test(`${c.first_name} ${c.last_name}`);
        const duplicates=phoneKey(c.phone)&&(state.customers||[]).filter(x=>phoneKey(x.phone)===phoneKey(c.phone)).length>1;
        return [esc(`${c.first_name} ${c.last_name}`),phone(c.phone),esc(c.email||'—'),`${isTest(c)?'Test record. ':''}${duplicates?'Possible duplicate phone. ':''}${unknown&&linked?'Lead name: '+esc(linked.caller_name):''}${c.source==='drive-recovery-20261031-v1'?'Imported; contact details need review.':''}`,button('customer-edit',c.id,'Edit customer')+button('customer-history',c.id,'View history')];
      }),'No matching customers.');
    }else if(key==='history'){
      rows=legacyRows(rows,$('#historySearch').value,$('#historyKind').value,$('#historyReview').checked,historyCustomer);
      const pages=Math.max(1,Math.ceil(rows.length/50));historyPage=Math.min(historyPage,pages-1);
      const start=historyPage*50;
      host.innerHTML=`<p>${rows.length} records${historyCustomer?' for '+esc(customerName(historyCustomer)):''}. Page ${historyPage+1} of ${pages}.</p>`+grid(['Type','Record','Review','Details'],rows.slice(start,start+50).map(r=>{
        const p=r.payload||{};
        const label=p['Customer name']||p['Original item path']||p['Source staff name']||p['Source name']||p.Setting||r.source_key;
        const source=/^https:\/\/docs\.google\.com\//.test(r.source_url)?`<a href="${esc(r.source_url)}" target="_blank" rel="noopener noreferrer">Source file</a>`:'';
        return [esc(r.record_kind),esc(label),r.review_required?'Needs review':(r.record_kind==='job'?'Historical record':'Historical reference'),`<details><summary>View original fields</summary><dl>${Object.entries(p).map(([k,v])=>`<dt>${esc(k)}</dt><dd style="white-space:pre-wrap">${esc(v)}</dd>`).join('')}</dl>${source}</details>`];
      }),'No matching imported records.')+`<div class="row gap"><button type="button" class="btn secondary" data-history-page="${historyPage-1}" ${historyPage===0?'disabled':''}>Previous</button><button type="button" class="btn secondary" data-history-page="${historyPage+1}" ${historyPage>=pages-1?'disabled':''}>Next</button></div>`;
    }else if(key==='appointments'){
      rows.sort((a,b)=>a.scheduled_start.localeCompare(b.scheduled_start));
      host.innerHTML=grid(['Start (Eastern)','Customer','Staff','Status','Issue','Actions'],rows.map(a=>[date(a.scheduled_start),esc(customerName(a.customer_id)),esc(staffName(a.assigned_to)),pill(a.status),details(a),button('appointment',a.id,'Update appointment')+button('job-create',a.id,'Open / create job')]),'No appointments. Use Book appointment to schedule an active lead.');
    }else if(key==='jobs'){
      host.innerHTML=grid(['Job','Customer','Technician','Status','Issue','Actions'],rows.map(j=>[`#${esc(j.work_order_number)}`,esc(customerName(j.customer_id)),esc(staffName(j.technician_id)),pill(j.status),details(j),button('job',j.id,'Update job')+button('invoice',j.id,'Draft invoice')]),'No jobs. Booking a lead creates a linked appointment and job.');
    }else if(key==='dispatch'){
      host.innerHTML=grid(['Ticket','Urgency','Status','Caller','Phone','Issue','Acknowledged'],rows.map(d=>[`#${esc(d.ticket_number)}`,pill(d.urgency),pill(d.status),esc(d.caller_name),phone(d.caller_phone),details(d),date(d.accepted_at)]),'No dispatch tickets. Review the urgent follow-up queue on the Dashboard.');
    }else if(key==='invoices'){
      host.innerHTML=grid(['Invoice','Customer','Title','Status','Total','Paid','Due'],rows.map(i=>[`#${esc(i.invoice_number)}`,esc(customerName(i.customer_id)),esc(i.title),pill(i.status),money(i.total),money(i.amount_paid),esc(i.due_date||'—')]),'No invoices. Create a draft from a job. Draft creation does not send an invoice or charge a customer.');
    }else if(key==='calls'){
      host.innerHTML=grid(['Caller','Phone','Status','Summary','Started'],rows.sort((a,b)=>b.created_at.localeCompare(a.created_at)).map(c=>[esc(c.caller_name||'Unknown caller'),phone(c.caller_phone),pill(c.status),details(c),date(c.started_at||c.created_at)]));
    }else if(key==='prices'){
      const category=$('[data-filter="prices"]');
      const categories=[...new Set(rows.map(p=>p.category).filter(Boolean))].sort((a,b)=>a.localeCompare(b));
      if(filters.prices&&!categories.includes(filters.prices))filters.prices='';
      category.innerHTML='<option value="">All categories</option>'+categories.map(c=>`<option value="${esc(c)}">${esc(c)}</option>`).join('');
      category.value=filters.prices;
      rows=root.PP911PriceBook.filter(rows,search.prices||'',filters.prices);
      const rate=v=>v==null?'—':money(v);
      host.innerHTML=`<p class="muted" role="status">${rows.length.toLocaleString('en-US')} of ${(state.prices||[]).length.toLocaleString('en-US')} services</p>`+grid(['Code','Category','Service','Standard','Standard OT','Member','Member OT','Minutes','Book page'],rows.map(p=>[esc(p.sku||'—'),esc(p.category),`<strong>${esc(p.service_name)}</strong>${p.description?`<br><span class="muted">${esc(p.description)}</span>`:''}`,rate(p.standard_price),rate(p.standard_ot_price),rate(p.member_price),rate(p.member_ot_price),esc(p.estimated_minutes??'—'),esc(p.source_page??'—')]),'No matching services.');
    }
  }
  function select(name,label,choices,value='',required=false){return `<label>${esc(label)}<select name="${name}" ${required?'required':''}>${choices.map(([v,t])=>`<option value="${esc(v)}" ${String(v)===String(value)?'selected':''}>${esc(t)}</option>`).join('')}</select></label>`;}
  function input(name,label,value='',type='text',extra=''){return `<label>${esc(label)}<input name="${name}" type="${type}" value="${esc(value)}" ${extra}></label>`;}
  function textarea(name,label,value=''){return `<label>${esc(label)}<textarea name="${name}" required>${esc(value)}</textarea></label>`;}
  function staffOptions(){if(errors.staff)throw new Error('Staff could not load. Refresh before assigning or booking.');return [['','Unassigned'],...(state.staff||[]).filter(s=>s.active).map(s=>[s.id,s.full_name])];}
  function open(title,fields,action,label='Save'){
    currentAction=action;$('#workflowTitle').textContent=title;$('#workflowFields').innerHTML=fields;$('#workflowError').classList.add('hidden');$('#workflowSave').textContent=label;$('#workflowModal').showModal();
  }
  async function rpc(name,args){const {data,error}=await sb.rpc(name,args);if(error)throw error;return data;}
  async function update(table,id,patch){const {data,error}=await sb.from(table).update(patch).eq('id',id).select('id').single();if(error)throw error;if(!data)throw new Error('Record was not saved. Refresh and try again.');}
  function requireData(keys){for(const k of keys)if(errors[k]||!state[k])throw new Error(`${names[k]} is unavailable. Refresh and try again.`);}
  function openBook(id){
    requireData(['leads','properties','staff','appointments']);
    const l=state.leads.find(x=>x.id===id);if(!l||!activeLead(l))throw new Error('Choose an active lead.');
    const p=state.properties.find(p=>p.id===l.property_id)||{};
    open('Book appointment and job',`<p>${esc(l.caller_name||l.phone)}</p><p class="muted">Choose the service time in Eastern time (South Carolina).</p>`+input('start','Appointment start (Eastern)','','datetime-local','required')+input('minutes','Duration in minutes',60,'number','required min="15" max="480" step="15"')+input('address','Service address',p.address_line1||'','text','required')+input('city','City',p.city||'','text','required')+input('postal','ZIP',p.postal_code||'')+select('staff','Assigned staff',staffOptions(),l.assigned_to||'')+textarea('summary','Issue summary',excerpt(l)),async f=>{
      const start=easternISO(f.start);if(!start)throw new Error('That Eastern time does not exist or is ambiguous because of daylight saving time. Choose another time.');
      const result=await rpc('ops_book_lead',{p_lead_id:id,p_start:start,p_minutes:Number(f.minutes),p_address:f.address,p_city:f.city,p_postal:f.postal,p_staff_id:f.staff||null,p_summary:f.summary});
      show('schedule');return result.existing?'This lead already has a booking; no duplicate was created.':'Appointment and job saved.';
    },'Book appointment and job');
  }
  function openInvoice(id){requireData(['jobs','invoices']);const j=state.jobs.find(x=>x.id===id);if(!j||j.status==='cancelled')throw new Error('Choose an active job.');
    const existing=state.invoices.find(i=>i.work_order_id===id&&i.status!=='void');if(existing){show('invoices');info(`Invoice #${existing.invoice_number} already exists for this job.`);return;}
    open('Draft invoice',`<p>Job #${esc(j.work_order_number)} · ${esc(customerName(j.customer_id))}</p><p class="muted">Creates a draft for review. No invoice is sent and no payment is collected.</p>`+input('title','Invoice title','Service invoice','text','required')+input('subtotal','Subtotal ($)','','number','required min="0" max="1000000" step="0.01"')+input('tax','Tax ($)',0,'number','required min="0" max="1000000" step="0.01"')+input('due','Due date','','date'),async f=>{await rpc('ops_draft_invoice',{p_work_order_id:id,p_title:f.title,p_subtotal:Number(f.subtotal),p_tax:Number(f.tax),p_due:f.due||null});show('invoices');return 'Invoice draft saved.';},'Create draft');
  }
  async function act(action,id){
    if(action==='customer-history'){historyCustomer=id;historyPage=0;$('#historySearch').value='';$('#historyKind').value='job';$('#historyReview').checked=false;render('history');show('history');return;}
    if(action==='retry'){delete state[id];await refresh();return;}
    if(action==='book'){openBook(id);return;}
    if(action==='invoice'){openInvoice(id);return;}
    if(action==='book-choose'||action==='invoice-choose'){
      const booking=action==='book-choose';requireData([booking?'leads':'jobs']);
      const choices=booking?state.leads.filter(activeLead).map(l=>[l.id,l.caller_name||l.phone]):state.jobs.filter(j=>j.status!=='cancelled').map(j=>[j.id,`Job #${j.work_order_number} — ${customerName(j.customer_id)}`]);
      if(!choices.length){show(booking?'leads':'jobs');info(booking?'Create a lead first, then book its appointment.':'Create a job before drafting an invoice.');return;}
      open(booking?'Choose a lead':'Choose a job',select('record','Record',[['','Choose a record'],...choices],'',true),async f=>{ $('#workflowModal').close();queueMicrotask(()=>{try{booking?openBook(f.record):openInvoice(f.record);}catch(e){info(e.message,true);}});return null;},'Continue');return;
    }
    if(action==='ack'){await rpc('ops_acknowledge_lead',{p_lead_id:id});await refresh();info('Lead acknowledged. This records staff review, not technician dispatch.');return;}
    if(action==='assign'){
      const l=state.leads.find(l=>l.id===id);open('Assign follow-up',select('staff','Staff',staffOptions(),l.assigned_to||''),async f=>{await update('leads',id,{assigned_to:f.staff||null});return 'Follow-up assignment saved.';});return;
    }
    if(action==='lead-status'){
      const l=state.leads.find(l=>l.id===id);open('Update lead status',select('status','Status',['new','contacted','qualified','booked','lost','spam'].map(v=>[v,v]),l.status)+'<p class="muted">Use Book appointment to create a linked schedule entry and job. Changing a status alone does not create a booking.</p>',async f=>{await update('leads',id,{status:f.status});return 'Lead status saved.';});return;
    }
    if(action==='job-create'){await rpc('ops_job_from_appointment',{p_appointment_id:id});await refresh();show('jobs');info('Linked job is ready.');return;}
    if(action==='job'){
      const j=state.jobs.find(j=>j.id===id);open('Update job #'+j.work_order_number,select('status','Status',['open','diagnosing','quoted','approved','in_progress','completed','cancelled'].map(v=>[v,v]),j.status)+select('staff','Technician',staffOptions(),j.technician_id||'')+textarea('diagnosis','Diagnosis / notes',j.diagnosis||'')+textarea('work','Work performed',j.work_performed||''),async f=>{await rpc('ops_update_job',{p_job_id:id,p_status:f.status,p_staff_id:f.staff||null,p_diagnosis:f.diagnosis,p_work:f.work});return 'Job updated.';});$('#workflowFields textarea').required=false;$('#workflowFields textarea[name="work"]').required=false;return;
    }
    if(action==='appointment'){
      const a=state.appointments.find(a=>a.id===id);open('Update appointment',select('status','Status',['scheduled','confirmed','en_route','on_site','completed','cancelled','no_show'].map(v=>[v,v]),a.status),async f=>{await update('appointments',id,{status:f.status});return 'Appointment status saved. Linked job status is managed separately.';});return;
    }
    if(action==='customer-edit'){requireData(['customers','leads']);
      const c=state.customers.find(c=>c.id===id);const linked=state.leads.find(l=>l.customer_id===id&&l.caller_name&&!/unknown|system test/i.test(l.caller_name));
      open('Edit customer',linked?`<p class="muted">Linked lead name: ${esc(linked.caller_name)}</p>`:'',async()=>{});
      $('#workflowFields').insertAdjacentHTML('beforeend',input('first','First name / source display name',c.first_name,'text','required')+input('last','Last name',c.last_name)+input('phone','Phone',c.phone,'tel',c.source==='drive-recovery-20261031-v1'?'':'required')+input('email','Email',c.email||'','email'));
      currentAction=async f=>{const duplicate=phoneKey(f.phone)&&state.customers.some(x=>x.id!==id&&phoneKey(x.phone)===phoneKey(f.phone));if(duplicate)throw new Error('Another customer has this phone. Review the duplicate before saving.');await update('customers',id,{first_name:f.first.trim(),last_name:f.last.trim(),phone:f.phone.trim(),email:f.email.trim()||null});return 'Customer saved.';};return;
    }
  }
  document.querySelector('#appView').addEventListener('click',async e=>{const b=e.target.closest('[data-action]');if(!b||b.disabled)return;b.disabled=true;try{await act(b.dataset.action,b.dataset.id);}catch(e){info(e.message||'Action failed. Try again.',true);}finally{b.disabled=false;}});
  document.querySelector('#appView').addEventListener('input',e=>{const k=e.target.dataset.search;if(k){search[k]=e.target.value;render(k);}});
  document.querySelector('#appView').addEventListener('change',e=>{const k=e.target.dataset.filter;if(k){filters[k]=e.target.value;render(k);}});
  document.querySelectorAll('#workflowModal [data-close]').forEach(b=>b.addEventListener('click',()=>$('#workflowModal').close()));
  $('#workflowForm').addEventListener('submit',async e=>{
    e.preventDefault();if($('#workflowSave').disabled||!$('#workflowForm').reportValidity())return;
    $('#workflowSave').disabled=true;document.querySelectorAll('#workflowModal [data-close]').forEach(b=>b.disabled=true);$('#workflowError').classList.add('hidden');
    try{const result=await currentAction(Object.fromEntries(new FormData($('#workflowForm'))));if(result!==null){$('#workflowModal').close();await refresh();info(result||'Saved.');}}
    catch(e){$('#workflowError').textContent=e.message||'Could not save. Try again.';$('#workflowError').classList.remove('hidden');}
    finally{$('#workflowSave').disabled=false;document.querySelectorAll('#workflowModal [data-close]').forEach(b=>b.disabled=false);}
  });
  $('#workflowModal').addEventListener('cancel',e=>{if($('#workflowSave').disabled)e.preventDefault();});
  setInterval(()=>{if(!document.hidden&&!document.querySelector('dialog[open]')&&!$('#appView').classList.contains('hidden'))refresh();},60000);
  return {refresh,info};
}
// Interpret the form's wall-clock time in the business zone, independent of the device zone.
// Reject DST gaps and repeated times rather than silently scheduling the wrong instant.
function easternISO(value){
  if(!/^\d{4}-\d\d-\d\dT\d\d:\d\d$/.test(value))return null;
  const matches=[];
  for(const offset of ['-04:00','-05:00']){
    const d=new Date(value+offset);if(Number.isNaN(d.getTime()))continue;
    const p=Object.fromEntries(new Intl.DateTimeFormat('en-US',{timeZone:'America/New_York',year:'numeric',month:'2-digit',day:'2-digit',hour:'2-digit',minute:'2-digit',hourCycle:'h23'}).formatToParts(d).map(x=>[x.type,x.value]));
    if(`${p.year}-${p.month}-${p.day}T${p.hour}:${p.minute}`===value)matches.push(d.toISOString());
  }
  return matches.length===1?matches[0]:null;
}
const api={create,esc,isTest,activeLead,followup,excerpt,phoneKey,visibleCustomers,easternISO,legacyRows};
if(typeof module!=='undefined')module.exports=api;else root.PP911Operations=api;
})(typeof window==='undefined'?globalThis:window);

