| Method                                    | What it does                                             | When to use it                                                    |
| ----------------------------------------- | -------------------------------------------------------- | ----------------------------------------------------------------- |
| `wait_for_load_state("load")`             | Waits for the page to fully load (HTML + resources)      | When you want the entire page loaded, but can be slow             |
| `wait_for_load_state("domcontentloaded")` | Waits until the DOM is parsed, but some JS may still run | Faster, often enough for scraping                                 |
| `wait_for_load_state("networkidle")`      | Waits until **no network requests** for 500ms            | Good for SPAs, but some pages poll continuously → can hang        |
| `wait_for_timeout(ms)`                    | Just waits a fixed number of milliseconds                | Not ideal, only for small delays                                  |
| `wait_for_event("response")`              | Waits for a network response matching a URL or pattern   | Useful if you want **XHR/JSON requests** instead of scraping HTML |
