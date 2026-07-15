# Recipe, Please!

## About The Project

Django web app that scrapes recipe data (title, ingredients, instructions, servings, prep/cook time) from any recipe website URL and displays it in a clean, ad-free format.

[recipe-please-demo](https://github.com/user-attachments/assets/e2dbe44c-d5c7-4250-b646-d581269bc2ea)

<!-- [Screencast from 2026-07-15 10-50-25.webm](https://github.com/user-attachments/assets/e2dbe44c-d5c7-4250-b646-d581269bc2ea) -->

Built to practice web scraping with Beautiful Soup. Rather than writing a custom parser per site, it uses regex-based pattern matching against common HTML class naming conventions. This works well for independent/personal recipe blogs, but not for larger corporate recipe sites (e.g. AllRecipes, Delish), which use more complex, non-standard markup.

> This project is no longer deployed and dependencies are outdated. Not intended to be run locally.

## Features

- **Pattern-based scraping** — pulls recipe data from most independent recipe sites via regex/class pattern matching (`getrecipe/services/recipe/scraper.py`), no per-site scraper needed
- **Data validation** — scraped data is parsed into a Pydantic model for type safety
- **Temporary caching** — scraped recipes are cached (Memcached) for 5 minutes and accessed by a short UUID, so no database is needed to store recipes
- **Graceful failure** — sites that can't be scraped redirect to a friendly "recipe not found" page instead of erroring out

## Built With

Django 5.1 · BeautifulSoup4 + lxml · Pydantic · Memcached · Gunicorn

## Potential Improvements

- **Reduce redundancy in scraping code** — `scrape_preparation_time`, `scrape_cook_time`, and `scrape_servings` share nearly identical logic (filter by class → check for digits → regex match). Could be consolidated into one generic function
- **Extract regex patterns** — patterns are currently hardcoded inline in each scraping function. Moving them to a constants/config module would make them easier to maintain, test, and extend as new site formats are added
- **Fix cache scope bug** — `index()` calls `cache.clear()` on every request, which wipes _all_ cached recipes for _all_ users, not just the current one. Should scope invalidation per-session or per-recipe instead
- **Replace bare exception handling with logging** — `main.py` catches all exceptions and `print()`s them; should use Python's `logging` module for real error visibility
<!-- print() just writes to stdout — it disappears once the process exits, has no severity level, no timestamp, and no way to route it anywhere. If this were deployed, you couldn't search deployed logs for "how often is scraping failing" or set up alerts. -->

## Potential Future Extensions

_This project is no longer being developed, but these are natural next steps it would need if it were revisited:_

- Automated tests — `pytest` and `pytest-django` are listed as dependencies, but no test files exist in the repo
- Rate-limiting — `django-ratelimit` is installed but never applied; the scrape endpoint has no protection against abuse
- Handling JS-rendered sites — scraping relies on `requests` + BeautifulSoup, so sites that render recipe content client-side aren't supported; a headless browser fallback (e.g. Playwright) could address this
- Persisting recipes to a database — recipes currently expire after 5 minutes with no way to save them
