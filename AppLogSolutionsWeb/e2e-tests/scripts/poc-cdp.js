const { chromium } = require('playwright');

(async () => {
    console.log("=== INIZIO POC CDP ===");
    const browser = await chromium.launch({ headless: true });
    const context = await browser.newContext();
    const page = await context.newPage();
    
    // Creiamo sessione CDP agganciata alla pagina
    const client = await context.newCDPSession(page);
    
    const requests = new Map();
    let swFound = false;

    // Quando un nuovo target viene rilevato (incluso il SW)
    client.on('Target.attachedToTarget', async (event) => {
        const swSessionId = event.sessionId;
        if (event.targetInfo.type === 'service_worker') {
            swFound = true;
            console.log(`\n[CDP-1] Individuato target Service Worker: ${event.targetInfo.url}`);
            console.log(`[CDP-2] Collegamento alla sessione figlio completato (SessionId: ${swSessionId})`);
            
            try {
                // Inviamo comandi direttamente alla sessione del SW tramite Target.sendMessageToTarget
                await client.send('Target.sendMessageToTarget', {
                    sessionId: swSessionId,
                    message: JSON.stringify({id: 1, method: 'Network.enable', params: {}})
                });
                
                await client.send('Target.sendMessageToTarget', {
                    sessionId: swSessionId,
                    message: JSON.stringify({id: 2, method: 'Runtime.enable', params: {}})
                });

                // 5. Blocchiamo una richiesta di test
                // Firebase SDK usa firebase-app.js
                await client.send('Target.sendMessageToTarget', {
                    sessionId: swSessionId,
                    message: JSON.stringify({id: 3, method: 'Network.setBlockedURLs', params: { urls: ['*firebase-app.js*']}})
                });
                console.log(`[CDP] Comandi Network e Runtime abilitati sul SW. Blocco URLs impostato.`);
            } catch (err) {
                console.error("Errore nell'abilitazione:", err);
            }
        }
    });

    // Ascoltiamo i messaggi grezzi in entrata dai target figli
    client.on('Target.receivedMessageFromTarget', (event) => {
        const message = JSON.parse(event.message);
        
        // 3. Intercettiamo Network.requestWillBeSent
        if (message.method === 'Network.requestWillBeSent') {
            const reqId = message.params.requestId;
            const url = message.params.request.url;
            // 4. Correla requestId e URL
            requests.set(reqId, url);
            
            if (url.includes('firebase')) {
                console.log(`[CDP-3/4] RequestWillBeSent (SW) -> reqId: ${reqId}, URL: ${url.substring(0,80)}...`);
            }
        }
        // 6. Riceviamo Network.loadingFailed
        else if (message.method === 'Network.loadingFailed') {
            const reqId = message.params.requestId;
            const url = requests.get(reqId) || 'Sconosciuto';
            if (url.includes('firebase')) {
                console.log(`[CDP-5/6] LoadingFailed (SW) -> reqId: ${reqId}, errore: ${message.params.errorText}, URL correlato: ${url}`);
            }
        }
        // 7. Raccogliamo i console.log
        else if (message.method === 'Runtime.consoleAPICalled') {
            const args = message.params.args.map(a => a.value).join(' ');
            if (args.includes('Firebase') || args.includes('cache')) {
                console.log(`[CDP-7] Console SW -> ${args}`);
            }
        }
    });

    // Configura auto-attach senza flatten per ricevere messaggi incapsulati in receivedMessageFromTarget
    await client.send('Target.setAutoAttach', {
        autoAttach: true,
        waitForDebuggerOnStart: false,
        flatten: false
    });

    console.log("Navigazione in corso su https://log-solutions-sviluppo.web.app/ ...");
    // Navighiamo nell'ambiente di staging in cui il service worker tenterà di registrarsi ed eseguire le fetch
    await page.goto('https://log-solutions-sviluppo.web.app/', { waitUntil: 'networkidle' });
    
    // Attesa estesa per permettere le chiamate di fetch del SW
    await page.waitForTimeout(10000);
    
    if (!swFound) {
        console.log("ERRORE: Service Worker non rilevato. L'ambiente potrebbe non aver installato il SW.");
    }

    await browser.close();
    console.log("=== FINE POC ===");
})();
