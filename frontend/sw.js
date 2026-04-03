const CACHE_NAME = 'log-solution-v1.43';
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
    './firebase-config.js',
    './manifest.json',
    './img/logo.png',
    'https://fonts.googleapis.com/icon?family=Material+Icons+Round'
];
// Nota: JS/CSS con ?v= non sono in ASSETS perché usano strategia Network-First
// e vengono cachati dinamicamente al primo accesso.

// 1. Installazione: cache solo asset statici puri
self.addEventListener('install', (event) => {
    console.log(`[SW ${CACHE_NAME}] Installazione cache...`);
    event.waitUntil(
        caches.open(CACHE_NAME).then((cache) => cache.addAll(ASSETS))
    );
    self.skipWaiting();
});

// 2. Attivazione: elimina TUTTE le cache vecchie + claim immediato
self.addEventListener('activate', (event) => {
    console.log(`[SW ${CACHE_NAME}] Attivazione: pulizia cache vecchie...`);
    event.waitUntil(
        caches.keys().then((cacheNames) =>
            Promise.all(
                cacheNames.map((name) => {
                    if (name !== CACHE_NAME) {
                        console.log('[SW] Eliminazione cache vecchia:', name);
                        return caches.delete(name);
                    }
                })
            )
        ).then(() => self.clients.claim())
    );
});

// 3. SKIP_WAITING via messaggio (forza aggiornamento immediato)
self.addEventListener('message', (event) => {
    if (event.data === 'SKIP_WAITING' || event.data?.type === 'SKIP_WAITING') {
        console.log(`[SW ${CACHE_NAME}] SKIP_WAITING ricevuto — attivazione forzata.`);
        self.skipWaiting();
    }
});

// 4. Fetch: strategie differenziate per tipo di risorsa
self.addEventListener('fetch', (event) => {
    if (event.request.method !== 'GET') return;

    const url = event.request.url;

    // ── Bypass totale: Firebase, Firestore, autenticazione ─────────────────
    if (
        url.includes('firebaseio.com') ||
        url.includes('firestore.googleapis.com') ||
        url.includes('identitytoolkit.googleapis.com') ||
        url.includes('securetoken.googleapis.com') ||
        url.endsWith('.json')
    ) {
        return;
    }

    // ── Network-First: HTML (navigazione) ───────────────────────────────────
    if (event.request.mode === 'navigate' || url.endsWith('.html')) {
        event.respondWith(
            fetch(event.request)
                .then((response) => {
                    const copy = response.clone();
                    caches.open(CACHE_NAME).then((c) => c.put(event.request, copy));
                    return response;
                })
                .catch(() => caches.match(event.request))
        );
        return;
    }

    // ── Network-First: JS e CSS (sempre freschi, fallback offline) ──────────
    // Questa strategia elimina il bisogno di bumping manuale del ?v=
    if (url.match(/\.(js|css)(\?|$)/)) {
        event.respondWith(
            fetch(event.request)
                .then((response) => {
                    const copy = response.clone();
                    caches.open(CACHE_NAME).then((c) => c.put(event.request, copy));
                    return response;
                })
                .catch(() =>
                    // Offline: prova esatto, poi ignora query string
                    caches.match(event.request)
                        .then((r) => r || caches.match(event.request, { ignoreSearch: true }))
                )
        );
        return;
    }

    // ── Cache-First: immagini e altri asset statici (cambiano raramente) ────
    event.respondWith(
        caches.match(event.request).then((cached) => {
            if (cached) return cached;
            return fetch(event.request).then((response) => {
                const copy = response.clone();
                caches.open(CACHE_NAME).then((c) => c.put(event.request, copy));
                return response;
            });
        })
    );
});
