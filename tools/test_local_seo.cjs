// Local-search plumbing for the priority markets. Runs after release_build.py.
//
// Covers four things that were each wrong at some point and are invisible
// unless something checks them:
//   1. The homepage links the high-intent local pages. A page nothing links to
//      from the strongest page on the site is a page Google deprioritises.
//   2. The pricing hub does not name a single city, which made it compete with
//      the city pricing pages for the same term.
//   3. The priority city pages carry the business itself in JSON-LD, with the
//      real NAP and the shared @id - never a fabricated per-city identity.
//   4. No sitemap date is in the future.
const {test}=require('node:test');
const assert=require('node:assert/strict');
const fs=require('node:fs');
const path=require('node:path');
const root=path.join(__dirname,'..');
const read=rel=>fs.readFileSync(path.join(root,rel),'utf8');

// The single source of truth, from CLAUDE.md.
const NAP={
  name:'Plumbing Paramedic 911',
  telephone:'+1-864-446-8911',
  streetAddress:'13 Callaway Dr',
  addressLocality:'Abbeville',
  addressRegion:'SC',
  postalCode:'29620',
};
const BASE='https://plumbingparamedic911.com';
const LOCALBUSINESS_ID=`${BASE}/#localbusiness`;
// Every city page, including the two hand-authored lake-area pages that
// build.py does not generate and release_build.py injects into instead.
const SCHEMA_CITIES=[
  'abbeville-sc','greenwood-sc','anderson-sc','laurens-sc','mccormick-sc',
  'ninety-six-sc','calhoun-falls-sc','due-west-sc',
  'iva-lake-secession-sc','savannah-lakes-village-sc',
];

const graphOf=rel=>{
  const text=read(rel);
  const nodes=[];
  for(const m of text.matchAll(/<script type="application\/ld\+json">([\s\S]*?)<\/script>/g)){
    const parsed=JSON.parse(m[1]);
    nodes.push(...(parsed['@graph']||[parsed]));
  }
  return nodes;
};

const danglingRefs=nodes=>{
  const defined=new Set(nodes.map(n=>n['@id']).filter(Boolean));
  const refs=new Set();
  const walk=o=>{
    if(Array.isArray(o)){o.forEach(walk);return;}
    if(o&&typeof o==='object'){
      const keys=Object.keys(o);
      if(keys.length===1&&keys[0]==='@id'){refs.add(o['@id']);return;}
      for(const k of keys)walk(o[k]);
    }
  };
  walk(nodes);
  return [...refs].filter(r=>!defined.has(r));
};

test('every city page under /service-areas/ is covered by these tests',()=>{
  // A city page added later must either carry the business schema or be added
  // here deliberately - it must not simply go unchecked.
  const dir=path.join(root,'service-areas');
  const found=fs.readdirSync(dir,{withFileTypes:true})
    .filter(e=>e.isDirectory()&&fs.existsSync(path.join(dir,e.name,'index.html')))
    .map(e=>e.name);
  const missing=found.filter(c=>!SCHEMA_CITIES.includes(c));
  assert.deepEqual(missing,[],'a city page exists that no business-schema test covers');
});

test('the homepage links every city+service page, not a subset',()=>{
  // It linked 4 of 16 and nothing linked the other 12 from the strongest page
  // on the site. The block is generated from MONEY_PAGES now, so this asserts
  // the invariant rather than a hand-kept list: every root-level *-sc page
  // directory must be linked from the homepage.
  const home=read('index.html');
  const pages=fs.readdirSync(root,{withFileTypes:true})
    .filter(e=>e.isDirectory()&&/-sc$/.test(e.name)
      &&fs.existsSync(path.join(root,e.name,'index.html')))
    .map(e=>e.name);
  assert.ok(pages.length>=14,`expected the local pages to exist, found ${pages.length}`);
  const missing=pages.filter(slug=>!home.includes(`href="/${slug}/"`));
  assert.deepEqual(missing,[],'the homepage does not link these local pages');
});

test('the homepage keeps the markers the generated directory needs',()=>{
  // Losing either marker makes the build fail loudly rather than quietly
  // shipping a homepage that links nothing; this catches it at test time too.
  const home=read('index.html');
  assert.match(home,/money-page-directory:start/,'index.html lost the directory start marker');
  assert.match(home,/money-page-directory:end/,'index.html lost the directory end marker');
});

