from playwright.sync_api import sync_playwright
# Example: Hacker News

# All <a> story links are pre-rendered in the HTML

# wait_for_selector for first element is enough

def scrape_static(url: str, selector: str):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url, wait_until="domcontentloaded")

        # Wait for at least one element to exist
        page.wait_for_selector(selector)

        # Grab all repeated elements safely
        elements = page.query_selector_all(selector)
        texts = [el.inner_text() for el in elements]

        browser.close()
#         return texts
# 2️⃣ Slightly dynamic / “waiting for first guarantees most others”

# Example: Blog with preloaded first section, remaining injected quickly

# Waiting for first section often guarantees most repeated elements
from playwright.sync_api import sync_playwright
import time

def scrape_slightly_dynamic(url: str, selector: str, wait_extra: float = 2):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url, wait_until="domcontentloaded")

        # Wait for the first element
        page.wait_for_selector(selector)

        # Give a small extra delay for remaining duplicates
        time.sleep(wait_extra)

        # Grab all elements
        elements = page.query_selector_all(selector)
        texts = [el.inner_text() for el in elements]

        browser.close()
        return texts


# Example usage
if __name__ == "__main__":
    url = "https://example-blog.com"
    selector = "h1.my-class"
    data = scrape_slightly_dynamic(url, selector)
    print(f"Found {len(data)} elements")


#very advanced 
from playwright.sync_api import sync_playwright

def scrape_dynamic(url: str, selector: str, min_count: int = 10, timeout: int = 15000):
    """
    Waits until at least min_count elements exist in the DOM.
    Suitable for SPAs or JS-injected content.
    """
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url, wait_until="domcontentloaded")

        # Wait until at least one element exists
        page.wait_for_selector(selector, timeout=timeout)

        # Wait until minimum count exists
        if min_count:
            page.wait_for_function(
                f"() => document.querySelectorAll('{selector}').length >= {min_count}",
                timeout=timeout
            )

        # Grab all elements
        elements = page.query_selector_all(selector)
        texts = [el.inner_text() for el in elements]

        browser.close()
        return texts


# Example usage
if __name__ == "__main__":
    url = "https://example-spa.com"
    selector = "h1.my-class"
    data = scrape_dynamic(url, selector, min_count=10)
    print(f"Found {len(data)} elements")
"**********************************************************************************************"

from playwright.sync_api import sync_playwright
import time

def scrape_slightly_dynamic(url: str, selector: str, wait_extra: float = 2):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url, wait_until="domcontentloaded")

        # Wait for the first element
        page.wait_for_selector(selector)

        # Give a small extra delay for remaining duplicates
        time.sleep(wait_extra)

        # Grab all elements
        elements = page.query_selector_all(selector)
        texts = [el.inner_text() for el in elements]

        browser.close()
        return texts


# Example usage
if __name__ == "__main__":
    url = "https://example-blog.com"
    selector = "h1.my-class"
    data = scrape_slightly_dynamic(url, selector)
    print(f"Found {len(data)} elements")


# Example usage
if __name__ == "__main__":
    url = "https://news.ycombinator.com/"
    selector = "a.storylink"
    data = scrape_static(url, selector)
    print(f"Found {len(data)} elements")

