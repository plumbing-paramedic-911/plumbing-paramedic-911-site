const {test}=require('node:test');
const assert=require('node:assert/strict');
const est=require('../ops/estimator.js');

const BOOK={id:'a',code:'01-01',name:'Clear main drain',qty:1,std:400,mem:340,stdOt:560,memOt:476,taxable:true,kind:'service'};
const CUSTOM={id:'b',name:'Custom repair',qty:1,std:100,taxable:true,kind:'service'};
const FEE={id:'c',name:'Service call',qty:1,std:79,taxable:false,kind:'fee'};

test('book lines price from the book and custom lines fall back to the published plan rates',()=>{
  assert.equal(est.priceFor(BOOK,{member:false,afterHours:false}),400);
  assert.equal(est.priceFor(BOOK,{member:true,afterHours:false}),340);
  assert.equal(est.priceFor(BOOK,{member:false,afterHours:true}),560);
  assert.equal(est.priceFor(BOOK,{member:true,afterHours:true}),476);
  // No book columns: 15% off for the plan, 1.40x after hours, both together.
  assert.equal(est.priceFor(CUSTOM,{member:true,afterHours:false}),85);
  assert.equal(est.priceFor(CUSTOM,{member:false,afterHours:true}),140);
  assert.equal(est.priceFor(CUSTOM,{member:true,afterHours:true}),119);
});

test('the service call is a flat fee: no plan discount and no after-hours uplift',()=>{
  for(const opts of [{member:false,afterHours:false},{member:true,afterHours:false},{member:false,afterHours:true},{member:true,afterHours:true}])
    assert.equal(est.priceFor(FEE,opts),79);
});

test('standard pricing totals when no plan or after-hours basis is chosen',()=>{
  const t=est.totals({lines:[BOOK,CUSTOM,FEE]});
  assert.equal(t.listSubtotal,579);
  assert.equal(t.afterHoursAdjustment,0);
  assert.equal(t.planSavings,0);
  assert.equal(t.subtotal,579);
  assert.equal(t.total,579);
});

test('the printed arithmetic reconciles: standard + after-hours - plan savings = charged',()=>{
  const t=est.totals({lines:[BOOK,CUSTOM,FEE],member:true,afterHours:true,taxRate:7,manualDiscount:74,depositPercent:25});
  assert.equal(t.listSubtotal,579);
  assert.equal(t.afterHoursAdjustment,200);
  assert.equal(t.planSavings,105);
  assert.equal(t.subtotal,674);
  assert.equal(est.round2(t.listSubtotal+t.afterHoursAdjustment-t.planSavings),t.subtotal);
  // Tax follows the taxable share of what is actually charged, so the untaxed
  // fee and the customer's discount are both out of the tax base.
  assert.equal(t.taxableBase,529.67);
  assert.equal(t.tax,37.08);
  assert.equal(t.total,637.08);
  assert.equal(t.deposit,159.27);
});

test('a discount never exceeds the work and never produces a negative total',()=>{
  const t=est.totals({lines:[BOOK],manualDiscount:5000});
  assert.equal(t.manualDiscount,400);
  assert.equal(t.total,0);
  assert.equal(t.taxableBase,0);
  assert.equal(est.totals({lines:[BOOK],manualDiscount:-50}).manualDiscount,0);
});

test('quantities multiply the chosen basis rather than the standard price',()=>{
  const t=est.totals({lines:[{...BOOK,qty:3}],member:true});
  assert.equal(t.subtotal,1020);
  assert.equal(t.planSavings,180);
  assert.equal(est.lineTotal({...BOOK,qty:3},{member:true}),1020);
});

