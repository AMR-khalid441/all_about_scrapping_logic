from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    # Start listening for a specific response
    with page.expect_response(lambda res: "api/articles" in res.url and res.status == 200) as response_info:
        page.goto("https://pmc.ncbi.nlm.nih.gov/search/?term=mental+health")

    response = response_info.value  # the actual response object
    data = response.json()          # parse JSON body

    print(data)  # now you have JSON
    browser.close()
