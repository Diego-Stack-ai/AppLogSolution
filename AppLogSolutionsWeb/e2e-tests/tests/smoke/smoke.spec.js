const { test, expect } = require('@playwright/test');

test('Browser Smoke Test - Caricamento Pubblico', async ({ page }) => {
    // 11. Prima di eseguire la suite completa crea un test pubblico minimale che:
    // - avvii Chromium;
    // - apra https://log-solutions-sviluppo.web.app;
    // - verifichi il caricamento della pagina;
    // - non richieda login;
    // - chiuda correttamente il browser.
    
    const response = await page.goto('/');
    expect(response.status()).toBe(200);
    
    // Verifichiamo che il corpo della pagina o l'app sia caricata
    await expect(page.locator('body')).toBeVisible();
    
    // Il browser verrà chiuso automaticamente dal context di Playwright alla fine del test.
});
