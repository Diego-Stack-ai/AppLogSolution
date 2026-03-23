const CACHE_NAME = 'log-solution-v1.32';
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
    './gps-tracker.js',
    './firestore-service.js',
    './ui-render.js',
    './manifest.json',
    './img/logo.png',
    'https://fonts.googleapis.com/icon?family=Material+Icons+Round'
];

// 1. Installazione: Cache degli asset statici
self.addEventListener('install', (event) => {
    console.log(`[SW v1.32] Installazione cache: ${CACHE_NAME}`);
    event.waitUntil(
        caches.open(CACHE_NAME).then((cache) => {
            return cache.addAll(ASSETS);
        })
    );
    // Forza il Service Worker a diventare attivo immediatamente
    self.skipWaiting();
});

// 2. Attivazione: Pulizia TUTTE le vecchie cache + claim immediato dei client
self.addEventListener('activate', (event) => {
    console.log(`[SW v1.32] Attivazione: pulizia cache vecchie...`);
    event.waitUntil(
        caches.keys().then((cacheNames) => {
            return Promise.all(
                cacheNames.map((cache) => {
                    if (cache !== CACHE_NAME) {
                        console.log('[SW] Eliminazione cache vecchia:', cache);
                        return caches.delete(cache);
                    }
                })
            );
        }).then(() => {
            // Prende il controllo di TUTTI i tab aperti immediatamente
            return self.clients.claim();
        })
    );
});

// 3. Gestione Messaggi: accetta SKIP_WAITING sia come stringa (legacy) sia come oggetto { type: 'SKIP_WAITING' }
self.addEventListener('message', (event) => {
    if (event.data === 'SKIP_WAITING' || event.data?.type === 'SKIP_WAITING') {
        console.log(`[SW v${CACHE_NAME}] SKIP_WAITING ricevuto — attivazione forzata.`);
        self.skipWaiting();
    }
});

// 4. Fetch: Strategie differenziate
self.addEventListener('fetch', (event) => {
    if (event.request.method !== 'GET') return;

    const url = event.request.url;

    // Bypass totale per Firebase, Firestore e risorse esterne dinamiche
    if (
        url.includes('firebaseio.com') ||
        url.includes('firestore.googleapis.com') ||
        url.includes('identitytoolkit.googleapis.com') ||
        url.includes('securetoken.googleapis.com') ||
        url.endsWith('.json')
    ) {
        return;
    }

    // Strategia Network-First per pagine HTML (aggiornamenti sempre freschi)
    if (event.request.mode === 'navigate' || url.endsWith('.html')) {
        event.respondWith(
            fetch(event.request)
                .then((response) => {
                    if (url.startsWith('http') && !url.includes('chrome-extension')) {
                        const copy = response.clone();
                        caches.open(CACHE_NAME).then((cache) => cache.put(event.request, copy));
                    }
                    return response;
                })
                .catch(() => {
                    console.warn('[SW] Offline: rispondo dalla cache per', url);
                    return caches.match(event.request);
                })
        );
        return;
    }

    // Strategia Cache-First per asset statici (CSS, JS, immagini)
    event.respondWith(
        caches.match(event.request).then((cachedResponse) => {
            if (cachedResponse) {
                return cachedResponse;
            }
            return fetch(event.request).then((response) => {
                if (url.startsWith('http') && !url.includes('chrome-extension')) {
                    const copy = response.clone();
                    caches.open(CACHE_NAME).then((cache) => cache.put(event.request, copy));
                }
                return response;
            });
        })
    );
});
