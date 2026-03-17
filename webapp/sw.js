const CACHE_NAME = 'log-solution-v1.12';
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
    './trip-tracker.js',
    './manifest.json',
    './img/logo.png',
    'https://fonts.googleapis.com/icon?family=Material+Icons+Round'
];

// 1. Installazione: Cache degli asset statici
self.addEventListener('install', (event) => {
    event.waitUntil(
        caches.open(CACHE_NAME).then((cache) => {
            console.log('Service Worker: Caching assets v1.8 (Force Refresh)...');
            return cache.addAll(ASSETS);
        })
    );
    // Forza il Service Worker a diventare attivo immediatamente
    self.skipWaiting();
});

// 2. Attivazione: Pulizia delle vecchie cache
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
    // Assicura che il SW controlli subito tutti i client aperti
    return self.clients.claim();
});

// 3. Gestione Messaggi: Salto dell'attesa se richiesto
self.addEventListener('message', (event) => {
    if (event.data === 'SKIP_WAITING') {
        self.skipWaiting();
    }
});

// 4. Fetch: Strategie differenziate tra Asset e Dati
self.addEventListener('fetch', (event) => {
    // Gestiamo solo le richieste GET (POST/PUT/DELETE non possono essere messe in cache)
    if (event.request.method !== 'GET') return;
    
    const url = event.request.url;

    // ESCLUSIONE TOTALE: Firebase, Google APIs e chiamate a dati dinamici (JSON)
    if (url.includes('google.com') || url.includes('firebase') || url.includes('firestore') || url.endsWith('.json')) {
        return; // Lascia che la richiesta vada normalmente al network
    }

    // Strategia per HTML (Principalmente Pagine): Network-First
    if (event.request.mode === 'navigate' || url.endsWith('.html')) {
        event.respondWith(
            fetch(event.request)
                .then((response) => {
                    // Se la risposta è valida, aggiorniamo la cache
                    const copy = response.clone();
                    caches.open(CACHE_NAME).then((cache) => cache.put(event.request, copy));
                    return response;
                })
                .catch(() => caches.match(event.request))
        );
        return;
    }

    // Strategia per Asset Statici (CSS, JS, Fonts): Cache-First
    event.respondWith(
        caches.match(event.request).then((cachedResponse) => {
            if (cachedResponse) {
                return cachedResponse;
            }
            return fetch(event.request).then((response) => {
                // Mettiamo in cache nuovi asset scoperti (es. icone caricate dinamicamente)
                const copy = response.clone();
                caches.open(CACHE_NAME).then((cache) => cache.put(event.request, copy));
                return response;
            });
        })
    );
});
