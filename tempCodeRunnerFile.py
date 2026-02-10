from playwright.sync_api import sync_playwright

def scrapping_unothirized(url):
    with sync_playwright() as P:
        browser = P.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto(url, wait_until="domcontentloaded")

        # Correct selector for PMC search results
        selector = "div.docsum-wrap"  # usually each article summary is in div.docsum-wrap
        page.wait_for_selector(selector, timeout=50000)

        # Grab all repeated elements safely
        elements = page.query_selector_all(selector)
        texts = [el.inner_text() for el in elements]

        for i, t in enumerate(texts, 1):
            print(f"--- Article {i} ---")
            print(t, "\n")  # print first 500 chars to check

        page.screenshot(path="example.png")
        browser.close()


if __name__ == "__main__":
    url = "https://pmc.ncbi.nlm.nih.gov/search/?term=mental+health"
    scrapping_unothirized(url)
