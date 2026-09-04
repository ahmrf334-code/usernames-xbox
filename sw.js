// Service Worker لتطبيق Xbox Names
const CACHE_NAME = 'xbox-names-v1';
const urlsToCache = [
  '/usernames-xbox/',
  '/usernames-xbox/index.html',
  '/usernames-xbox/manifest.json',
  '/usernames-xbox/sw.js'
];

// تثبيت Service Worker
self.addEventListener('install', (event) => {
  console.log('Service Worker: تثبيت...');
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      console.log('Service Worker: فتح الذاكرة المؤقتة');
      return cache.addAll(urlsToCache);
    })
  );
  self.skipWaiting();
});

// تفعيل Service Worker
self.addEventListener('activate', (event) => {
  console.log('Service Worker: تفعيل...');
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames.map((cacheName) => {
          if (cacheName !== CACHE_NAME) {
            console.log('Service Worker: حذف ذاكرة مؤقتة قديمة');
            return caches.delete(cacheName);
          }
        })
      );
    })
  );
  self.clients.claim();
});

// اعتراض الطلبات
self.addEventListener('fetch', (event) => {
  event.respondWith(
    caches.match(event.request).then((response) => {
      // إذا وجدنا الملف في الذاكرة المؤقتة
      if (response) {
        return response;
      }

      // إذا لم نجده، حاول الحصول عليه من الإنترنت
      return fetch(event.request).then((response) => {
        // تحقق من أن الرد صحيح
        if (!response || response.status !== 200 || response.type === 'error') {
          return response;
        }

        // انسخ الرد
        const responseToCache = response.clone();
        caches.open(CACHE_NAME).then((cache) => {
          cache.put(event.request, responseToCache);
        });

        return response;
      }).catch(() => {
        // إذا حدث خطأ وكان هناك نسخة مخزنة، استخدمها
        return caches.match('/usernames-xbox/index.html');
      });
    })
  );
});
