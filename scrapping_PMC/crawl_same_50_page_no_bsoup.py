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
        all_texts = []  # store visible text

        while articles_collected < max_articles:
            print(f"\n--- Visiting page {page_number} ---")
            page.goto(url + f"&page={page_number}", wait_until="networkidle")

            selector = "div.docsum-wrap"  # parent div of each article
            try:
                page.wait_for_selector(selector, timeout=20000)
            except:
                print("No more results found or timeout")
                break

            elements = page.query_selector_all(selector)
            for el in elements:
                html = el.inner_html()       # full HTML
                text = el.inner_text()       # visible text only
                all_htmls.append(html)
                all_texts.append(text)
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

        # Print first 3 articles (HTML + visible text) to check
        for i in range(min(3, len(all_htmls))):
            print(f"\n--- Article {i+1} HTML ---\n{all_htmls[i]}\n")
            print(f"--- Article {i+1} Visible Text ---\n{all_texts[i]}\n")

        print(f"\nTotal articles collected: {len(all_htmls)}")
        return all_htmls, all_texts


if __name__ == "__main__":
    url = "https://pmc.ncbi.nlm.nih.gov/search/?term=mental+health"
    articles_html, articles_text = crawl_pmc_articles(url, max_articles=50)

    # Example: parse first article's title using BeautifulSoup on HTML
    soup = BeautifulSoup(articles_html[0], "html.parser")
    title = soup.find("a", class_="docsum-link")
    print(f"\nTitle from HTML: {title.get_text(strip=True) if title else 'Not found'}")

    # Example: access the visible text directly
    print(f"\nFirst article visible text:\n{articles_text[0]}")
