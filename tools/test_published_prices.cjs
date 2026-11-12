// The city pricing pages and the field estimator quote the same jobs. When the
// two disagree, the customer finds out at the door, so this locks them together.
// Runs after release_build.py, against the generated pages.
const {test}=require('node:test');
const assert=require('node:assert/strict');
const fs=require('node:fs');
const path=require('node:path');
const root=path.join(__dirname,'..');
const estimator=require('../ops/estimator.js');

const PRICED_PAGES=['plumbing-prices-greenwood-sc','plumbing-prices-anderson-sc'];
const ROW=/<td class="job-cell">(.*?)<\/td><td class="price-cell" data-label="Regular hours">\$([\d,]+)<\/td><td class="price-cell" data-label="After hours">\$([\d,]+)<\/td>/g;
const num=v=>Number(String(v).replace(/,/g,''));
const read=slug=>fs.readFileSync(path.join(root,slug,'index.html'),'utf8');
const rowsOf=slug=>[...read(slug).matchAll(ROW)].map(m=>({job:m[1],regular:num(m[2]),after:num(m[3])}));

test('every published price is the one the estimator would quote',()=>{
  for(const slug of PRICED_PAGES){
    const rows=rowsOf(slug);
    assert.ok(rows.length>=30,`${slug} published only ${rows.length} prices`);
    for(const {job,regular,after} of rows){
      const line={std:regular,stdOt:after,kind:'service'};
      assert.equal(estimator.priceFor(line,{afterHours:false}),regular,`${slug}: ${job} regular hours`);
      assert.equal(estimator.priceFor(line,{afterHours:true}),after,`${slug}: ${job} after hours`);
      // The book stores its overtime column in whole dollars, so the published
      // figure is the rounded 1.40x uplift rather than the exact product.
      assert.equal(after,Math.round(regular*estimator.OT_FACTOR),`${slug}: ${job} published uplift`);
      // A custom line carries no stored overtime price; the estimator's fallback
      // must land on the same uplift, to the dollar.
      assert.ok(Math.abs(estimator.priceFor({std:regular,kind:'service'},{afterHours:true})-after)<1,
        `${slug}: ${job} estimator fallback drifts from the published price`);
    }
  }
});

test('no page promises that the time of day leaves the repair price alone',()=>{
  const retired=[
    'sets the service-call charge only, not the repair price',
    'not the repair price',
  ];
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
