const fs = require('fs');
const path = require('path');
const envPath = path.join(__dirname, '.env');
if (fs.existsSync(envPath)) {
    const envFile = fs.readFileSync(envPath, 'utf8');
    envFile.split('\n').forEach(line => {
        const match = line.match(/^([^=]+)=(.*)$/);
        if (match) process.env[match[1].trim()] = match[2].trim();
    });
}
const EMAIL = process.env.E2E_TEST_EMAIL;
const PASSWORD = process.env.E2E_TEST_PASSWORD;
console.log('--- Pre-flight Environment Check ---');
if (!EMAIL || !PASSWORD) {
    console.log('⚠️ ATTENZIONE: Credenziali E2E_TEST_EMAIL o E2E_TEST_PASSWORD mancanti.');
    console.log('I test autenticati (auth, dashboard) verranno saltati (NON ESEGUITO).');
    console.log('I test pubblici (PWA, caching, smoke) verranno eseguiti regolarmente.');
} else {
    console.log('✅ Credenziali di test configurate.');
}
console.log('------------------------------------');
