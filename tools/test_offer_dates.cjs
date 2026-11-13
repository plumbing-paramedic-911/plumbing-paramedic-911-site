// Promotions carry a deadline. When one passes, the offer stays on the live
// site advertising terms the business will not honour, and Google keeps an
// expired priceValidUntil in its structured-data index. That is how the
// October 2026 repipe offer sat live until 2026-11-13.
//
// This fails the quality gate when any built page carries a deadline that has
// already passed, so an expired offer gets noticed at review time instead of
// by a customer. Runs after release_build.py.
//
// To clear a failure: either refresh the offer with a new date, or retire it
// the way the repipe offer was retired in tools/build.py.
const {test}=require('node:test');
const assert=require('node:assert/strict');
const fs=require('node:fs');
const path=require('node:path');
const root=path.join(__dirname,'..');

const MONTHS=['january','february','march','april','may','june','july','august',
  'september','october','november','december'];

// "booked by October 31, 2026", "Offer Ends October 31, 2026", and the other
// phrasings the promo blocks use. Deliberately narrow: a date in prose that
// is not an offer deadline is not this test's business.
const DEADLINE=new RegExp(
  '(?:booked|signed|completed|scheduled|ends|expires|valid through|redeem(?:ed)? by)\\s*' +
  '(?:by\\s+)?(' + MONTHS.join('|') + ')\\s+(\\d{1,2}),\\s*(\\d{4})','gi');
const PRICE_VALID_UNTIL=/"priceValidUntil"\s*:\s*"(\d{4})-(\d{2})-(\d{2})"/g;

const today=()=>{const d=new Date();return Date.UTC(d.getUTCFullYear(),d.getUTCMonth(),d.getUTCDate());};

const htmlPages=()=>{
  const found=[];
  const walk=dir=>{
    for(const entry of fs.readdirSync(dir,{withFileTypes:true})){
      if(entry.name.startsWith('.')||entry.name==='node_modules')continue;
      const full=path.join(dir,entry.name);
      if(entry.isDirectory())walk(full);
      else if(entry.name.endsWith('.html'))found.push(full);
    }
  };
  walk(root);
  return found;
};

test('no page advertises an offer deadline that has already passed',()=>{
  const now=today();
  const expired=[];
  for(const file of htmlPages()){
    const text=fs.readFileSync(file,'utf8');
    const rel=path.relative(root,file);
    for(const m of text.matchAll(DEADLINE)){
      const when=Date.UTC(Number(m[3]),MONTHS.indexOf(m[1].toLowerCase()),Number(m[2]));
      if(when<now)expired.push(`${rel}: "${m[0].trim()}" passed`);
    }
  }
  assert.deepEqual([...new Set(expired)],[],
    'an expired offer deadline is live on the site — refresh the offer or retire it');
});

test('no structured-data offer is already out of date',()=>{
  const now=today();
  const expired=[];
  for(const file of htmlPages()){
    const text=fs.readFileSync(file,'utf8');
    const rel=path.relative(root,file);
    for(const m of text.matchAll(PRICE_VALID_UNTIL)){
      const when=Date.UTC(Number(m[1]),Number(m[2])-1,Number(m[3]));
      if(when<now)expired.push(`${rel}: priceValidUntil ${m[1]}-${m[2]}-${m[3]} has passed`);
    }
  }
  assert.deepEqual([...new Set(expired)],[],
    'an expired priceValidUntil is live in JSON-LD — Google indexes this as a dead offer');
});
