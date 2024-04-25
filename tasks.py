from APNewsScraper import APNewsScraper
from config import SEARCH_PHRASE, NEW_CATEGORY, NUM_MONTHS

def Scrape_APNews():
    search_phrase = SEARCH_PHRASE
    news_category = NEW_CATEGORY
    num_months = NUM_MONTHS
    
    scraper = APNewsScraper(search_phrase, news_category, num_months)
    scraper.scrape()
