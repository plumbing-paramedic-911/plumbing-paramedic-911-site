/* estimator.js — field estimates, plumbing calculators and printable PDFs.
 *
 * Ported from the browser-only Stage 1 estimator so that /ops/ can price a job
 * from the production price book, size it with the trade calculators and hand
 * the customer a printed estimate.
 *
 * Nothing here writes to the database. An estimate lives in the page until it
 * is printed, so a mis-typed line can never land on a customer record, and the
 * `estimates` table keeps its current meaning (approved work, created by the
 * job workflow) until line-item storage is designed for it.
 *
 * PDFs come from the browser's own print dialog rather than a PDF library:
 * no dependency, works offline, and on a phone it is Share -> Print -> Save
 * to Files with selectable text at the printer's native resolution.
 */
(function(root){
'use strict';

const esc=v=>String(v??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const num=v=>{const n=Number(v);return Number.isFinite(n)?n:0;};
const round2=n=>Math.round((n+Number.EPSILON)*100)/100;
const money=v=>num(v).toLocaleString('en-US',{style:'currency',currency:'USD'});

/* VIP Diamond Plan — 15% off covered repairs, the same rate the price book's
   member_price column already carries. Used only as the fallback for custom and
   calculator lines, which have no book price of their own. */
const MEMBER_RATE=0.15;
const MEMBER_PLAN='VIP Diamond Plan';
/* After-hours uplift carried by the book's standard_ot_price column (1.40x). */
const OT_FACTOR=1.40;

/* Current service/diagnostic-call policy. These are flat fees for the trip and
   diagnosis: the plan discount and the after-hours uplift do not apply to them,
   because the time of day is already priced into the fee itself. */
const SERVICE_CALLS=[
  ['','No service call line','',0],
  ['79','$79 service call — Monday-Friday, 9 AM-5 PM','Service call — Monday-Friday, 9 AM-5 PM',79],
  ['99','$99 service call — after hours and weekends','Service call — after hours and weekends',99],
  ['158','$158 service call — after midnight or holidays','Service call — after midnight or holidays',158]
];

const BUSINESS={
  name:'Plumbing Paramedic 911',
  owner:'Eric Callaway, SC Master Plumber',
  address:'13 Callaway Dr',
  city:'Abbeville, SC 29620',
  phone:'(864) 446-8911',
  website:'plumbingparamedic911.com'
};

/* ---------------------------------------------------------------- pricing --- */

/* Per-linear-foot installed material cost by pipe material and nominal size.
   Covers pipe plus typical fittings and hangers; labor is added separately. */
const PIPE_RATES={
  pex:{'1/2':3.10,'3/4':4.40,'1':6.80},
  copper:{'1/2':9.50,'3/4':13.75,'1':19.40},
  cpvc:{'1/2':2.65,'3/4':3.60,'1':5.20},
  pvc:{'2':6.40,'3':9.20,'4':12.60},
  castiron:{'2':22.00,'3':31.00,'4':42.00}
};
/* Nominal sizes sort by the fraction they name, not by key order: a plain "1"
   is an integer-like key, so Object.keys would otherwise offer 1" before 1/2"
   and leave the biggest pipe selected by default. */
const sizeValue=s=>String(s).split('/').reduce((a,b)=>a/b);
const pipeSizes=material=>Object.keys(PIPE_RATES[material]||{}).sort((a,b)=>sizeValue(a)-sizeValue(b));

/* Rough install rate in feet per hour by material, before the difficulty
   multiplier for tight or finished spaces. */
const PIPE_FEET_PER_HOUR={pex:22,copper:9,cpvc:16,pvc:14,castiron:6};
const DIFFICULTY={
  open:{label:'Open / new construction',mult:1.0},
  attic:{label:'Attic or crawlspace',mult:1.35},
  finished:{label:'Finished walls (cut and patch)',mult:1.75},
  slab:{label:'Under slab',mult:2.4}
};
const SURFACE_CUT={soil:0,gravel:4,sod:7,asphalt:22,concrete:34};
const SURFACE_RESTORE={soil:0,gravel:3,sod:6,asphalt:18,concrete:26};
const DEFAULT_LABOR_RATE=169;

function estimatePipeRun(opts){
  const feet=Math.max(0,num(opts.feet));
  const rate=(PIPE_RATES[opts.material]||{})[opts.diameter];
  if(rate===undefined)return null;
  const diff=DIFFICULTY[opts.difficulty]||DIFFICULTY.open;
  const laborRate=num(opts.laborRate)||DEFAULT_LABOR_RATE;
  const hours=(feet/(PIPE_FEET_PER_HOUR[opts.material]||12))*diff.mult;
  const materialCost=round2(feet*rate);
  const laborCost=round2(hours*laborRate);
  return {feet,hours:round2(hours),materialCost,laborCost,total:round2(materialCost+laborCost),
    description:`${feet} lin ft of ${opts.diameter}" ${String(opts.material).toUpperCase()} — ${diff.label.toLowerCase()} (${hours.toFixed(1)} hr est.)`};
}

/* Trenching for sewer and water service. Depth drives machine time and shoring
   together, so cost per foot is not linear in depth. */
function estimateTrench(opts){
  const feet=Math.max(0,num(opts.feet));
  const depth=Math.max(1,num(opts.depth)||3);
  const surface=opts.surface||'soil';
  const depthFactor=Math.max(0.6,1+(depth-3)*0.28);
  const excavate=round2(feet*12*depthFactor);
  const cut=round2(feet*(SURFACE_CUT[surface]||0));
  const restoration=round2(feet*(SURFACE_RESTORE[surface]||0));
  return {feet,depth,excavate,cut,restoration,total:round2(excavate+cut+restoration),
    description:`${feet} lin ft trench at ${depth} ft depth through ${surface}, including backfill and surface restoration`};
}

/* Water heater sizing from peak-hour demand rules of thumb. */
function sizeWaterHeater(people,baths,hasTub){
  const p=Math.max(1,num(people)||1),b=Math.max(1,num(baths)||1);
  const demand=p*12+b*8+(hasTub?10:0);
  const gallons=demand<=46?30:demand<=62?40:demand<=78?50:demand<=96?65:80;
  return {gallons,peakDemand:demand,tanklessWorthIt:demand>75,
    note:`${p} people, ${b} bath${b>1?'s':''}${hasTub?', soaking tub':''} → about ${demand} gal peak hour. `+
      `A ${gallons} gallon tank covers it. ${demand>75?'Tankless is worth quoting at this demand.':'Tankless becomes worth quoting above 75 gal/hr.'}`};
}

/* Fixture count drives repipe pricing the way square footage drives roofing. */
function estimateRepipe(opts){
  const fixtures=Math.max(0,num(opts.fixtures));
  const stories=Math.max(1,num(opts.stories)||1);
  const material=opts.material==='copper'?'copper':'pex';
  const perFixture=material==='copper'?950:650;
  const total=round2(fixtures*perFixture*(1+(stories-1)*0.18));
  return {fixtures,stories,material,total,
    description:`Whole-home repipe in ${material.toUpperCase()} — ${fixtures} fixtures, ${stories} stor${stories>1?'ies':'y'}`};
}

/* ------------------------------------------------------------------- math --- */

/* The price a line charges under the chosen plan and hours. Book lines carry
   all four prices from the price book; custom and calculator lines fall back to
   the documented plan rate and after-hours factor. Pass-through fees are never
   discounted or upcharged. */
function priceFor(line,opts){
  const std=round2(num(line.std));
  if(line.kind==='fee')return std;
  const member=!!(opts&&opts.member), afterHours=!!(opts&&opts.afterHours);
  const stdOt=line.stdOt==null?round2(std*OT_FACTOR):round2(num(line.stdOt));
  if(!member)return afterHours?stdOt:std;
  const mem=line.mem==null?round2(std*(1-MEMBER_RATE)):round2(num(line.mem));
  if(!afterHours)return mem;
  return line.memOt==null?round2(stdOt*(1-MEMBER_RATE)):round2(num(line.memOt));
}
const lineTotal=(line,opts)=>round2(num(line.qty)*priceFor(line,opts));

/* Total an estimate. Every figure the printed sheet shows is derived here, so
   the arithmetic a customer can check on paper is the arithmetic on screen:
   standard subtotal + after-hours adjustment - plan savings = charged subtotal. */
function totals(est){
  const opts={member:!!est.member,afterHours:!!est.afterHours};
  const normal={member:false,afterHours:false};
  const sameHours={member:false,afterHours:opts.afterHours};
  let listSubtotal=0,afterHoursAdjustment=0,planSavings=0,subtotal=0,taxableBase=0;
  for(const line of est.lines||[]){
    const qty=num(line.qty);
    const base=priceFor(line,normal), hours=priceFor(line,sameHours), charged=priceFor(line,opts);
    listSubtotal+=qty*base;
    afterHoursAdjustment+=qty*(hours-base);
    planSavings+=qty*(hours-charged);
    subtotal+=qty*charged;
    if(line.taxable!==false)taxableBase+=qty*charged;
  }
  listSubtotal=round2(listSubtotal);
  afterHoursAdjustment=round2(afterHoursAdjustment);
  planSavings=round2(planSavings);
  subtotal=round2(subtotal);

  let manualDiscount=round2(Math.max(0,num(est.manualDiscount)));
  if(manualDiscount>subtotal)manualDiscount=subtotal;

  // Spread the manual discount proportionally across the taxable share so tax
  // is never charged on money the customer does not pay.
  const taxableShare=subtotal>0?taxableBase/subtotal:0;
  taxableBase=Math.max(0,round2(taxableBase-manualDiscount*taxableShare));
  const taxRate=Math.max(0,num(est.taxRate));
  const tax=round2(taxableBase*(taxRate/100));
  const total=Math.max(0,round2(subtotal-manualDiscount+tax));
  const depositPercent=Math.min(100,Math.max(0,num(est.depositPercent)));
  return {listSubtotal,afterHoursAdjustment,planSavings,subtotal,manualDiscount,
    taxableBase,taxRate,tax,total,depositPercent,deposit:round2(total*(depositPercent/100)),
    planLabel:MEMBER_PLAN,member:opts.member,afterHours:opts.afterHours};
}

/* --------------------------------------------------------- printed estimate --- */

const easternDate=d=>new Date(d).toLocaleDateString('en-US',{timeZone:'America/New_York',month:'long',day:'numeric',year:'numeric'});

function estimateNumber(now=new Date()){
  const p=Object.fromEntries(new Intl.DateTimeFormat('en-US',{timeZone:'America/New_York',year:'numeric',month:'2-digit',day:'2-digit',hour:'2-digit',minute:'2-digit',hourCycle:'h23'}).formatToParts(now).map(x=>[x.type,x.value]));
  return `EST-${p.year}${p.month}${p.day}-${p.hour}${p.minute}`;
}

function terms(est){
  const days=Math.max(1,num(est.validDays)||30);
  return `Estimate valid for ${days} days. Flat-rate pricing is based on the conditions we can see today. `+
    `If concealed conditions are found once the work is opened up we stop, explain what changed, and get your written approval before going further. `+
    `The service/diagnostic call is $79 Monday-Friday 9 AM-5 PM, $99 after hours and weekends, and $158 after midnight or on holidays. `+
    `Repair and installation work is priced separately and approved before it begins.`;
}

/* Returns the printable sheet as HTML. Pure and string-returning so the
   document can be checked without a browser, and so every customer-supplied
   value passes through esc() on its way to the page. */
function sheetHTML(est,t){
  t=t||totals(est);
  const rows=(est.lines||[]).map(l=>`<tr>
      <td>${esc(l.name)}${l.code?`<div class="sheet-code">${esc(l.code)}</div>`:''}</td>
      <td class="right">${esc(num(l.qty))}${l.unit?' '+esc(l.unit):''}</td>
      <td class="right">${money(priceFor(l,{member:est.member,afterHours:est.afterHours}))}</td>
      <td class="right">${money(lineTotal(l,{member:est.member,afterHours:est.afterHours}))}</td>
    </tr>`).join('');
  const row=(label,value,cls='')=>`<div class="${cls}"><span>${esc(label)}</span><span>${esc(value)}</span></div>`;
  const address=[est.customerCity,est.customerPostal].filter(Boolean).join(' ');
  return `<div class="sheet">
  <div class="sheet-head">
    <div>
      <strong>${esc(BUSINESS.name)}</strong>
      <div>${esc(BUSINESS.owner)}</div>
      <div>${esc(BUSINESS.address)}</div>
      <div>${esc(BUSINESS.city)}</div>
      <div>${esc(BUSINESS.phone)} · ${esc(BUSINESS.website)}</div>
    </div>
    <div class="right">
      <strong>Estimate</strong>
      <div>#${esc(est.number||estimateNumber())}</div>
      <div>${esc(easternDate(est.issuedOn||Date.now()))}</div>
      <div>Valid ${esc(Math.max(1,num(est.validDays)||30))} days</div>
    </div>
  </div>
  <div class="sheet-parties">
    <div>
      <strong>Prepared for</strong>
      <div>${esc(est.customerName||'—')}</div>
      ${est.customerAddress?`<div>${esc(est.customerAddress)}</div>`:''}
      ${address?`<div>${esc(address)}</div>`:''}
      ${est.customerPhone?`<div>${esc(est.customerPhone)}</div>`:''}
    </div>
    <div class="right">
      ${est.title?`<strong>${esc(est.title)}</strong>`:''}
      ${est.member?`<div>${esc(MEMBER_PLAN)} member</div>`:''}
      ${est.afterHours?'<div>After-hours rate</div>':''}
    </div>
  </div>
  <table class="sheet-lines">
    <thead><tr><th>Description</th><th class="right">Qty</th><th class="right">Rate</th><th class="right">Amount</th></tr></thead>
    <tbody>${rows||'<tr><td colspan="4">No line items.</td></tr>'}</tbody>
  </table>
  <div class="sheet-totals">
    ${row('Subtotal at standard pricing',money(t.listSubtotal))}
    ${t.afterHoursAdjustment>0?row('After-hours rate adjustment','+'+money(t.afterHoursAdjustment)):''}
    ${t.planSavings>0?row(MEMBER_PLAN+' savings','−'+money(t.planSavings)):''}
    ${t.manualDiscount>0?row('Discount','−'+money(t.manualDiscount)):''}
    ${t.tax>0?row(`Sales tax (${t.taxRate}%)`,money(t.tax)):''}
    ${row('Estimated total',money(t.total),'grand')}
    ${t.deposit>0?row(`Deposit to schedule (${t.depositPercent}%)`,money(t.deposit)):''}
  </div>
  ${est.notes?`<div class="sheet-notes"><strong>Notes</strong><div>${esc(est.notes)}</div></div>`:''}
  <div class="sheet-terms"><strong>Terms — </strong>${esc(terms(est))}</div>
  <div class="sheet-sign"><div>Customer signature</div><div>Date</div></div>
  <div class="sheet-foot">${esc(BUSINESS.name)} · ${esc(BUSINESS.owner)} · ${esc(BUSINESS.phone)} · ${esc(BUSINESS.website)}</div>
</div>`;
}

/* --------------------------------------------------------------------- UI --- */

function create(sb){
  const $=s=>document.querySelector(s);
  const view=$('#estimator');
  if(!view)return null;

  const est={customerName:'',customerPhone:'',customerAddress:'',customerCity:'',customerPostal:'',
    title:'',member:false,afterHours:false,lines:[],manualDiscount:0,taxRate:0,depositPercent:0,
    validDays:30,notes:'',number:estimateNumber(),issuedOn:Date.now()};
  let prices=null,pricesError='',loading=false,nextId=1;

  view.insertAdjacentHTML('beforeend',`
    <div class="panel">
      <div class="panel-head"><h3>Customer and pricing basis</h3></div>
      <div class="grid2 form-grid">
        <label>Customer name<input data-est-field="customerName" autocomplete="off"></label>
        <label>Phone<input data-est-field="customerPhone" type="tel" autocomplete="off"></label>
        <label>Service address<input data-est-field="customerAddress" autocomplete="off"></label>
        <label>City<input data-est-field="customerCity" autocomplete="off"></label>
        <label>ZIP<input data-est-field="customerPostal" autocomplete="off"></label>
        <label>Job title<input data-est-field="title" placeholder="Water heater replacement" autocomplete="off"></label>
      </div>
      <div class="filter-bar">
        <label class="checkline"><input type="checkbox" data-est-field="member"> ${esc(MEMBER_PLAN)} member — 15% off covered repairs</label>
        <label class="checkline"><input type="checkbox" data-est-field="afterHours"> After-hours, weekend or holiday rate</label>
      </div>
      <div class="filter-bar">
        <label>Service call line<select data-est-field="serviceCall">${SERVICE_CALLS.map(([v,t])=>`<option value="${esc(v)}">${esc(t)}</option>`).join('')}</select></label>
        <label>Discount ($)<input data-est-field="manualDiscount" type="number" min="0" step="0.01" value="0"></label>
        <label>Sales tax (%)<input data-est-field="taxRate" type="number" min="0" max="20" step="0.01" value="0"></label>
        <label>Deposit (%)<input data-est-field="depositPercent" type="number" min="0" max="100" step="1" value="0"></label>
        <label>Valid for (days)<input data-est-field="validDays" type="number" min="1" max="180" step="1" value="30"></label>
      </div>
      <p class="muted">Plan and after-hours prices come from the price book itself. Custom and calculator lines use the published ${esc(MEMBER_PLAN)} rate of 15% and the book's 1.40x after-hours factor. The service call is a flat fee and is never discounted or upcharged.</p>
    </div>

    <div class="panel">
      <div class="panel-head"><h3>Add from the price book</h3></div>
      <div class="filter-bar">
        <label>Search services<input type="search" data-est-search placeholder="Code, service, or keyword"></label>
        <label>Category<select data-est-category><option value="">All categories</option></select></label>
      </div>
      <div id="estimatorPrices"><p class="muted">Loading the price book…</p></div>
    </div>

    <div class="panel">
      <div class="panel-head"><h3>Field calculators</h3></div>
      <div class="grid2">
        <form class="calc-card" data-est-calc="pipe">
          <h4>Pipe run</h4>
          <div class="grid2 form-grid">
            <label>Material<select name="material">${Object.keys(PIPE_RATES).map(m=>`<option value="${m}">${m.toUpperCase()}</option>`).join('')}</select></label>
            <label>Size (in)<select name="diameter"></select></label>
            <label>Length (lin ft)<input name="feet" type="number" min="0" max="2000" step="1" value="40" required></label>
            <label>Conditions<select name="difficulty">${Object.entries(DIFFICULTY).map(([k,v])=>`<option value="${k}">${esc(v.label)}</option>`).join('')}</select></label>
            <label>Labor rate ($/hr)<input name="laborRate" type="number" min="0" max="500" step="1" value="${DEFAULT_LABOR_RATE}" required></label>
          </div>
          <p class="calc-out" data-est-out="pipe"></p>
          <button type="submit" class="btn secondary compact">Add as line item</button>
        </form>
        <form class="calc-card" data-est-calc="trench">
          <h4>Trenching</h4>
          <div class="grid2 form-grid">
            <label>Length (lin ft)<input name="feet" type="number" min="0" max="2000" step="1" value="60" required></label>
            <label>Depth (ft)<input name="depth" type="number" min="1" max="20" step="0.5" value="3" required></label>
            <label>Surface<select name="surface">${Object.keys(SURFACE_CUT).map(s=>`<option value="${s}">${s}</option>`).join('')}</select></label>
          </div>
          <p class="calc-out" data-est-out="trench"></p>
          <button type="submit" class="btn secondary compact">Add as line item</button>
        </form>
        <form class="calc-card" data-est-calc="repipe">
          <h4>Whole-home repipe</h4>
          <div class="grid2 form-grid">
            <label>Fixtures<input name="fixtures" type="number" min="0" max="60" step="1" value="12" required></label>
            <label>Stories<input name="stories" type="number" min="1" max="4" step="1" value="1" required></label>
            <label>Material<select name="material"><option value="pex">PEX</option><option value="copper">Copper</option></select></label>
          </div>
          <p class="calc-out" data-est-out="repipe"></p>
          <button type="submit" class="btn secondary compact">Add as line item</button>
        </form>
        <form class="calc-card" data-est-calc="heater">
          <h4>Water heater sizing</h4>
          <div class="grid2 form-grid">
            <label>People in home<input name="people" type="number" min="1" max="12" step="1" value="4" required></label>
            <label>Bathrooms<input name="baths" type="number" min="1" max="8" step="1" value="2" required></label>
            <label class="checkline"><input name="tub" type="checkbox"> Soaking tub</label>
          </div>
          <p class="calc-out" data-est-out="heater"></p>
          <button type="submit" class="btn secondary compact">Add sizing note</button>
        </form>
      </div>
      <p class="muted">Calculator figures are starting points for the estimate, not published prices. Review every line before printing.</p>
    </div>

    <div class="panel">
      <div class="panel-head"><h3>Estimate lines</h3><button type="button" class="btn secondary compact" data-est="custom">+ Custom line</button></div>
      <div id="estimatorLines"></div>
      <div id="estimatorTotals"></div>
      <label>Notes for the customer<textarea data-est-field="notes" rows="3" placeholder="Anything the customer should read before approving the work."></textarea></label>
    </div>`);

  const pricesHost=$('#estimatorPrices'),linesHost=$('#estimatorLines'),totalsHost=$('#estimatorTotals');
  const field=name=>view.querySelector(`[data-est-field="${name}"]`);
  const notice=(text,error=false)=>{const n=document.querySelector('#opsNotice');if(n){n.textContent=text;n.className='msg'+(error?' error':'');}};

  /* Pipe sizes depend on the material, so the size list is rebuilt with it. */
  function syncDiameters(form){
    form.diameter.innerHTML=pipeSizes(form.material.value).map(s=>`<option value="${s}">${s}"</option>`).join('');
  }

  function readFields(){
    for(const name of ['customerName','customerPhone','customerAddress','customerCity','customerPostal','title','notes']){
      const el=field(name);if(el)est[name]=el.value;
    }
    for(const name of ['manualDiscount','taxRate','depositPercent','validDays']){
      const el=field(name);if(el)est[name]=num(el.value);
    }
    est.member=!!field('member').checked;
    est.afterHours=!!field('afterHours').checked;
  }

  function serviceCallLine(){
    const value=field('serviceCall').value;
    est.lines=est.lines.filter(l=>l.source!=='service-call');
    const choice=SERVICE_CALLS.find(([v])=>v===value);
    if(!choice||!value)return;
    est.lines.unshift({id:nextId++,source:'service-call',kind:'fee',code:'SC-'+value,
      name:choice[2],unit:'each',qty:1,std:choice[3],taxable:false});
  }

  function addLine(line){
    est.lines.push({id:nextId++,kind:'service',unit:'each',qty:1,taxable:true,...line});
    renderLines();
    notice('Line added to the estimate.');
  }

  function renderPrices(){
    if(pricesError){pricesHost.innerHTML=`<div class="msg error" role="alert">The price book could not load: ${esc(pricesError)} <button type="button" class="btn secondary compact" data-est="reload-prices">Retry</button></div>`;return;}
    if(!prices){pricesHost.innerHTML='<p class="muted">Loading the price book…</p>';return;}
    const query=view.querySelector('[data-est-search]').value;
    const category=view.querySelector('[data-est-category]').value;
    const matches=root.PP911PriceBook.filter(prices,query,category);
    const shown=matches.slice(0,40);
    const rows=shown.map(p=>`<tr>
        <td data-label="Code">${esc(p.sku||'—')}</td>
        <td data-label="Service">${esc(p.service_name)}<div class="sheet-code">${esc(p.category)}</div></td>
        <td data-label="Standard">${money(p.standard_price)}</td>
        <td data-label="Member">${p.member_price==null?'—':money(p.member_price)}</td>
        <td data-label="Add"><button type="button" class="btn secondary compact" data-est="add-price" data-sku="${esc(p.id)}">Add</button></td>
      </tr>`).join('');
    pricesHost.innerHTML=`<p class="muted">${matches.length} of ${prices.length} services${matches.length>shown.length?` — showing the first ${shown.length}, narrow the search to see more`:''}</p>`+
      (rows?`<div class="table-wrap"><table class="data-table"><thead><tr><th scope="col">Code</th><th scope="col">Service</th><th scope="col">Standard</th><th scope="col">Member</th><th scope="col">Add</th></tr></thead><tbody>${rows}</tbody></table></div>`:'<p class="empty">No services match that search.</p>');
  }

  function renderLines(){
    if(!est.lines.length){linesHost.innerHTML='<p class="empty">No lines yet. Add services from the price book, run a calculator, or add a custom line.</p>';renderTotals();return;}
    const opts={member:est.member,afterHours:est.afterHours};
    linesHost.innerHTML=`<div class="table-wrap"><table class="data-table"><thead><tr>
      <th scope="col">Description</th><th scope="col">Qty</th><th scope="col">Rate</th><th scope="col">Amount</th><th scope="col">Taxable</th><th scope="col">Remove</th>
      </tr></thead><tbody>${est.lines.map(l=>`<tr data-line="${l.id}">
        <td data-label="Description">${esc(l.name)}${l.code?`<div class="sheet-code">${esc(l.code)}</div>`:''}${l.kind==='fee'?'<div class="sheet-code">Flat fee — no plan discount</div>':''}</td>
        <td data-label="Qty"><input class="qty" type="number" min="0" max="999" step="0.5" value="${esc(num(l.qty))}" data-est-qty="${l.id}" aria-label="Quantity for ${esc(l.name)}"></td>
        <td data-label="Rate">${money(priceFor(l,opts))}</td>
        <td data-label="Amount" data-amount="${l.id}">${money(lineTotal(l,opts))}</td>
        <td data-label="Taxable"><input type="checkbox" ${l.taxable===false?'':'checked'} data-est-taxable="${l.id}" aria-label="Taxable: ${esc(l.name)}"></td>
        <td data-label="Remove"><button type="button" class="btn secondary compact" data-est="remove" data-id="${l.id}">Remove</button></td>
      </tr>`).join('')}</tbody></table></div>`;
    renderTotals();
  }

  function renderTotals(){
    const t=totals(est);
    const row=(label,value,cls='')=>`<div class="${cls}"><span>${esc(label)}</span><span>${esc(value)}</span></div>`;
    totalsHost.innerHTML=`<div class="est-totals">
      ${row('Subtotal at standard pricing',money(t.listSubtotal))}
      ${t.afterHoursAdjustment>0?row('After-hours rate adjustment','+'+money(t.afterHoursAdjustment)):''}
      ${t.planSavings>0?row(MEMBER_PLAN+' savings','−'+money(t.planSavings)):''}
      ${t.manualDiscount>0?row('Discount','−'+money(t.manualDiscount)):''}
      ${t.tax>0?row(`Sales tax (${t.taxRate}%)`,money(t.tax)):''}
      ${row('Estimated total',money(t.total),'grand')}
      ${t.deposit>0?row(`Deposit to schedule (${t.depositPercent}%)`,money(t.deposit)):''}
    </div>`;
  }

  async function loadPrices(){
    if(loading||prices)return;
    loading=true;pricesError='';renderPrices();
    try{
      prices=await root.PP911PriceBook.loadAll(sb);
      const categories=[...new Set(prices.map(p=>p.category).filter(Boolean))].sort();
      view.querySelector('[data-est-category]').insertAdjacentHTML('beforeend',categories.map(c=>`<option value="${esc(c)}">${esc(c)}</option>`).join(''));
    }catch(e){pricesError=e.message||'Connection failed';}
    finally{loading=false;renderPrices();}
  }

  function print(){
    readFields();serviceCallLine();
    if(!est.customerName.trim())throw new Error('Enter the customer name before printing an estimate.');
    if(!est.lines.length)throw new Error('Add at least one line item before printing an estimate.');
    est.number=estimateNumber();est.issuedOn=Date.now();
    let sheet=document.querySelector('#estimateSheet');
    if(!sheet){sheet=document.createElement('div');sheet.id='estimateSheet';sheet.className='print-sheet';document.body.append(sheet);}
    sheet.innerHTML=sheetHTML(est);
    const previous=document.title;
    document.title=`${est.number}-${est.customerName.trim().replace(/[^\w]+/g,'-')}`;
    window.print();
    setTimeout(()=>{document.title=previous;},800);
    renderLines();
    notice(`Estimate ${est.number} sent to the print dialog. Choose "Save as PDF" to keep a copy. Nothing was saved to the database.`);
  }

  function reset(){
    est.lines=[];est.notes='';est.member=false;est.afterHours=false;
    for(const name of ['customerName','customerPhone','customerAddress','customerCity','customerPostal','title','notes'])field(name).value='';
    field('member').checked=false;field('afterHours').checked=false;field('serviceCall').value='';
    field('manualDiscount').value='0';field('taxRate').value='0';field('depositPercent').value='0';field('validDays').value='30';
    readFields();renderLines();notice('Estimate cleared.');
  }

  function custom(){
    const name=prompt('Line description');
    if(!name)return;
    const price=Number(prompt('Price for one unit ($)','0'));
    if(!Number.isFinite(price)||price<0)throw new Error('Enter a price of zero or more for the custom line.');
    addLine({name,std:round2(price),code:'',unit:'each'});
  }

  const calculators={
    pipe(f){
      const r=estimatePipeRun({material:f.material.value,diameter:f.diameter.value,feet:f.feet.value,difficulty:f.difficulty.value,laborRate:f.laborRate.value});
      if(!r)throw new Error('Choose a pipe material and size that the rate table covers.');
      return {text:`${r.description} — material ${money(r.materialCost)} + labor ${money(r.laborCost)} = ${money(r.total)}`,
        line:{name:r.description,std:r.total,unit:'job',code:'CALC-PIPE'}};
    },
    trench(f){
      const r=estimateTrench({feet:f.feet.value,depth:f.depth.value,surface:f.surface.value});
      return {text:`${r.description} — excavation ${money(r.excavate)} + surface cut ${money(r.cut)} + restoration ${money(r.restoration)} = ${money(r.total)}`,
        line:{name:r.description,std:r.total,unit:'job',code:'CALC-TRENCH'}};
    },
    repipe(f){
      const r=estimateRepipe({fixtures:f.fixtures.value,stories:f.stories.value,material:f.material.value});
      return {text:`${r.description} — ${money(r.total)}`,line:{name:r.description,std:r.total,unit:'job',code:'CALC-REPIPE'}};
    },
    heater(f){
      const r=sizeWaterHeater(f.people.value,f.baths.value,f.tub.checked);
      return {text:r.note,note:r.note};
    }
  };

  function runCalculator(form,add){
    const result=calculators[form.dataset.estCalc](form);
    view.querySelector(`[data-est-out="${form.dataset.estCalc}"]`).textContent=result.text;
    if(!add)return;
    if(result.line)return addLine(result.line);
    readFields();
    est.notes=(est.notes?est.notes.trim()+'\n':'')+result.note;
    field('notes').value=est.notes;
    notice('Sizing note added to the estimate notes.');
  }

  view.addEventListener('click',async e=>{
    const button=e.target.closest('[data-est]');
    if(!button||button.disabled)return;
    button.disabled=true;
    try{
      const action=button.dataset.est;
      if(action==='print')print();
      else if(action==='reset')reset();
      else if(action==='custom')custom();
      else if(action==='reload-prices'){prices=null;await loadPrices();}
      else if(action==='remove'){est.lines=est.lines.filter(l=>String(l.id)!==button.dataset.id);renderLines();}
      else if(action==='add-price'){
        const item=(prices||[]).find(p=>String(p.id)===button.dataset.sku);
        if(!item)throw new Error('That service is no longer in the loaded price book. Refresh and try again.');
        addLine({code:item.sku||'',name:item.service_name,std:item.standard_price,mem:item.member_price,
          stdOt:item.standard_ot_price,memOt:item.member_ot_price,taxable:item.taxable!==false});
      }
    }catch(err){notice(err.message||'That action could not be completed.',true);}
    finally{button.disabled=false;}
  });

  view.addEventListener('submit',e=>{
    const form=e.target.closest('[data-est-calc]');
    if(!form)return;
    e.preventDefault();
    if(!form.reportValidity())return;
    try{runCalculator(form,true);}catch(err){notice(err.message||'That calculator could not run.',true);}
  });

  view.addEventListener('input',e=>{
    const t=e.target;
    if(t.hasAttribute('data-est-search')||t.hasAttribute('data-est-category'))return renderPrices();
    if(t.dataset.estQty!==undefined){
      const line=est.lines.find(l=>String(l.id)===t.dataset.estQty);
      if(!line)return;
      line.qty=Math.max(0,num(t.value));
      const cell=linesHost.querySelector(`[data-amount="${line.id}"]`);
      if(cell)cell.textContent=money(lineTotal(line,{member:est.member,afterHours:est.afterHours}));
      return renderTotals();
    }
    if(t.dataset.estField==='notes'){est.notes=t.value;return;}
    if(t.dataset.estField){readFields();renderTotals();}
  });

  view.addEventListener('change',e=>{
    const t=e.target;
    if(t.dataset.estTaxable!==undefined){
      const line=est.lines.find(l=>String(l.id)===t.dataset.estTaxable);
      if(line)line.taxable=t.checked;
      return renderTotals();
    }
    if(t.name==='material'&&t.form&&t.form.dataset.estCalc==='pipe')return syncDiameters(t.form);
    if(t.dataset.estField==='serviceCall'){readFields();serviceCallLine();return renderLines();}
    if(t.dataset.estField&&t.dataset.estField!=='notes'){readFields();renderLines();}
  });

  document.querySelectorAll('#tabs button, #mobileView').forEach(el=>el.addEventListener('change',()=>{if(el.value==='estimator')loadPrices();}));
  document.querySelectorAll('#tabs button').forEach(b=>b.addEventListener('click',()=>{if(b.dataset.view==='estimator')loadPrices();}));

  syncDiameters(view.querySelector('[data-est-calc="pipe"]'));
  for(const key of Object.keys(calculators)){
    try{runCalculator(view.querySelector(`[data-est-calc="${key}"]`),false);}catch(e){/* defaults are valid; a bad default is not worth a notice */}
  }
  renderLines();
  return {loadPrices,print,state:est};
}

const api={create,sheetHTML,totals,priceFor,lineTotal,pipeSizes,estimatePipeRun,estimateTrench,sizeWaterHeater,estimateRepipe,
  estimateNumber,terms,round2,money,esc,MEMBER_RATE,OT_FACTOR,MEMBER_PLAN,SERVICE_CALLS,PIPE_RATES,DIFFICULTY,BUSINESS};
if(typeof module!=='undefined'&&module.exports)module.exports=api;else root.PP911Estimator=api;
})(typeof window==='undefined'?globalThis:window);
