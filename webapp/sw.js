const CACHE_NAME = 'log-solution-v1.1';
const ASSETS = [
    './',
    './index.html',
    './login.html',
    './dashboard.html',
    './inserimento.html',
    './clienti.html',
    './impostazioni.html',
    './visualizzazione.html',
    './mappa_consegne.html',
    './styles.css',
    './script.js',
    './firebase-auth-sync.js',
    './firebase-config.js',
    'https://fonts.googleapis.com/icon?family=Material+Icons+Round'
];

// Installazione: Cache degli asset
self.addEventListener('install', (event) => {
    event.waitUntil(
        caches.open(CACHE_NAME).then((cache) => {
            console.log('Service Worker: Caching assets...');
            return cache.addAll(ASSETS);
        })
    );
    self.skipWaiting();
});

// Attivazione: Pulizia vecchie cache
self.addEventListener('activate', (event) => {
    event.waitUntil(
        caches.keys().then((cacheNames) => {
            return Promise.all(
                cacheNames.map((cache) => {
                    if (cache !== CACHE_NAME) {
                        console.log('Service Worker: Clearing old cache...', cache);
                        return caches.delete(cache);
                    }
                })
            );
        })
    );
    return self.clients.claim();
});

// Fetch: Network-First (preferiamo i dati freschi, ma usiamo la cache se offline)
self.addEventListener('fetch', (event) => {
    // Escludiamo le chiamate alle API (Google Sheets / Firebase) dal caching del SW
    if (event.request.url.includes('google.com') || event.request.url.includes('firebase')) {
        return;
    }

    event.respondWith(
        fetch(event.request).catch(() => {
            return caches.match(event.request);
        })
    );
});
