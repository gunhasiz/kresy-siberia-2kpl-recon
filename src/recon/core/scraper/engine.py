import asyncio
from random import uniform
from re import Match, search
from typing import TypeVar, Type, List
from pydantic import BaseModel
from playwright.async_api import BrowserContext, Browser, Locator, Page, async_playwright

import recon.helpers.constants as constants
from recon.utils.api_client import ReconAPIClient
from recon.core.config import config
from recon.models.status import Status
from recon.models.record import Record
from recon.models.person import Person
from recon.models.personal_situation_outbreak import PersonalSituationOutbreak
from recon.models.deportation_and_repression import DeportationAndRepression
from recon.models.repatriation import Repatriation
from recon.models.occupation_period import OccupationPeriod
from recon.models.military_experience import MilitaryExperience
from recon.models.other_military_experience import OtherMilitaryExperience
from recon.models.sources import Source
from recon.models.related_galleries import RelatedGallery

T = TypeVar("T", bound=BaseModel)

class ScraperEngine:
    def __init__(self) -> None:
        self.base_url: str | None = config.BASE_URL
        self.total_pages: int = 1
        self.data_to_scrape: List[Status] = []
        self.records: List[Record] = []
        self.api_client: ReconAPIClient = ReconAPIClient()

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

                for page_num in range(1, self.total_pages + 1):
                    await self.scrape_page_content(page, page_num)

                print(
                    f"[*] Outer scraping complete. Total items collected: {len(self.data_to_scrape)}")

                for data in self.data_to_scrape:
                    print(
                        f"[*] Scraping page for item {data.entry_id}: {data.url}")
                    await self.scrape_record_page(page, data)

            except Exception as e:
                print(f"[!] An error occurred during scraping: {e}")
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

    async def scrape_page_content(self, page: Page, page_number: int) -> None:
        url = f"{self.base_url}/?pagenum={page_number}"

        print(f"[*] Scraping page {page_number}: {url}")

        await page.goto(url, wait_until="networkidle")
        await self.extract_table_data(page)

        delay: float = await self._get_random_delay()

        await asyncio.sleep(delay)

    async def extract_table_data(self, page: Page) -> None:
        await page.wait_for_selector("div[id^='gv-view-']", state="attached", timeout=30000)

        data_rows: Locator = page.locator("div[id^='gv_diy']")
        count: int = await data_rows.count()

        print(f"[*] Found {count} data rows on the page.")

        for i in range(count):
            # print(f"[*] Scraping row {i}")

            href: str | None = await data_rows.nth(i).locator("div").locator("a").get_attribute("href")
            match: Match[str] | None = search(r"(?<=\/entry\/)\d+", str(href))
            value: str = match.group(0) if match else ""

            if href:
                status: Status = Status(entry_id=value, url=href)
                self.data_to_scrape.append(status)
                self.api_client.send_status(status)

    async def scrape_record_page(self, page: Page, data: Status) -> None:
        record: Record = Record()

        if data.url:
            await page.goto(data.url, wait_until="networkidle")

        try:
            h4_locators: Locator = page.locator("div[id^='gv_diy'] h4")
            h4_count: int = await h4_locators.count()
            for i in range(h4_count):
                header_text: str = (await h4_locators.nth(i).inner_text()).strip()

                match header_text:
                    case constants.PERSONAL_DETAILS:
                        record.person = await self._get_single_table(page, header_text, Person)
                    case constants.PERSONAL_SITUATION_OUTBREAK:
                        record.personal_situation_outbreak = await self._get_single_table(page, header_text, PersonalSituationOutbreak)
                    case constants.DEPORTATIONS_AND_REPRESSIONS:
                        record.deportation_and_repression = await self._get_multi_table(page, header_text, DeportationAndRepression)
                    case constants.REPATRIATION:
                        record.repatration = await self._get_single_table(page, header_text, Repatriation)
                    case constants.OCCUPATION_PERIOD:
                        record.occupation_period = await self._get_single_table(page, header_text, OccupationPeriod)
                    case constants.MILITARY_EXPERIENCE:
                        record.military_experience = await self._get_multi_table(page, header_text, MilitaryExperience)
                    case constants.OTHER_MILITARY_EXPERIENCE:
                        record.other_military_experience = await self._get_single_table(page, header_text, OtherMilitaryExperience)
                    case constants.SOURCES:
                        record.sources = await self._get_ul_li_a_href(page, header_text, Source)
                    case constants.RELATED_GALLERIES:
                        record.related_galleries = await self._get_ul_li_a_href(page, header_text, RelatedGallery)

            data.status = "success"
            record.person.external_entry_id = data.entry_id if data.entry_id else "N/A"
            self.records.append(record)
            result = self.api_client.send_record(record)
            if result:
                self.api_client.send_status(data)
        except Exception as e:
            if config.DEBUG:
                print(f"[@] EXCEPTION {e=}, {type(e)=}")

            print(f"[!] Scraping failed for {data.url}")
            data.status = "failed"

    async def _get_ul_li_a_href(self, page: Page, header_text: str, model: Type[T]) -> List[T]:
        li: Locator = page.locator(
            f"//h4[contains(text(), '{header_text}')]/following::ul[position() =1]").locator("li a")
        a_count: int = await li.count()
        results: List[T] = []

        for j in range(a_count):
            label: str = await li.nth(j).inner_text()
            href: str | None = await li.nth(j).get_attribute("href")

            results.append(
                model(
                    summary=label,
                    url_text=str(href),
                    url=href
                )
            )

        return results

    async def _get_single_table(self, page: Page, header_text: str, model: Type[T]) -> T:
        table: Locator = page.locator(
            f"//h4[contains(text(), '{header_text}')]/following::table[position() = 1]")
        table_count: int = await table.count()

        if table_count == 0:
            return model()

        field_map: dict[str, str] = constants.MODEL_FIELD_MAP[model]
        data: dict = {}

        rows: Locator = table.locator("tbody tr")
        rows_count: int = await rows.count()

        for j in range(rows_count):
            tds: Locator = rows.nth(j).locator("td")
            tds_count: int = await tds.count()

            if tds_count == 2:
                label: str = (await tds.nth(0).inner_text()).strip().rstrip(':')
                value: str = (await tds.nth(1).inner_text()).strip()

                if label in field_map:
                    field_name: str = field_map[label]
                    data[field_name] = value
            elif tds_count == 3:
                label: str = (await tds.nth(1).inner_text()).strip().rstrip(':')
                value: str = (await tds.nth(2).inner_text()).strip()
                if label in field_map:
                    field_name: str = field_map[label]
                    data[field_name] = value

        return model(**data)

    async def _get_multi_table(self, page: Page, header_text: str, model: Type[T]) -> T:
        table: Locator = page.locator(
            f"//h4[contains(text(), '{header_text}')]/following::table[position() <= 2 and not(preceding::h4[1][not(contains(text(), '{header_text}'))])]")
        table_count: int = await table.count()

        field_map: dict = constants.MODEL_FIELD_MAP[model]

        main_data: dict = {}
        nested_data: dict = {}
        list_data: dict = {}

        nested_cfg: dict = field_map.get("_nested", {})
        list_cfg: dict = field_map.get("_list", {})

        simple_map: dict = {k: v for k, v in field_map.items() if not k.startswith("_")}

        if table_count == 2:
            for t in range(table_count):
                column_names: Locator = table.nth(t).locator("thead tr th")
                column_names_count: int = await column_names.count()
                rows: Locator = table.nth(t).locator("tbody tr")
                rows_count: int = await rows.count()

                pairs: list[tuple[str, str]] = []
                for j in range(rows_count):
                    tds: Locator = rows.nth(j).locator("td")
                    tds_count: int = await tds.count()

                    if tds_count == column_names_count:
                        for col in range(column_names_count):
                            label: str = (await column_names.nth(col).inner_text()).strip().strip(":")
                            value: str = (await tds.nth(col).inner_text()).strip()
                            if label:
                                pairs.append((label, value))
                    else:
                        label: str = (await tds.nth(0).inner_text()).strip().strip(":")
                        value: str = (await tds.nth(1).inner_text()).strip()
                        if label:
                            pairs.append((label, value))

                for label, value in pairs:
                    if label in simple_map:
                        main_data[simple_map[label]] = value

                if tds_count == column_names_count:
                    for nested_key, nested_def in nested_cfg.items():
                        seq: list[tuple] = nested_def.get("map_sequence", [])
                        if seq:
                            if nested_key not in nested_data:
                                nested_data[nested_key] = []
                            nested_data[nested_key].append(self._map_by_sequence(
                                pairs, seq))

                    for list_key, list_def in list_cfg.items():
                        seq: list[tuple] = list_def.get("map_sequence", [])
                        if seq:
                            if list_key not in list_data:
                                list_data[list_key] = []
                            list_data[list_key].append(
                                self._map_by_sequence(pairs, seq))

        main_data.update(nested_data)
        main_data.update(list_data)
        return model(**main_data)

    def _map_by_sequence(self, pairs: list[tuple[str, str]], sequence: list[tuple[str, str]],) -> dict:
        result: dict = {}
        seq_index: int = 0

        for label, value in pairs:
            while seq_index < len(sequence):
                expected_label, field_name = sequence[seq_index]
                if label == expected_label:
                    result[field_name] = value
                    seq_index += 1
                    break
                seq_index += 1

        return result

    async def _get_random_delay(self) -> float:
        return uniform(config.DELAY_MIN, config.DELAY_MAX)

async def main() -> None:
    engine = ScraperEngine()
    await engine.run()