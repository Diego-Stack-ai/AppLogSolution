const { test, expect } = require('@playwright/test');

test.describe('Test 9 & 10 - Asset Critico Inesistente e Continuità', () => {
    test('Installazione rigettata su asset critico mancante e continuità offline', async ({ page, context }) => {
        const logs = [];
        page.on('console', msg => logs.push(msg.text()));

        // 1. Navigazione dopo il deploy della versione difettosa (Test 9)
        await page.goto('https://log-solutions-sviluppo.web.app/');
        
        // Aspettiamo l'installazione fallita
        await page.waitForTimeout(5000);

        // Verifica dei log di errore critico e rigetto
        const isAssetFailed = logs.some(log => log.includes('Fallita installazione asset critico') || log.includes('script-INVENTATO.js') || log.includes('status 404'));
        
        expect(isAssetFailed).toBeTruthy();
        
        // 2. Continuità e Offline (Test 10)
        await context.setOffline(true);
        
        // Ricaricamento della pagina, dovrebbe servire la versione dalla cache baseline
        await page.reload();
        
        await page.waitForTimeout(3000);
        
        // Verifica presenza elemento critico per accertare che l'app funziona ancora
        const titleVisible = await page.isVisible('body'); // controllo basilare UI
        expect(titleVisible).toBeTruthy();

        // Controllo caches
        const cacheKeys = await page.evaluate(async () => {
            return await window.caches.keys();
        });
        
        // Deve esserci la vecchia cache v6 attiva
        const hasV6Cache = cacheKeys.some(c => c.includes('log-solution-v6.'));
        expect(hasV6Cache).toBeTruthy();
    });
});
