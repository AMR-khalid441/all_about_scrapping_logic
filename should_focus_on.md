| Topic                       | Your level | Notes                                                           |
| --------------------------- | ---------- | --------------------------------------------------------------- |
| **Playwright basics**       | 90%        | Launching browser, opening pages, headless vs visible           |
| **Navigating pages**        | 85%        | `page.goto`, `wait_until` options like `domcontentloaded`       |
| **Waiting for elements**    | 80%        | `wait_for_selector` — enough for most dynamic pages             |
| **Querying elements**       | 90%        | `query_selector_all`, understanding tag/class selectors         |
| **Grabbing content**        | 85%        | `.inner_text()`, `.inner_html()` → you can get full HTML for BS |
| **Parsing HTML**            | 80%        | BeautifulSoup usage, `find`, `find_all`, extracting attributes  |
| **Handling multiple pages** | 75%        | Pagination loop, polite delays, stopping when no results        |
| **Printing/debugging**      | 85%        | Checking first few articles, screenshots                        |





| Topic                                        | Why it matters                                        | How hard it is |
| -------------------------------------------- | ----------------------------------------------------- | -------------- |
| **`wait_for_response` / JSON APIs**          | Can bypass HTML scraping, faster & cleaner            | Medium         |
| **Advanced CSS selectors / XPaths**          | Grab elements that don’t have clean classes           | Easy-medium    |
| **Error handling / retries**                 | For timeouts, failed requests, or missing elements    | Easy           |
| **Dealing with SPAs & lazy-loading content** | Infinite scroll, pagination with JS                   | Medium         |
| **Rate limiting / politeness**               | Avoid bans, throttling, random delays                 | Easy           |
| **Headless anti-bot measures**               | Some sites block bots → rotating user agents, stealth | Hard           |
