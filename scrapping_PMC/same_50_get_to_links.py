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
        all_texts = []
        all_links = []  # store article links

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
                html = el.inner_html()   # full HTML
                text = el.inner_text()   # visible text
                link_el = el.query_selector("a.docsum-link")  # find <a> tag
                link = link_el.get_attribute("href") if link_el else None
                if link and not link.startswith("http"):
                    link = "https://www.ncbi.nlm.nih.gov" + link  # full URL

                all_htmls.append(html)
                all_texts.append(text)
                all_links.append(link)

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

        # Print first 3 articles info
        for i in range(min(3, len(all_htmls))):
            print(f"\n--- Article {i+1} HTML ---\n{all_htmls[i]}\n")
            print(f"--- Article {i+1} Visible Text ---\n{all_texts[i]}\n")
            print(f"--- Article {i+1} Link ---\n{all_links[i]}\n")

        print(f"\nTotal articles collected: {len(all_htmls)}")
        return all_htmls, all_texts, all_links


if __name__ == "__main__":
    url = "https://www.ncbi.nlm.nih.gov/pmc/?term=mental+health"
    articles_html, articles_text, articles_links = crawl_pmc_articles(url, max_articles=50)

    print(f"\nFirst article link: {articles_links[0]}")
