const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

(async () => {
    console.log("=== INIZIO TEST 10: CONTINUITÀ OFFLINE ===");
    
    const userDataDir = path.join(__dirname, '../.playwright_test10_profile_v2');
    if (fs.existsSync(userDataDir)) {
        fs.rmSync(userDataDir, { recursive: true, force: true });
    }
    
    const context = await chromium.launchPersistentContext(userDataDir, { headless: true });
    const page = await context.newPage();
    
    console.log("[Fase 1] Caricamento app originale (6.257) e installazione cache...");
    await page.goto('https://log-solutions-sviluppo.web.app/login.html');
    
    console.log("   -> Attesa 20 secondi per completamento pre-caching...");
    await page.waitForTimeout(20000); 

    await page.reload();
    await page.waitForTimeout(5000);
    
    console.log("[Fase 2] Intercettazione traffico per simulare aggiornamento difettoso...");
    await context.route('https://log-solutions-sviluppo.web.app/sw.js', async route => {
        const response = await route.fetch();
        let body = await response.text();
        body = body.replace(/const CACHE_NAME = "[^"]+";/, 'const CACHE_NAME = "log-solution-v6.258-ROTTA";');
        body = body.replace('./script.js', './script-INVENTATO.js');
        console.log("   -> [Intercept] Servito sw.js fasullo (6.258-ROTTA) con asset inesistente!");
        route.fulfill({
            response,
            body,
            headers: { ...response.headers(), 'content-type': 'application/javascript' }
        });
    });

    console.log("[Fase 3] Ricaricamento pagina per innescare l'aggiornamento SW (che fallirà)...");
    await page.reload();
    await page.waitForTimeout(8000); // tempo per far fallire il nuovo SW (404)

    console.log("[Fase 4] Simulazione assenza di rete (OFFLINE)...");
    await context.setOffline(true);
    
    console.log("[Fase 5] Ricaricamento pagina in stato OFFLINE...");
    let success = false;
    try {
        await page.reload({ waitUntil: 'domcontentloaded', timeout: 10000 });
        const title = await page.title();
        console.log(`   -> Pagina caricata con successo in OFFLINE! Titolo: "${title}"`);
        success = true;
    } catch (e) {
        console.log("   -> ERRORE: La pagina non si è caricata offline!", e.message);
    }

    if (success) {
        console.log("=== ESITO TEST 10: PASS ✅ ===");
        console.log("L'aggiornamento difettoso è stato ignorato e la vecchia cache (6.257) ha mantenuto l'app online!");
    } else {
        console.log("=== ESITO TEST 10: FAIL ❌ ===");
    }
    
    await context.close();
})();
