from robot.api import TestData
from APNewsScraper import APNewsScraper
from config import SEARCH_PHRASE, NEW_CATEGORY, NUM_MONTHS

def get_test_cases():
    # Create a test suite
    suite = TestData(parent=None, source="")

    # Define a test case
    test_case = suite.tests.create(name="Scrape APNews")

    # Define the test steps
    test_case.keywords.create(name="Initialize APNewsScraper", args=[SEARCH_PHRASE, NEW_CATEGORY, NUM_MONTHS])
    test_case.keywords.create(name="Scrape")

    return suite

# from robot.api.deco import keyword
# from APNewsScraper import APNewsScraper
# from config import SEARCH_PHRASE, NEW_CATEGORY, NUM_MONTHS

# @keyword('Scrape APNews')
# def scrape_apnews():
#     search_phrase = SEARCH_PHRASE
#     news_category = NEW_CATEGORY
#     num_months = NUM_MONTHS
    
#     scraper = APNewsScraper(search_phrase, news_category, num_months)
#     scraper.scrape()
