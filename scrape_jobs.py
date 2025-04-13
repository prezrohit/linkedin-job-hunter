import asyncio
from json.decoder import JSONDecodeError

from playwright.async_api import async_playwright
from send_mail import *  # Assume it works with async context if needed
from login import login  # login() should also be async if it interacts with browser

PARENT_URL = "https://www.linkedin.com"
TARGET_URL = PARENT_URL + "/jobs/search/?f_TPR=r3600&refresh=true"
AUTH_RETRY_COUNT = 3


def get_qualified_link(url):
    url = url[:url.index('?')] if '?' in url else url
    return PARENT_URL + url


async def check_auth(browser, page, count):
    if count == 0:
        await browser.close()
        print("❌ Auth failed after multiple retries.")
        exit()

    me_menu = await page.query_selector("div.global-nav__me")
    if not me_menu:
        print(f"🚫 Not authenticated — Logging in... (attempt {AUTH_RETRY_COUNT - count + 1})")
        await browser.close()
        await login()  # this should be async
        await main(count - 1)  # retry from top after login
        return False
    return True


async def main(auth_retry_count=AUTH_RETRY_COUNT):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)

        try:
            context = await browser.new_context(storage_state="linkedin_state.json")

        except JSONDecodeError:
            print("❌ Storage state JSON is invalid or corrupted. Re-running login.")
            await login()  # your login method that saves a new valid json
            context = await browser.new_context(storage_state="linkedin_state.json")

        page = await context.new_page()

        await page.goto(TARGET_URL, timeout=60000)

        is_authenticated = await check_auth(browser, page, auth_retry_count)
        if not is_authenticated:
            return  # Already handled in check_auth

        jobs_list_parent_selector = await page.query_selector("div.scaffold-layout__list")
        jobs_list_selector_div = (await jobs_list_parent_selector.query_selector_all(":scope > *"))[1]

        scroll_container = jobs_list_selector_div
        last_count = 0
        max_scrolls = 20

        for _ in range(max_scrolls):
            job_list_items = await jobs_list_selector_div.query_selector_all("ul > li")
            current_count = len(job_list_items)

            if current_count == last_count:
                break
            last_count = current_count

            await page.evaluate("(el) => el.scrollBy(0, 500)", scroll_container)
            await asyncio.sleep(0.7)

        jobs_list_selector = await jobs_list_selector_div.query_selector("ul")
        jobs_result = ""

        if jobs_list_selector:
            job_list_root = await jobs_list_selector.query_selector_all(":scope > li")
            print(f"\n🧠 Total jobs loaded in DOM: {len(job_list_root)}\n")

            for li_root in job_list_root:
                job_title = await li_root.query_selector("strong")
                company_name = await li_root.query_selector("div.artdeco-entity-lockup__subtitle.ember-view")
                link = await li_root.query_selector("a")

                if job_title and company_name and link:
                    title_text = await job_title.inner_text()
                    company_text = (await company_name.inner_text()).strip()
                    link_href = await link.get_attribute("href")

                    jobs_result += f"{title_text} - [{company_text}]\n"
                    jobs_result += get_qualified_link(link_href) + "\n\n"

        await browser.close()

        print("Sending jobs to email...")
        send_email(jobs_result)

        print("Jobs sent to email!")
