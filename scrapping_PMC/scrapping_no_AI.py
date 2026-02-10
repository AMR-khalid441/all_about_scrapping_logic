from playwright.sync_api import sync_playwright , Playwright
from bs4 import BeautifulSoup

def scrapping_html(url):
    with sync_playwright() as P:
        browser = P.chromium.launch(headless=False , timeout=20000)
        page = browser.new_page()
        page.goto(url=url , wait_until="networkidle")
        selector = "div.docsum-wrap"
        page.wait_for_selector(selector=selector , timeout=20000)
                # Get FULL rendered HTML after JS execution
        html = page.content()

        browser.close()
        return html
def soup_function(htlm):
    soup = BeautifulSoup.get(htlm).find("")
    pass










if __name__ =="__main__":
    pass