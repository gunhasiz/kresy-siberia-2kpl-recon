import asyncio
from random import uniform
from re import search
from typing import List
from playwright.async_api import BrowserContext, Browser, Locator, Page, async_playwright

import recon.helpers.constants as constants
from recon.core.config import config
from recon.models.status import Status


class ScraperEngine:
    def __init__(self) -> None:
        self.base_url: str | None = config.BASE_URL
        self.total_pages: int = 1
        self.data_to_scrape: List[Status] = []

    async def run(self) -> None:
        async with async_playwright() as p:
            print(
                f"[*] Setting up browser with user agent: {config.USER_AGENT}")
            browser: Browser = await p.chromium.launch(headless=True)
            print(f"[*] Browser launched successfully.")
            print(f"[*] Running browser context....")
            context: BrowserContext = await browser.new_context(user_agent=config.USER_AGENT)
            page: Page = await context.new_page()

            try:
                first_url: str = f"{self.base_url}/?pagenum=1"
                await page.goto(first_url, wait_until="networkidle")
                await self.get_total_pages(page)

                # TODO: Remove hardcoded page limit after testing
                for page_num in range(1, 1+1):  # self.total_pages + 1):
                    await self.scrape_page_content(page, page_num)

                print(
                    f"[*] Outer scraping complete. Total items collected: {len(self.data_to_scrape)}")

                for data in self.data_to_scrape:
                    print(
                        f"[*] Scraping page for item {data.entry_id}: {data.url}")
                    await self.scrape_record_page(page, data)

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
                self.data_to_scrape.append(Status(entry_id=value, url=href))

    async def scrape_record_page(self, page: Page, data: Status):
        if data.url:
            await page.goto(data.url, wait_until="networkidle")

        try:
            h4_locators = page.locator("div[id^='gv_diy'] h4")
            h4_count = await h4_locators.count()
            for i in range(h4_count):
                header_text = (await h4_locators.nth(i).inner_text()).strip()
                print(f"\n--- Section: {header_text} ---")

                match header_text:
                    case constants.PERSONAL_DETAILS:
                        table: Locator = page.locator(
                            f"//h4[contains(text(), '{header_text}')]/following::table[position() = 1]")
                        table_count: int = await table.count()

                        if table_count > 0:
                            rows: Locator = table.locator("tbody tr")
                            rows_count: int = await rows.count()

                            for j in range(rows_count):
                                tds: Locator = rows.nth(j).locator("td")
                                tds_count: int = await tds.count()

                                if tds_count == 2:
                                    label: str = (await tds.nth(0).inner_text()).strip().rstrip(':')
                                    value: str = (await tds.nth(1).inner_text()).strip()

                                    if label:
                                        print(f"[*] {label}: {value}")
                                elif tds_count == 3:
                                    entry_id: str = (await tds.nth(0).inner_text()).strip()
                                    if entry_id:
                                        print(f"[*] Entry ID: {entry_id}")
                                    label: str = (await tds.nth(1).inner_text()).strip().rstrip(':')
                                    value: str = (await tds.nth(2).inner_text()).strip()

                                    if label:
                                        print(f"[*] {label}: {value}")
                    case constants.PERSONAL_SITUATION_OUTBREAK:
                        table: Locator = page.locator(
                            f"//h4[contains(text(), '{header_text}')]/following::table[position() = 1]")
                        table_count: int = await table.count()

                        if table_count > 0:
                            rows: Locator = table.locator("tbody tr")
                            rows_count: int = await rows.count()

                            for j in range(rows_count):
                                tds: Locator = rows.nth(j).locator("td")
                                tds_count: int = await tds.count()

                                if tds_count == 2:
                                    label: str = (await tds.nth(0).inner_text()).strip().rstrip(':')
                                    value: str = (await tds.nth(1).inner_text()).strip()

                                    if label:
                                        print(f"[*] {label}: {value}")
                    case constants.DEPORTATIONS_AND_REPRESSIONS:
                        table: Locator = page.locator(
                            f"//h4[contains(text(), '{header_text}')]/following::table[position() <= 2]")
                        table_count: int = await table.count()

                        if table_count == 2:
                            for t in range(table_count):
                                column_names: Locator = table.nth(t).locator("thead tr th")
                                column_names_count: int = await column_names.count()
                                rows: Locator = table.nth(t).locator("tbody tr")
                                rows_count: int = await rows.count()

                                for j in range(rows_count):
                                    tds: Locator = rows.nth(j).locator("td")
                                    tds_count: int = await tds.count()

                                    if tds_count == column_names_count:
                                        for column_index in range(column_names_count):
                                            label: str = await column_names.nth(column_index).inner_text()
                                            value: str = (await tds.nth(column_index).inner_text()).strip()

                                            if label:
                                                print(f"[*] {label}: {value}")
                                    else:
                                        label: str = await tds.nth(0).inner_text()
                                        value: str = await tds.nth(1).inner_text()
                                        if label:
                                                print(f"[*] {label}: {value}")
                    case constants.REPATRIATION:
                        table: Locator = page.locator(
                            f"//h4[contains(text(), '{header_text}')]/following::table[position() = 1]")
                        table_count: int = await table.count()

                        if table_count > 0:
                            rows: Locator = table.locator("tbody tr")
                            rows_count: int = await rows.count()

                            for j in range(rows_count):
                                tds: Locator = rows.nth(j).locator("td")
                                tds_count: int = await tds.count()

                                if tds_count == 2:
                                    label: str = (await tds.nth(0).inner_text()).strip().rstrip(':')
                                    value: str = (await tds.nth(1).inner_text()).strip()

                                    if label:
                                        print(f"[*] {label}: {value}")
                    case constants.OCCUPATION_PERIOD:
                        table: Locator = page.locator(
                            f"//h4[contains(text(), '{header_text}')]/following::table[position() = 1]")
                        table_count: int = await table.count()

                        if table_count > 0:
                            rows: Locator = table.locator("tbody tr")
                            rows_count: int = await rows.count()

                            for j in range(rows_count):
                                tds: Locator = rows.nth(j).locator("td")
                                tds_count: int = await tds.count()

                                if tds_count == 2:
                                    label: str = (await tds.nth(0).inner_text()).strip().rstrip(':')
                                    value: str = (await tds.nth(1).inner_text()).strip()

                                    if label:
                                        print(f"[*] {label}: {value}")
                    case constants.MILITARY_EXPERIENCE:
                        table: Locator = page.locator(
                            f"//h4[contains(text(), '{header_text}')]/following::table[position() <= 2]")
                        table_count: int = await table.count()

                        if table_count == 2:
                            for t in range(table_count):
                                column_names: Locator = table.nth(t).locator("thead tr th")
                                column_names_count: int = await column_names.count()
                                rows: Locator = table.nth(t).locator("tbody tr")
                                rows_count: int = await rows.count()

                                for j in range(rows_count):
                                    tds: Locator = rows.nth(j).locator("td")
                                    tds_count: int = await tds.count()

                                    if tds_count == column_names_count:
                                        for column_index in range(column_names_count):
                                            label: str = await column_names.nth(column_index).inner_text()
                                            value: str = (await tds.nth(column_index).inner_text()).strip()

                                            if label:
                                                print(f"[*] {label}: {value}")
                                    else:
                                        label: str = await tds.nth(0).inner_text()
                                        value: str = await tds.nth(1).inner_text()
                                        if label:
                                                print(f"[*] {label}: {value}")
                    case constants.OTHER_MILITARY_EXPERIENCE:
                        table: Locator = page.locator(
                            f"//h4[contains(text(), '{header_text}')]/following::table[position() = 1]")
                        table_count: int = await table.count()

                        if table_count > 0:
                            rows: Locator = table.locator("tbody tr")
                            rows_count: int = await rows.count()

                            for j in range(rows_count):
                                tds: Locator = rows.nth(j).locator("td")
                                tds_count: int = await tds.count()

                                if tds_count == 2:
                                    label: str = (await tds.nth(0).inner_text()).strip().rstrip(':')
                                    value: str = (await tds.nth(1).inner_text()).strip()

                                    if label:
                                        print(f"[*] {label}: {value}")
                    case constants.SOURCES:
                        li: Locator = page.locator(f"//h4[contains(text(), '{header_text}')]/following::ul[position() =1]").locator("li a")
                        a_count: int = await li.count()
                        
                        for j in range(a_count):
                            label: str = await li.nth(j).inner_text()
                            href: str | None = await li.nth(j).get_attribute("href")
                            
                            print(f"[*] {label}: {href}")
                    case constants.RELATED_GALLERIES:
                        li: Locator = page.locator(f"//h4[contains(text(), '{header_text}')]/following::ul[position() =1]").locator("li a")
                        a_count: int = await li.count()
                        
                        for j in range(a_count):
                            label: str = await li.nth(j).inner_text()
                            href: str | None = await li.nth(j).get_attribute("href")
                            
                            print(f"[*] {label}: {href}")
        except:
            print(f"[!] Scraping failed for {data.url}")
            data.status = "failed"

    async def get_random_delay(self):
        return uniform(config.DELAY_MIN, config.DELAY_MAX)


async def main():
    engine = ScraperEngine()
    await engine.run()
