from playwright.sync_api import sync_playwright
import time
from bs4 import BeautifulSoup
def crawl_pmc_articles(url, max_articles=50):
    with sync_playwright() as P:
        browser = P.chromium.launch(headless=False)
        page = browser.new_page()

        articles_collected = 0
        page_number = 1
        all_htmls = []

        while articles_collected < max_articles:
            print(f"\n--- Visiting page {page_number} ---")
            page.goto(url + f"&page={page_number}", wait_until="domcontentloaded")

            selector = "div.docsum-wrap"  # parent div of each article
            try:
                page.wait_for_selector(selector, timeout=20000)
            except:
                print("No more results found or timeout")
                break

            elements = page.query_selector_all(selector)
            for el in elements:
                html = el.inner_html()  # grab full HTML of the section
                all_htmls.append(html)
                articles_collected += 1
                print(f"Collected article {articles_collected}")
                if articles_collected >= max_articles:
                    break

            if not elements:
                print("No more articles on this page")
                break

            page_number += 1
            time.sleep(1)

        page.screenshot(path="example_last_page.png")
        browser.close()

        # Print first article fully to check
        for i, html in enumerate(all_htmls[:3], 1):  # print first 3 for brevity
            print(f"\n--- Article {i} HTML ---\n{html}\n")

        print(f"\nTotal articles collected: {len(all_htmls)}")
        return all_htmls


if __name__ == "__main__":
    url = "https://pmc.ncbi.nlm.nih.gov/search/?term=mental+health"
    articles_html = crawl_pmc_articles(url, max_articles=50)
    soup = BeautifulSoup(articles_html[1], "html.parser")  # create soup object
    title = soup.find("a", class_="docsum-link")
    print(title)

   
