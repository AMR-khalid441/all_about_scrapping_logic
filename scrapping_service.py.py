from playwright.sync_api import sync_playwright
from datetime import datetime
import uuid
import json
import time
import os
from pathlib import Path


# =========================================================
# STEP 1 — Crawl PMC Search Pages (Multi-Page Safe)
# =========================================================
def crawl_pmc_article_urls(search_url, max_articles=50):
    """
    Crawl PMC search results across multiple pages
    and collect article URLs.
    """
    all_urls = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        page_number = 1

        while len(all_urls) < max_articles:
            print(f"\n--- Visiting search page {page_number} ---")

            page.goto(f"{search_url}&page={page_number}",
                      wait_until="networkidle",
                      timeout=30000)

            page.wait_for_selector("div.docsum-wrap", timeout=20000)

            results = page.query_selector_all("div.docsum-wrap")

            if not results:
                print("No more results found.")
                break

            for result in results:
                link_element = result.query_selector("a.docsum-link")

                if link_element:
                    href = link_element.get_attribute("href")

                    if href:
                        if href.startswith("/"):
                            full_url = f"https://www.ncbi.nlm.nih.gov{href}"
                        else:
                            full_url = href

                        if full_url not in all_urls:
                            all_urls.append(full_url)
                            print(f"Collected {len(all_urls)}: {full_url}")

                        if len(all_urls) >= max_articles:
                            break

            page_number += 1
            time.sleep(1)

        browser.close()

    print(f"\nTotal URLs collected: {len(all_urls)}")
    return all_urls[:max_articles]


# =========================================================
# STEP 2 — Build JSON Structure
# =========================================================
def build_paper_json(doc_title, source_url, sections_data):
    return {
        "doc_id": str(uuid.uuid4()),
        "doc_title": doc_title,
        "source_url": source_url,
        "created_at": datetime.today().strftime("%Y-%m-%d"),
        "sections": sections_data
    }


# =========================================================
# STEP 3 — Scrape Only 2 Sections (FULL TEXT)
# =========================================================
def scrape_pmc_sections(page, url, target_sections=["Results", "Discussion"]):
    """
    Scrape Results & Discussion.
    Each section is stored as ONE full accumulated text block.
    """

    page.goto(url, wait_until="domcontentloaded", timeout=30000)

    try:
        doc_title = page.locator("h1").inner_text().strip()
    except:
        doc_title = "Unknown Article Title"

    sections_data = []

    for section_name in target_sections:

        h2 = page.locator("h2.pmc_sec_title").filter(has_text=section_name)

        if h2.count() == 0:
            print(f"Warning: {section_name} not found.")
            continue

        section_element = h2.locator("xpath=..")
        paragraphs = section_element.locator("p")

        full_text_parts = []

        for i in range(paragraphs.count()):
            text = paragraphs.nth(i).inner_text().strip()
            if text:
                full_text_parts.append(text)

        if full_text_parts:
            sections_data.append({
                "title": section_name,
                "order": len(sections_data),
                "text": "\n\n".join(full_text_parts)
            })

    if not sections_data:
        print(f"No valid sections found for {url}")
        return None

    return build_paper_json(doc_title, url, sections_data)


# =========================================================
# STEP 4 — Save Each Article Separately
# =========================================================
def save_json(data, folder="pmc_articles"):
    os.makedirs(folder, exist_ok=True)

    filename = os.path.join(folder, f"{data['doc_id']}.json")

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"Saved: {filename}")


# =========================================================
# MAIN EXECUTION
# =========================================================
def main():

    search_url = "https://pmc.ncbi.nlm.nih.gov/search/?term=mental+health"
    max_articles = 50
    output_folder = "pmc_articles"

    Path(output_folder).mkdir(exist_ok=True)

    print("=" * 60)
    print("STEP 1: Collecting Article URLs")
    print("=" * 60)

    article_urls = crawl_pmc_article_urls(search_url, max_articles)

    if not article_urls:
        print("No articles found.")
        return

    print("\n" + "=" * 60)
    print("STEP 2: Scraping Articles")
    print("=" * 60)

    successful = 0
    failed = 0

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        for idx, url in enumerate(article_urls, 1):
            print(f"\n[{idx}/{len(article_urls)}] Scraping: {url}")

            try:
                paper_json = scrape_pmc_sections(page, url)

                if paper_json:
                    save_json(paper_json, output_folder)
                    successful += 1
                else:
                    failed += 1

                time.sleep(1.5)  # be polite

            except Exception as e:
                print(f"Error: {e}")
                failed += 1

        browser.close()

    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Collected URLs: {len(article_urls)}")
    print(f"Successfully scraped: {successful}")
    print(f"Failed: {failed}")
    print(f"Saved in folder: {output_folder}/")
    print("=" * 60)


if __name__ == "__main__":
    main()
