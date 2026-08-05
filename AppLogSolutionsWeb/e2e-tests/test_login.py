import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto('https://log-solutions-cantiere.web.app/login.html')
        await page.wait_for_selector('#email')
        await page.fill('#email', 'boschetto.diego@gmail.com')
        await page.fill('#password', 'Password1')
        await page.click('#loginButton')
        
        try:
            await page.wait_for_url('**/dashboard.html', timeout=5000)
            print("LOGIN SUCCESS: boschetto.diego@gmail.com")
        except:
            print("LOGIN FAILED")
            
        await browser.close()

asyncio.run(main())
