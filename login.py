from playwright.async_api import async_playwright

USERNAME = "your-linkedin-email"
PASSWORD = "your-linkedin-password"

async def login():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)  # Headless=False so you can manually solve captchas
        context = await browser.new_context()
        page = await context.new_page()

        await page.goto("https://www.linkedin.com/login")

        await page.fill('input#username', USERNAME)
        await page.fill('input#password', PASSWORD)
        await page.click('button[type="submit"]')

        # Optional wait in case of CAPTCHA or 2FA (you can increase if needed)
        await page.wait_for_timeout(5000)

        await context.storage_state(path="linkedin_state.json")
        print("✅ Session saved to linkedin_state.json")

        await browser.close()
