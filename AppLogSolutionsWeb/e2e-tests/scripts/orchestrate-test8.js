const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

(async () => {
    let browser;
    try {
        console.log("=== INIZIO FASE 1: BASELINE CDP (DRY-RUN) ===");
        
        const userDataDir = path.join(__dirname, '../.profiles/pwa-cdp');
        if (fs.existsSync(userDataDir)) {
            try {
                fs.rmSync(userDataDir, { recursive: true, force: true });
                console.log("Profilo QA precedente rimosso con successo.");
            } catch(e) {
                console.log("Impossibile rimuovere completamente il profilo (file in uso), verrà riutilizzato.");
            }
        }
        
        browser = await chromium.launchPersistentContext(userDataDir, { 
            channel: 'chrome',
            headless: false
        });
        
        const page = browser.pages().length > 0 ? browser.pages()[0] : await browser.newPage();
        
        const client = await page.context().newCDPSession(page);

        let swTargetId = null;
        let swSessionId = null;
        let swUrl = null;
        let swLogs = [];
        let isActivated = false;
        
        client.on('Target.attachedToTarget', async (event) => {
            if (event.targetInfo.type === 'service_worker') {
                swTargetId = event.targetInfo.targetId;
                swSessionId = event.sessionId;
                swUrl = event.targetInfo.url;
                console.log(`[CDP] Target Service Worker rilevato: ${swUrl}`);
                
                try {
                    await client.send('Target.sendMessageToTarget', {
                        sessionId: swSessionId,
                        message: JSON.stringify({id: 1, method: 'Runtime.enable', params: {}})
                    });
                } catch(e) {}
            }
        });

        client.on('Target.receivedMessageFromTarget', (event) => {
            if (event.sessionId === swSessionId) {
                const msg = JSON.parse(event.message);
                if (msg.method === 'Runtime.consoleAPICalled') {
                    const txt = msg.params.args.map(a => (a.value || a.description || '')).join(' ');
                    swLogs.push(txt);
                    console.log(`[SW LOG] ${txt}`);
                    if (txt.toLowerCase().includes('attivato') || txt.toLowerCase().includes('activate') || txt.toLowerCase().includes('completata')) {
                        isActivated = true;
                    }
                }
            }
        });

        await client.send('Target.setAutoAttach', {
            autoAttach: true,
            waitForDebuggerOnStart: false,
            flatten: false
        });

        console.log("Navigazione diretta su login.html...");
        await page.goto('https://log-solutions-cantiere.web.app/login.html');
        
        console.log("Attendendo installazione completa SW...");
        let waitLoops = 0;
        while(waitLoops < 40) {
            if (isActivated) {
                console.log("Attivazione SW intercettata nei log!");
                break;
            }
            await page.waitForTimeout(500);
            waitLoops++;
        }
        await page.waitForTimeout(4000); 
        
        const securityOrigin = 'https://log-solutions-cantiere.web.app';
        let cacheNamesRes;
        try {
            cacheNamesRes = await client.send('CacheStorage.requestCacheNames', { securityOrigin });
        } catch (e) {
            const frameTree = await client.send('Page.getResourceTree');
            const frameId = frameTree.frameTree.frame.id;
            const storageKeyRes = await client.send('Storage.getStorageKeyForFrame', { frameId });
            cacheNamesRes = await client.send('CacheStorage.requestCacheNames', { storageKey: storageKeyRes.storageKey });
        }
        
        const cachesFound = cacheNamesRes.caches.map(c => c.cacheName);
        console.log(`[CDP] Nomi Cache rilevati:`, cachesFound);

        let allEntries = [];
        const v6Cache = cacheNamesRes.caches.find(c => c.cacheName.includes('log-solution-v6.256'));
        
        const checkSdk = async (url) => {
            try {
                const res = await client.send('CacheStorage.requestCachedResponse', {
                    cacheId: v6Cache.cacheId,
                    requestURL: url,
                    requestHeaders: []
                });
                let ct = 'Sconosciuto';
                if (res.response && res.response.headers) {
                    const ctHeader = res.response.headers.find(h => h.name.toLowerCase() === 'content-type');
                    if (ctHeader) ct = ctHeader.value;
                }
                return { 
                    found: true, 
                    url, 
                    status: res.response.statusCode,
                    responseType: res.response.responseType,
                    contentType: ct
                };
            } catch(e) {
                return { found: false, url };
            }
        };

        let sdkChecks = [];
        let localChecks = {};

        if (v6Cache) {
            let skipCount = 0;
            const pageSize = 100;
            let hasMore = true;
            while(hasMore) {
                const entriesRes = await client.send('CacheStorage.requestEntries', {
                    cacheId: v6Cache.cacheId,
                    skipCount: skipCount,
                    pageSize: pageSize
                });
                if (entriesRes.cacheDataEntries && entriesRes.cacheDataEntries.length > 0) {
                    allEntries.push(...entriesRes.cacheDataEntries);
                    skipCount += entriesRes.cacheDataEntries.length;
                    if (entriesRes.returnCount < pageSize) hasMore = false;
                } else {
                    hasMore = false;
                }
            }
            
            console.log(`[CDP] Trovate ${allEntries.length} entries totali nella cache ${v6Cache.cacheName}`);

            const sdksToFind = [
                'https://www.gstatic.com/firebasejs/10.8.0/firebase-app.js',
                'https://www.gstatic.com/firebasejs/10.8.0/firebase-firestore.js',
                'https://www.gstatic.com/firebasejs/10.8.0/firebase-auth.js'
            ];
            
            for (const sdk of sdksToFind) {
                sdkChecks.push(await checkSdk(sdk));
            }
            
            const localAssetsToFind = [
                '/login.html',
                '/dashboard.html',
                '/script.js',
                '/core/firebase-init.js',
                '/core/auth-service.js'
            ];
            
            const cacheKeysStrings = allEntries.map(e => {
                try {
                    return new URL(e.requestURL).pathname;
                } catch(err) {
                    return e.requestURL;
                }
            });
            
            for (const asset of localAssetsToFind) {
                localChecks[asset] = cacheKeysStrings.some(p => p.endsWith(asset));
            }
        }

        const missingSdks = sdkChecks.some(c => !c.found);
        const missingLocals = Object.values(localChecks).some(v => !v);
        const hasRejection = swLogs.some(l => l.toLowerCase().includes('fail') || l.toLowerCase().includes('error'));

        const isValid = v6Cache && isActivated && !missingSdks && !missingLocals && !hasRejection;

        console.log("\n=== REPORT DRY-RUN BASELINE 6.256 ===");
        console.log(`Versione Browser: ${(await browser.browser().version())}`);
        console.log(`URL Worker: ${swUrl || 'Nessuno'}`);
        console.log(`Stato install/activate: ${isActivated ? 'Attivato' : 'Non Attivato (o log mancanti)'}`);
        console.log(`Log SW completi:`);
        swLogs.forEach(l => console.log(`  - ${l}`));
        
        console.log(`Nome e cacheId: ${v6Cache ? v6Cache.cacheName + ' (ID: ' + v6Cache.cacheId + ')' : 'NON TROVATA'}`);
        console.log(`Numero totale entry: ${allEntries.length}`);
        
        console.log(`Risultato ricerche Firebase:`);
        sdkChecks.forEach(c => {
            console.log(`  - ${c.url}`);
            console.log(`    Trovato: ${c.found}`);
            if (c.found) {
                console.log(`    Status: ${c.status}`);
                console.log(`    ResponseType: ${c.responseType}`);
                console.log(`    Content-Type: ${c.contentType}`);
            }
        });
        
        console.log(`Asset locali verificati:`);
        for (const [asset, found] of Object.entries(localChecks)) {
            console.log(`  - ${asset}: ${found ? 'Trovato' : 'Mancante'}`);
        }
        
        if (isValid) {
            console.log("\n=== BASELINE 6.256: VALIDA ===");
        } else {
            console.log("\n=== BASELINE 6.256: NON VALIDA ===");
        }

        await browser.close();

    } catch (e) {
        console.error("Eccezione catturata:", e);
        if (browser) await browser.close();
        process.exit(1);
    }
})();
