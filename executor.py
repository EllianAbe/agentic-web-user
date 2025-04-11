from playwright.async_api import async_playwright
import asyncio


async def execute_steps(steps):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        result = ""

        for step in steps:
            attr = getattr(page, step["action"])

            if callable(attr):
                await attr(**step["args"])

            await asyncio.sleep(1)

        result = await page.title()

        await browser.close()
        return result
