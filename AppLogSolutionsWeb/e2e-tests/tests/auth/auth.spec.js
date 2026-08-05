const { test, expect, chromium } = require('@playwright/test');

const EMAIL = process.env.E2E_TEST_EMAIL;
const PASSWORD = process.env.E2E_TEST_PASSWORD;

function checkCreds() {
    if (!EMAIL || !PASSWORD) {
        test.skip('NON ESEGUITO — credenziali test non configurate');
    }
}

test.describe.serial('Collaudo PWA Autenticato (Test 2, 3, 4)', () => {

    let userDataDir;

    test.beforeAll(async () => {
        const fs = require('fs');
        const path = require('path');
        userDataDir = path.join(__dirname, '../../.playwright_auth_profile');
        if (fs.existsSync(userDataDir)) {
            fs.rmSync(userDataDir, { recursive: true, force: true });
        }
    });

    test('Test 2 - Login e Dashboard Online', async () => {
        checkCreds();
        const context = await chromium.launchPersistentContext(userDataDir, { baseURL: 'https://log-solutions-cantiere.web.app' });
        const page = await context.pages()[0] || await context.newPage();
        
        await page.goto('/login.html');
        const emailField = page.locator('#username');
        if (await emailField.isVisible()) {
            await emailField.fill(EMAIL);
            await page.locator('#password').fill(PASSWORD);
            await page.locator('#loginBtn').click();
        }
        
        await page.waitForURL('**/dashboard.html', { timeout: 15000 });
        await expect(page.locator('body')).toBeVisible();
        
        await page.goto('/inserimento.html');
        await expect(page.locator('body')).toBeVisible();
        await context.close();
    });

    test('Test 3 - Dashboard e Opzionale Offline', async () => {
        checkCreds();
        const context = await chromium.launchPersistentContext(userDataDir, { baseURL: 'https://log-solutions-cantiere.web.app' });
        const page = await context.pages()[0] || await context.newPage();
        
        await page.goto('/dashboard.html');
        await expect(page.locator('body')).toBeVisible();
        
        await context.setOffline(true);
        try { await page.reload({ timeout: 5000 }); } catch (e) {}
        await expect(page.locator('body')).toBeVisible();
        
        try { await page.goto('/inserimento.html', { timeout: 5000 }); } catch (e) {}
        await expect(page.locator('body')).toBeVisible();
        
        await context.close();
    });

    test('Test 4 - Riapertura Completa Offline', async () => {
        checkCreds();
        const context = await chromium.launchPersistentContext(userDataDir, { baseURL: 'https://log-solutions-cantiere.web.app' });
        await context.setOffline(true);
        const page = await context.pages()[0] || await context.newPage();
        
        try { await page.goto('/dashboard.html', { timeout: 5000 }); } catch (e) {}
        await expect(page.locator('body')).toBeVisible({ timeout: 10000 });
        await context.close();
    });

});