test('the pricing hub is not scoped to one city',()=>{
  const text=read('pricing/index.html');
  const title=/<title>([^<]*)<\/title>/.exec(text)[1];
  assert.ok(!/Abbeville/i.test(title),
    `the pricing hub title names a single city and competes with the city pricing pages: ${title}`);
  assert.ok(title.length<=62,`pricing title is ${title.length} chars, over the 62 Google shows`);
  const desc=/<meta\s+name="description"\s+content="([^"]*)"/i.exec(text)[1];
  assert.ok(!/Abbeville SC/i.test(desc),
    'the pricing hub meta description still narrows the page to Abbeville');
});

test('every city page carries the business, with the real NAP',()=>{
  for(const city of SCHEMA_CITIES){
    const nodes=graphOf(`service-areas/${city}/index.html`);
    const lb=nodes.find(n=>[].concat(n['@type']||[]).includes('LocalBusiness'));
    assert.ok(lb,`service-areas/${city}/ has no LocalBusiness node`);
    assert.ok([].concat(lb['@type']).includes('Plumber'),`${city}: LocalBusiness is not also a Plumber`);
    assert.equal(lb.name,NAP.name,`${city}: business name`);
    assert.equal(lb.telephone,NAP.telephone,`${city}: telephone`);
    assert.equal(lb.address.streetAddress,NAP.streetAddress,`${city}: street`);
    assert.equal(lb.address.addressLocality,NAP.addressLocality,`${city}: locality`);
    assert.equal(lb.address.addressRegion,NAP.addressRegion,`${city}: region`);
    assert.equal(lb.address.postalCode,NAP.postalCode,`${city}: postal code`);
    assert.ok(lb.geo&&lb.geo.latitude&&lb.geo.longitude,`${city}: missing geo coordinates`);
    assert.ok(lb.openingHoursSpecification,`${city}: missing opening hours`);
  }
});

test('the city pages claim one business, not a branch per city',()=>{
  // A per-city @id, or a city address on the business, would assert locations
  // that do not exist. One licensed plumber, one Abbeville address.
  for(const city of SCHEMA_CITIES){
    const nodes=graphOf(`service-areas/${city}/index.html`);
    const lb=nodes.find(n=>[].concat(n['@type']||[]).includes('LocalBusiness'));
    assert.equal(lb['@id'],LOCALBUSINESS_ID,
      `${city}: LocalBusiness uses its own @id, which claims a branch office that does not exist`);
    assert.equal(lb.address.addressLocality,'Abbeville',
      `${city}: the business address was localised to the city - that is a fabricated location`);
  }
});

test('every city page resolves every schema reference it makes',()=>{
  for(const city of SCHEMA_CITIES){
    const left=danglingRefs(graphOf(`service-areas/${city}/index.html`));
    assert.deepEqual(left,[],`service-areas/${city}/ points at schema nodes it does not define`);
  }
});

test('every page ships parseable JSON-LD',()=>{
  const bad=[];
  const walk=dir=>{
    for(const entry of fs.readdirSync(dir,{withFileTypes:true})){
      if(entry.name.startsWith('.')||entry.name==='node_modules')continue;
      const full=path.join(dir,entry.name);
      if(entry.isDirectory())walk(full);
      else if(entry.name.endsWith('.html')){
        const rel=path.relative(root,full);
        try{graphOf(rel);}catch(e){bad.push(`${rel}: ${e.message}`);}
      }
    }
  };
  walk(root);
  assert.deepEqual(bad,[]);
});

