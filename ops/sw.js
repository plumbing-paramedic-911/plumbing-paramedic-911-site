const CACHE='pp911-ops-workflow1';
const ASSETS=['/ops/','/ops/index.html','/ops/styles.css?v=20261013-workflow1','/ops/workflows.js?v=20261013-workflow1','/ops/app.js?v=20261013-workflow1','/ops/vendor/supabase-2.117.3.js','/ops/manifest.webmanifest'];
self.addEventListener('install',e=>e.waitUntil(caches.open(CACHE).then(c=>c.addAll(ASSETS)).then(()=>self.skipWaiting())));
self.addEventListener('activate',e=>e.waitUntil(caches.keys().then(keys=>Promise.all(keys.filter(k=>k.startsWith('pp911-ops-')&&k!==CACHE).map(k=>caches.delete(k)))).then(()=>self.clients.claim())));
self.addEventListener('fetch',e=>{
  if(e.request.method!=='GET')return;
  const u=new URL(e.request.url);
  if(u.origin!==location.origin||!ASSETS.includes(u.pathname+u.search))return;
  e.respondWith(fetch(e.request).then(r=>{
    if(r.ok){const copy=r.clone();e.waitUntil(caches.open(CACHE).then(c=>c.put(e.request,copy)))}
    return r;
  }).catch(async()=>await caches.match(e.request)||Response.error()));
});
