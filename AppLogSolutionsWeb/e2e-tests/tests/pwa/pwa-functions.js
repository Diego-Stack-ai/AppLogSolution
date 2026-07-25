const { test, expect, chromium } = require('@playwright/test');

async function getSWState(page) {
    return await page.evaluate(async () => {
        const reg = await navigator.serviceWorker.getRegistration();
        if (!reg) return null;
        if (reg.active) return reg.active.state;
        if (reg.waiting) return reg.waiting.state;
        if (reg.installing) return reg.installing.state;
        return null;
    });
}

async function waitForSWActivated(page) {
    return await page.evaluate(async () => {
        return new Promise(resolve => {
            navigator.serviceWorker.getRegistration().then(reg => {
                if (reg && reg.active && reg.active.state === 'activated') {
                    resolve(true);
                } else {
                    navigator.serviceWorker.addEventListener('controllerchange', () => {
                        resolve(true);
                    });
                }
            });
        });
    });
}

async function getCacheInfo(page) {
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
}