test('no page claims this service area has hard city water',()=>{
  // Owner correction, 2026-11-13: Greenwood city water comes off Lake
  // Greenwood and is not hard. What shortens heater life on it is the
  // chlorine used to treat it, which consumes the sacrificial anode rod and
  // works on the elements. Real hardness, with iron and sulfur, is on the
  // wells outside the city. Four pages asserted hardness as plain fact.
  // Hardness claims about the county wells are correct and not matched here.
  // USGS county estimates from the owner's own data: Abbeville County about
  // 14.0 mg/L (0.8 gpg, 231 samples) and Anderson County about 12.5 mg/L
  // (0.7 gpg, 650 samples). Both soft. Calhoun Falls is in Abbeville County.
  // Hardness claims about the WELLS outside these towns are correct and are
  // deliberately not matched here.
  const towns=['Greenwood','Abbeville','Anderson','Calhoun Falls','Ninety Six'];
  const wrong=towns.flatMap(t=>[
    new RegExp(`${t}'?s hard[- ]water`,'i'),
    new RegExp(`hard[- ]water areas? like ${t}`,'i'),
    new RegExp(`${t} and other hard[- ]water`,'i'),
    new RegExp(`hard[- ]water[^.]{0,30}\\bin ${t}\\b`,'i'),
    new RegExp(`${t}[^.]{0,30}\\bhas hard[- ]water`,'i'),
  ]);
  const offenders=[];
  const walk=dir=>{
    for(const entry of fs.readdirSync(dir,{withFileTypes:true})){
      if(entry.name.startsWith('.')||entry.name==='node_modules')continue;
      const full=path.join(dir,entry.name);
      if(entry.isDirectory())walk(full);
      else if(entry.name.endsWith('.html')){
        const text=fs.readFileSync(full,'utf8');
        for(const re of wrong)
          if(re.test(text))offenders.push(`${path.relative(root,full)}: ${re}`);
      }
    }
  };
  walk(root);
  assert.deepEqual(offenders,[],
    'a page states this service area has hard city water, which the owner corrected');
});

test('water-quality pages never overstate what a health goal means',()=>{
  // The riskiest content on this site. "Above EPA health guidelines" means
  // above the MCLG, a non-enforceable goal set to zero for compounds treated
  // as possible carcinogens. The enforceable MCLs are group totals: 80 ppb
  // for the four trihalomethanes, 60 ppb for the five haloacetic acids.
  // Reporting the first without the second reads as "your utility is poisoning
  // you", which is both untrue and a claim about a named public utility that
  // this business works alongside. A page may not do that.
  const pages=[];
  const walk=dir=>{
    for(const entry of fs.readdirSync(dir,{withFileTypes:true})){
      if(entry.name.startsWith('.')||entry.name==='node_modules')continue;
      const full=path.join(dir,entry.name);
      if(entry.isDirectory())walk(full);
      else if(entry.name.endsWith('.html'))pages.push(full);
    }
  };
  walk(root);

  // Never, on any page.
  const forbidden=[
    /water (?:is|here is) (?:not safe|unsafe)/i,
    /\b(?:illegal|unlawful)\b[^.]{0,40}(?:water|utility|system)/i,
    /(?:in violation|non-?compliant)[^.]{0,40}(?:water|utility|limit)/i,
    /exceeds? the (?:legal|enforceable|federal) limit/i,
    /causes? cancer/i,
  ];
  const offenders=[];
  for(const file of pages){
    const text=fs.readFileSync(file,'utf8');
    const rel=path.relative(root,file);
    for(const re of forbidden)
      if(re.test(text))offenders.push(`${rel}: ${re}`);
  }
  assert.deepEqual(offenders,[],'a page overstates a drinking-water finding');

  // And where a page raises the health goal, it must give the real limit.
  for(const file of pages){
    const text=fs.readFileSync(file,'utf8');
    const rel=path.relative(root,file);
    const raisesGoal=/health goal|MCLG|above (?:EPA(?:\u2019s|'s)? )?health/i.test(text);
    if(!raisesGoal)continue;
    assert.match(text,/80 ppb/,
      `${rel} raises the health goal without the 80 ppb trihalomethane limit`);
    assert.match(text,/60 ppb/,
      `${rel} raises the health goal without the 60 ppb haloacetic acid limit`);
    assert.match(text,/Consumer Confidence Report/,
      `${rel} discusses a utility's water without pointing at its own published report`);
  }
});

test('no sitemap entry claims a date in the future',()=>{
  const today=new Date().toISOString().slice(0,10);
  const future=[];
  for(const m of read('sitemap.xml').matchAll(/<loc>([^<]+)<\/loc><lastmod>(\d{4}-\d{2}-\d{2})<\/lastmod>/g))
    if(m[2]>today)future.push(`${m[1]} -> ${m[2]}`);
  assert.deepEqual(future,[],'a sitemap lastmod is in the future, which Google treats as untrustworthy');
});
