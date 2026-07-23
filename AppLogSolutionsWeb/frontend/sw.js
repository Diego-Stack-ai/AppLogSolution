const CACHE_NAME = 'log-solution-v6.249';
const ASSETS = [
    './',
    './index.html',
    './login.html',
    './dashboard.html',
    './inserimento.html',
    './presenze.html',
    './gestione.html',
    './elaborazione.html',
    './link_viaggi.html',
    './centrale_resi.html',
    './pianificazione.html',
    './visualizzazione.html',
    './fatturazione.html',
    './gestione_mezzi.html',
    './impostazioni.html',
    './mappa_consegne.html',
    './mappa_google.html',
    './mappa_zone.html',
    './mappa_riepilogativa.html',
    './gestione_anomalie.html',
    './styles.css',
    './script.js',
    './firebase-config.js',
    './firebase-auth-sync.js',
    './firestore-service.js',
    './gps-tracker.js',
    './core/firebase-init.js',
    './core/auth-service.js',
    './core/connectivity-service.js',
    './core/sync-manager.js',
    './services/realtime-sync.js',
    './services/crud-service.js',
    './services/anagraficheService.js',
    './services/dipendentiService.js',
    './services/fatturazioneService.js',
    './services/viaggiService.js',
    './ui-render.js',
    './cedolini-splitter.js',
    './firebase-config-env.js',
    './manifest.json',
    './img/logo.png',
    'https://fonts.googleapis.com/icon?family=Material+Icons+Round',
    'https://unpkg.com/leaflet@1.9.4/dist/leaflet.js',
    'https://unpkg.com/leaflet@1.9.4/dist/leaflet.css',
    'https://www.gstatic.com/firebasejs/10.8.0/firebase-app.js',
    'https://www.gstatic.com/firebasejs/10.8.0/firebase-firestore.js',
    'https://www.gstatic.com/firebasejs/10.8.0/firebase-auth.js',
    'https://www.gstatic.com/firebasejs/10.8.0/firebase-storage.js',
    'https://www.gstatic.com/firebasejs/10.7.1/firebase-storage.js'
];

// 1. Installazione: cache solo asset statici puri
self.addEventListener('install', (event) => {
    console.log(`[SW ${CACHE_NAME}] Installazione cache...`);
    event.waitUntil(
        caches.open(CACHE_NAME).then((cache) => {
            // Forza il bypass della cache HTTP del browser per garantire che
            // il SW scarichi e salvi sempre l'ultimissima versione dei file dal server
            const requests = ASSETS.map(url => new Request(url, { cache: 'no-cache' }));
            return cache.addAll(requests);
        })
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
        console.log(`[SW ${CACHE_NAME}] SKIP_WAITING ricevuto ï¿½ attivazione forzata.`);
        self.skipWaiting();
    }
});

// 4. Fetch: strategie differenziate per tipo di risorsa
self.addEventListener('fetch', (event) => {
    if (event.request.method !== 'GET') return;
    const url = event.request.url;

    // Ignora richieste non http (es: chrome-extension://) per evitare errori
    if (!url.startsWith('http')) return;

    // ? Bypass totale: Firebase, Firestore, Storage, autenticazione, Sentry, server locale ?
    if (
        url.includes('firebaseio.com') ||
        url.includes('firestore.googleapis.com') ||
        url.includes('firebasestorage.googleapis.com') ||
        url.includes('storage.googleapis.com') ||
        url.includes('identitytoolkit.googleapis.com') ||
        url.includes('securetoken.googleapis.com') ||
        url.includes('maps.googleapis.com') ||
        url.includes('sentry') ||
        url.includes('localhost') ||
        url.includes('127.0.0.1') ||
        url.includes('.json') ||
        url.includes('/__/')
    ) {
        return;
    }

    if (event.request.mode === 'navigate' || url.endsWith('.html')) {
        event.respondWith(
            fetch(event.request.url, { cache: 'no-store' })
                .then((response) => {
                    const copy = response.clone();
                    caches.open(CACHE_NAME).then((c) => c.put(event.request, copy));
                    return response;
                })
                .catch(() => caches.match(event.request, { ignoreSearch: true }).then((res) => {
                    return res || new Response(`
                        <!DOCTYPE html>
                        <html>
                        <head>
                            <meta charset="utf-8">
                            <title>Offline - Log Solution</title>
                            <style>
                                body { font-family: sans-serif; text-align: center; padding: 50px; background: #f8fafc; color: #334155; }
                                h1 { color: #0f172a; }
                                p { color: #64748b; }
                            </style>
                        </head>
                        <body>
                            <h1>Sei offline 🔌</h1>
                            <p>Questa pagina non è disponibile offline perché non è stata ancora visitata online.</p>
                            <a href="dashboard.html" style="color: #3b82f6; text-decoration: none; font-weight: bold;">Torna alla Dashboard</a>
                        </body>
                        </html>
                    `, {
                        status: 200,
                        headers: { 'Content-Type': 'text/html; charset=utf-8' }
                    });
                }))
        );
        return;
    }

    // ─── Network-First: JS e CSS (sempre freschi, fallback offline) ───
    if (url.match(/\.(js|css)(\?|$)/)) {
        event.respondWith(
            fetch(event.request.url, { cache: 'no-store' })
                .then((response) => {
                    const copy = response.clone();
                    caches.open(CACHE_NAME).then((c) => c.put(event.request, copy));
                    return response;
                })
                .catch(() =>
                    caches.match(event.request, { ignoreSearch: true }).then((res) => {
                        return res || new Response('', { status: 404 });
                    })
                )
        );
        return;
    }

    // ─── Cache-First: immagini e altri asset statici (cambiano raramente) ───
    const isStaticAsset = url.match(/\.(png|jpe?g|gif|svg|woff2?|ttf|eot|ico)(\?|$)/i);
    if (isStaticAsset) {
        event.respondWith(
            caches.match(event.request, { ignoreSearch: true }).then((cached) => {
                if (cached) return cached;
                return fetch(event.request)
                    .then((response) => {
                        const copy = response.clone();
                        caches.open(CACHE_NAME).then((c) => c.put(event.request, copy));
                        return response;
                    })
                    .catch(() => {
                        return new Response('', { status: 404 });
                    });
            })
        );
        return;
    }

    // Qualsiasi altra richiesta (API, Firebase SDK non catturate prima) passa liscia!
    // Se siamo offline fallirà con ERR_INTERNET_DISCONNECTED puro, che permette a Firebase
    // di gestire correttamente lo stato offline senza andare in deadlock su una finta Response 404.
    return;
});
