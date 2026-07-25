const { test, chromium, expect } = require('@playwright/test');
const path = require('path');

test.describe.serial('Test 8 - Orchestrazione Fallback CDN', () => {
    
    const userDataDir = path.join(__dirname, '../../.profiles/pwa-update');
    
    test('8.1 Installazione Baseline', async () => {
        const browser = await chromium.launchPersistentContext(userDataDir, { headless: false });
        const page = await browser.newPage();
        
        await page.goto('https://log-solutions-sviluppo.web.app/');
        await page.waitForTimeout(5000); // Attesa installazione SW v6.xxx
        
        // Verifica worker e Firebase assets
        const swStatus = await page.evaluate(async () => {
            const reg = await navigator.serviceWorker.ready;
            return reg.active ? reg.active.state : null;
        });
        expect(swStatus).toBe('activated');
        
        await browser.close(); // Chiudi mantenendo il profilo intatto
    });

    test('8.2 Verifica Fallback post-aggiornamento', async () => {
        // Da avviare MANUALMENTE dopo prepare-test-8.py (bump su hosting)
        const browser = await chromium.launchPersistentContext(userDataDir, { headless: false });
        
        // Blocco effettivo tramite CDP (Chrome DevTools Protocol)
        await browser.route('**/*www.gstatic.com/firebasejs/10.8.0*/**', route => route.abort());
        
        const page = await browser.newPage();
        
        const logs = [];
        page.on('console', msg => logs.push(msg.text()));

        await page.goto('https://log-solutions-sviluppo.web.app/');
        await page.waitForTimeout(6000);
        
        const hasFallbackLog = logs.some(l => l.includes('recuperato dalla cache precedente'));
        expect(hasFallbackLog).toBeTruthy();
        
        await browser.close();
    });
});
