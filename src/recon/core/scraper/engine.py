import asyncio
from random import uniform
from re import search
from playwright.async_api import BrowserContext, Browser, Locator, Page, async_playwright

from recon.core.config import config

class ScraperEngine:
    def __init__(self) -> None:
        self.base_url: str | None = config.BASE_URL
        self.total_pages: int  = 1
        self.data_to_scrape: dict = {}

    async def run(self) -> None:
        async with async_playwright() as p:
            browser: Browser = await p.chromium.launch(headless=True)
            context: BrowserContext = await browser.new_context(user_agent=config.USER_AGENT)
            page: Page = await context.new_page()

            try:
                first_url: str = f"{self.base_url}/?pagenum=1"
                await page.goto(first_url, wait_until="networkidle")
                await self.get_total_pages(page)

                for page_num in range(1, self.total_pages + 1):
                    await self.scrape_page_content(page, page_num)
                
                print(f"[*] Outer scraping complete. Total items collected: {len(self.data_to_scrape)}")
                
                for key, url in self.data_to_scrape.items():
                    print(f"[*] Scraping page for item {key}: {url}")

            finally:
                await browser.close()

    async def get_total_pages(self, page: Page) -> None:
        try:
            print("[*] Checking total page count...")

            pagination_selector = "ul.page-numbers"
            await page.wait_for_selector(pagination_selector, timeout=10000)
            
            page_items: Locator = page.locator(f"{pagination_selector} li")
            count: int = await page_items.count()
            
            if count >= 2:
                last_page_text: str = await page_items.nth(count - 2).inner_text()
                self.total_pages = int(last_page_text.strip())

                print(f"[*] Found total pages: {self.total_pages}")

        except Exception as e:
            print(f"[!] Could not determine total pages: {e}")

    async def scrape_page_content(self, page: Page, page_number: int):
        url = f"{self.base_url}/?pagenum={page_number}"
        
        print(f"[*] Scraping page {page_number}: {url}")

        await page.goto(url, wait_until="networkidle")
        await self.extract_table_data(page)

        delay: float = await self.get_random_delay()

        await asyncio.sleep(delay)

    async def extract_table_data(self, page: Page):
        await page.wait_for_selector("div[id^='gv-view-']", state="attached", timeout=30000)

        data_rows: Locator = page.locator("div[id^='gv_diy']")
        count: int = await data_rows.count()

        print(f"[*] Found {count} data rows on the page.")

        for i in range(count):
            print(f"[*] Scraping row {i}")

            href: str | None = await data_rows.nth(i).locator("div").locator("a").get_attribute("href")
            value: str = search(r"(?<=\/entry\/)\d+", str(href)).group(0)

            if href:
                self.data_to_scrape[value] = href

    async def scrape_record_page(self, page: Page, url: str):
        await page.goto(url, wait_until="networkidle")

    async def get_random_delay(self):
        return uniform(config.DELAY_MIN, config.DELAY_MAX)

async def main():
    engine = ScraperEngine()
    await engine.run()

if __name__ == "__main__":
    asyncio.run(main())