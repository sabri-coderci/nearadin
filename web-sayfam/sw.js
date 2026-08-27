// Simple service worker for caching shell resources
const CACHE = 'nearadin-shell-v1'
const ASSETS = [
  '/web-sayfam/',
  '/web-sayfam/index.html',
  '/web-sayfam/css/styles.css',
  '/web-sayfam/js/app.js'
]
self.addEventListener('install', e=>{
  e.waitUntil(caches.open(CACHE).then(c=>c.addAll(ASSETS)))
})
self.addEventListener('fetch', e=>{
  if(e.request.method !== 'GET') return
  e.respondWith(caches.match(e.request).then(r=>r||fetch(e.request).then(res=>{if(res && res.type==='basic') { const c = res.clone(); caches.open(CACHE).then(cache=>cache.put(e.request,c)) } return res})))
})
