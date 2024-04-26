from robot.api.deco import keyword
from robocorp.tasks import task
from APNewsScraper import APNewsScraper
from config import SEARCH_PHRASE, NEW_CATEGORY, NUM_MONTHS

@task
# def task():
#     print("fingers crossed")
#     return "fingers crossed"
# @keyword("Scrape APNews")
def scrape_apnews():
    """Scrapes news data from APNews based on provided search parameters.

    Args:
        search_phrase (str, optional): The keyword or phrase to search for in news articles. Defaults to SEARCH_PHRASE from config.py.
        news_category (str, optional): The news category to filter results by (optional). Defaults to NEW_CATEGORY from config.py.
        num_months (int, optional): The number of months to consider for searching recent news (defaults to 1 month). Defaults to NUM_MONTHS from config.py.
    """

    scraper = APNewsScraper()
    try:
        scraper.scrape()
    except Exception as e:
        print(f"An error occurred during scraping: {e}")

