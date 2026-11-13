// The city pricing pages, the recorded price-book snapshot and the field
// estimator all have to agree. When they drift, the customer finds out at the
// door, so this locks the three together. Runs after release_build.py.
const {test}=require('node:test');
const assert=require('node:assert/strict');
const fs=require('node:fs');
const path=require('node:path');
const root=path.join(__dirname,'..');
const estimator=require('../ops/estimator.js');
const snapshot=JSON.parse(fs.readFileSync(path.join(__dirname,'price_book_snapshot.json'),'utf8'));

const PRICED_PAGES=['plumbing-prices-greenwood-sc','plumbing-prices-anderson-sc'];
const ROW=/<td class="job-cell">(.*?)<\/td><td class="price-cell" data-label="Regular hours">\$([\d,]+)<\/td><td class="price-cell" data-label="After hours">\$([\d,]+)<\/td>/g;
const num=v=>Number(String(v).replace(/,/g,''));
const read=slug=>fs.readFileSync(path.join(root,slug,'index.html'),'utf8');
const rowsOf=slug=>[...read(slug).matchAll(ROW)].map(m=>({job:m[1],regular:num(m[2]),after:num(m[3])}));
const items=snapshot.groups.flatMap(g=>g.items);
const bySku=new Map(items.map(i=>[i.sku,i]));
const byLabel=new Map(items.map(i=>[i.published_as,i]));

test('the snapshot is a coherent record of the price book',()=>{
  assert.ok(items.length>=30,`snapshot holds only ${items.length} items`);
  assert.equal(bySku.size,items.length,'duplicate sku in the snapshot');
  assert.equal(byLabel.size,items.length,'two items published under the same label');
  for(const i of items){
    // The book stores its overtime and member columns in whole dollars.
    assert.equal(i.standard_ot_price,Math.round(i.standard_price*estimator.OT_FACTOR),
      `${i.sku}: overtime price is not the book's 1.40x uplift`);
    assert.equal(i.member_price,Math.round(i.standard_price*(1-estimator.MEMBER_RATE)),
      `${i.sku}: member price is not the published 15% off`);
    assert.equal(i.member_ot_price,Math.round(i.standard_ot_price*(1-estimator.MEMBER_RATE)),
      `${i.sku}: after-hours member price is not 15% off the overtime price`);
  }
});

test('every published price is the snapshot price, and what the estimator quotes',()=>{
  for(const slug of PRICED_PAGES){
    const rows=rowsOf(slug);
    assert.equal(rows.length,items.length,
      `${slug} publishes ${rows.length} prices but the snapshot holds ${items.length}`);
    for(const {job,regular,after} of rows){
      const item=byLabel.get(job);
      assert.ok(item,`${slug}: "${job}" is published but is not in the price-book snapshot`);
      // The page must show the recorded book price, not something recomputed.
      assert.equal(regular,item.standard_price,`${slug}: ${job} regular-hours price`);
      assert.equal(after,item.standard_ot_price,`${slug}: ${job} after-hours price`);
      // And the estimator, given that same book row, must quote the same thing.
      const line={std:item.standard_price,mem:item.member_price,
                  stdOt:item.standard_ot_price,memOt:item.member_ot_price,kind:'service'};
      assert.equal(estimator.priceFor(line,{afterHours:false}),regular,`${slug}: ${job} estimator, regular hours`);
      assert.equal(estimator.priceFor(line,{afterHours:true}),after,`${slug}: ${job} estimator, after hours`);
      assert.equal(estimator.priceFor(line,{member:true,afterHours:false}),item.member_price,`${slug}: ${job} estimator, member`);
      assert.equal(estimator.priceFor(line,{member:true,afterHours:true}),item.member_ot_price,`${slug}: ${job} estimator, member after hours`);
    }
  }
});

test('no page promises that the time of day leaves the repair price alone',()=>{
  const retired=['sets the service-call charge only, not the repair price','not the repair price'];
  const offenders=[];
  const walk=dir=>{
    for(const entry of fs.readdirSync(dir,{withFileTypes:true})){
      if(entry.name.startsWith('.')||entry.name==='node_modules')continue;
      const full=path.join(dir,entry.name);
      if(entry.isDirectory())walk(full);
      else if(entry.name.endsWith('.html')){
        const text=fs.readFileSync(full,'utf8');
        for(const phrase of retired)
          if(text.includes(phrase))offenders.push(`${path.relative(root,full)}: ${phrase}`);
      }
    }
  };
  walk(root);
  assert.deepEqual(offenders,[]);
});

test('the pages state the after-hours policy where they quote a price',()=>{
  for(const slug of PRICED_PAGES){
    const text=read(slug);
    assert.match(text,/After hours/,`${slug} is missing the after-hours column`);
    assert.match(text,/Why is the after-hours price higher\?/,`${slug} is missing the after-hours explanation`);
    assert.match(text,/15% less in either column/,`${slug} must say the member discount applies to both columns`);
  }
});
