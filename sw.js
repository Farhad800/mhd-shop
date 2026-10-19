const C='mhd-v1',A=['/','/index.html','/manifest.webmanifest','/img/logo.png','/img/mark.png','/img/icon-192.png','/fonts/rudaw-regular.woff','/js/a0.js','/js/p0.js','/js/p1.js','/js/p2.js','/js/p3.js','/js/t.js','/js/s.js','/js/app.js'];
self.addEventListener('install',e=>{e.waitUntil(caches.open(C).then(c=>c.addAll(A)).then(()=>self.skipWaiting()))});
self.addEventListener('activate',e=>{e.waitUntil(caches.keys().then(k=>Promise.all(k.filter(x=>x!==C).map(x=>caches.delete(x)))).then(()=>self.clients.claim()))});
self.addEventListener('fetch',e=>{const r=e.request;if(r.method!=='GET'||new URL(r.url).origin!==location.origin)return;
const u=new URL(r.url);const fresh=r.mode==='navigate'||u.pathname.startsWith('/js/');
if(fresh){e.respondWith(fetch(r).then(x=>{if(x.ok){const y=x.clone();caches.open(C).then(c=>c.put(r.mode==='navigate'?'/':r,y))}return x}).catch(()=>caches.match(r.mode==='navigate'?'/':r)));return}
e.respondWith(caches.match(r).then(h=>h||fetch(r).then(x=>{if(x.ok){const y=x.clone();caches.open(C).then(c=>c.put(r,y))}return x})))});