test('pipe run estimates material and labor separately',()=>{
  const r=est.estimatePipeRun({material:'pex',diameter:'3/4',feet:100,difficulty:'open',laborRate:169});
  assert.equal(r.materialCost,440);
  assert.equal(r.hours,4.55);
  assert.equal(r.laborCost,768.18);
  assert.equal(r.total,1208.18);
  assert.match(r.description,/100 lin ft of 3\/4" PEX/);
  // Finished walls cost more hours for the same footage.
  assert.ok(est.estimatePipeRun({material:'pex',diameter:'3/4',feet:100,difficulty:'finished'}).laborCost>r.laborCost);
  assert.equal(est.estimatePipeRun({material:'pex',diameter:'4',feet:10}),null);
});

test('pipe sizes are offered smallest first, not in object-key order',()=>{
  assert.deepEqual(est.pipeSizes('pex'),['1/2','3/4','1']);
  assert.deepEqual(est.pipeSizes('copper'),['1/2','3/4','1']);
  assert.deepEqual(est.pipeSizes('pvc'),['2','3','4']);
  assert.deepEqual(est.pipeSizes('nothing'),[]);
});

test('trenching charges depth, surface cut and restoration',()=>{
  assert.equal(est.estimateTrench({feet:60,depth:3,surface:'soil'}).total,720);
  const hard=est.estimateTrench({feet:60,depth:6,surface:'asphalt'});
  assert.equal(hard.excavate,1324.8);
  assert.equal(hard.cut,1320);
  assert.equal(hard.restoration,1080);
  assert.equal(hard.total,3724.8);
});

test('water heater sizing follows peak-hour demand',()=>{
  const small=est.sizeWaterHeater(4,2,true);
  assert.equal(small.peakDemand,74);
  assert.equal(small.gallons,50);
  assert.equal(small.tanklessWorthIt,false);
  const big=est.sizeWaterHeater(5,3,true);
  assert.equal(big.gallons,65);
  assert.equal(big.tanklessWorthIt,true);
  assert.equal(est.sizeWaterHeater(0,0,false).gallons,30);
});

test('repipe pricing scales with fixtures, stories and material',()=>{
  assert.equal(est.estimateRepipe({fixtures:12,stories:1,material:'pex'}).total,7800);
  assert.equal(est.estimateRepipe({fixtures:12,stories:2,material:'pex'}).total,9204);
  assert.equal(est.estimateRepipe({fixtures:12,stories:1,material:'copper'}).total,11400);
});

test('the printed sheet escapes customer text and shows the plan savings',()=>{
  const html=est.sheetHTML({customerName:'<img onerror="alert(1)">',title:'Repair',member:true,
    lines:[BOOK,FEE],depositPercent:25,validDays:30,notes:'Call before 8 AM'});
  assert.ok(!html.includes('<img'));
  assert.match(html,/&lt;img onerror=&quot;alert\(1\)&quot;&gt;/);
  assert.match(html,/VIP Diamond Plan savings/);
  assert.match(html,/−\$60\.00/);
  assert.match(html,/Call before 8 AM/);
  assert.match(html,/\$79 Monday-Friday 9 AM-5 PM, \$99 after hours and weekends, and \$158 after midnight/);
  assert.match(html,/Customer signature/);
});

test('printed terms carry the current service-call policy and no retired wording',()=>{
  const text=est.terms({validDays:30}).toLowerCase();
  assert.match(text,/estimate valid for 30 days/);
  for(const stale of ['service call fee is waived','$150 after-hours surcharge','free diagnostic','free estimate'])
    assert.ok(!text.includes(stale),`terms must not say "${stale}"`);
});

test('estimate numbers are stamped in Eastern time',()=>{
  assert.equal(est.estimateNumber(new Date('2026-10-20T15:04:00Z')),'EST-20261020-1104');
  assert.equal(est.estimateNumber(new Date('2026-12-20T15:04:00Z')),'EST-20261220-1004');
});

test('the plan rate and after-hours factor match the production price book',()=>{
  assert.equal(est.MEMBER_RATE,0.15);
  assert.equal(est.OT_FACTOR,1.40);
});
