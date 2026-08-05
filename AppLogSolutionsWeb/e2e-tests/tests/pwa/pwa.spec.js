const { test, expect, chromium } = require('@playwright/test');

async function getSWState(page) {
    try {
        return await page.evaluate(async () => {
            const reg = await navigator.serviceWorker.getRegistration();
            if (!reg) return null;
            if (reg.active) return reg.active.state;
            if (reg.waiting) return reg.waiting.state;
            if (reg.installing) return reg.installing.state;
            return null;
        });
    } catch (e) {
        if (e.message.includes('Execution context was destroyed') || e.message.includes('Target closed')) {
            return 'reloading';
        }
        throw e;
    }
}

async function getCacheInfo(page) {
    try {
        return await page.evaluate(async () => {
            const keys = await caches.keys();
            const info = {};
            for (const k of keys) {
                const cache = await caches.open(k);
                const reqs = await cache.keys();
                info[k] = reqs.map(r => r.url);
            }
            return info;
        });
    } catch (e) {
        return {};
    }
}

test.describe.serial('Collaudo PWA Pubblico (Nessuna Credenziale Richiesta)', () => {

    let userDataDir;

    test.beforeAll(async () => {
        const fs = require('fs');
        const path = require('path');
        userDataDir = path.join(__dirname, '../../.playwright_pwa_profile');
        if (fs.existsSync(userDataDir)) {
            fs.rmSync(userDataDir, { recursive: true, force: true });
        }
    });

    test('Test 1 - Aggiornamento Normale', async () => {
        const context = await chromium.launchPersistentContext(userDataDir, { baseURL: 'https://log-solutions-cantiere.web.app' });
        const page = await context.pages()[0] || await context.newPage();
        
        let swLogs = [];
        page.on('console', msg => {
            if (msg.text().includes('[SW]')) swLogs.push(msg.text());
        });

        await page.goto('/');
        
        await expect(async () => {
            const state = await getSWState(page);
            expect(state).toBe('activated');
        }).toPass({ timeout: 15000 });

        const cachesInfo = await getCacheInfo(page);
        expect(Object.keys(cachesInfo).some(k => k.includes('log-solution-v'))).toBeTruthy();
        
        await context.close();
    });

    test('Test 5 - Installazione senza Leaflet', async () => {
        const fs = require('fs');
        fs.rmSync(userDataDir, { recursive: true, force: true });

        const context = await chromium.launchPersistentContext(userDataDir, { baseURL: 'https://log-solutions-cantiere.web.app' });
        await context.route('**/*leaflet*', route => route.abort());
        const page = await context.pages()[0] || await context.newPage();
        
        let swLogs = [];
        page.on('console', msg => {
            if (msg.text().includes('[SW]') || msg.text().includes('Errore cache opzionale')) swLogs.push(msg.text());
        });

        await page.goto('/');
        
        await expect(async () => {
            const state = await getSWState(page);
            expect(state).toBe('activated');
        }).toPass({ timeout: 15000 });

        const failedLog = swLogs.find(l => l.includes('Errore cache opzionale') && l.includes('leaflet'));
        expect(failedLog).toBeDefined();

        await context.close();
    });

    test('Test 6 - Installazione senza Fonts', async () => {
        const fs = require('fs');
        fs.rmSync(userDataDir, { recursive: true, force: true });

        const context = await chromium.launchPersistentContext(userDataDir, { baseURL: 'https://log-solutions-cantiere.web.app' });
        await context.route('**/*fonts.googleapis.com*', route => route.abort());
        const page = await context.pages()[0] || await context.newPage();
        
        let swLogs = [];
        page.on('console', msg => {
            if (msg.text().includes('[SW]') || msg.text().includes('Errore cache opzionale')) swLogs.push(msg.text());
        });

        await page.goto('/');
        
        await expect(async () => {
            const state = await getSWState(page);
            expect(state).toBe('activated');
        }).toPass({ timeout: 15000 });

        const failedLog = swLogs.find(l => l.includes('Errore cache opzionale') && l.includes('fonts.googleapis.com'));
        expect(failedLog).toBeDefined();

        await context.close();
    });

    test('Test 7 - Prima installazione senza Firebase CDN', async () => {
        const fs = require('fs');
        fs.rmSync(userDataDir, { recursive: true, force: true });

        const context = await chromium.launchPersistentContext(userDataDir, { baseURL: 'https://log-solutions-cantiere.web.app' });
        await context.route('**/*www.gstatic.com/firebasejs/10.8.0*', route => route.abort());
        const page = await context.pages()[0] || await context.newPage();
        
        let swLogs = [];
        page.on('console', msg => {
            if (msg.text().includes('[SW]') || msg.text().includes('Installazione rigettata')) swLogs.push(msg.text());
        });

        await page.goto('/');
        
        await expect(async () => {
            const logFound = swLogs.some(l => l.includes('Installazione rigettata') && l.includes('Fallback Firebase assente'));
            expect(logFound).toBeTruthy();
        }).toPass({ timeout: 15000 });

        const state = await getSWState(page);
        expect(state).not.toBe('activated');

        const cachesInfo = await getCacheInfo(page);
        expect(Object.keys(cachesInfo).some(k => k.includes('log-solution-v'))).toBeFalsy();

        await context.close();
    });

});
