import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(base_url='https://log-solutions-sviluppo.web.app')
        
        async def on_sw(sw):
            print(f"[SW Worker Attached] {sw.url}")
            sw.on('console', lambda msg: print(f"[SW LOG] {msg.text}"))
            
        context.on('serviceworker', on_sw)
        
        page = await context.new_page()
        page.on('console', lambda msg: print(f"[PAGE LOG] {msg.text}"))
        
        print("Going to /")
        await page.goto('/')
        
        print("Waiting 10s...")
        await page.wait_for_timeout(10000)
        
        state = await page.evaluate('''async () => {
            const reg = await navigator.serviceWorker.getRegistration();
            if (!reg) return "NO_REG";
            if (reg.active) return "ACTIVE:" + reg.active.state;
            if (reg.waiting) return "WAITING:" + reg.waiting.state;
            if (reg.installing) return "INSTALLING:" + reg.installing.state;
            return "UNKNOWN";
        }''')
        print("SW STATE:", state)
        
        await browser.close()

asyncio.run(main())
