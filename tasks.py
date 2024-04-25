from APNewsScraper import APNewsScraper

def Scrape_APNews():
    search_phrase = "${SEARCH_PHRASE}"
    news_category = "${NEW_CATEGORY}"
    num_months = ${NUM_MONTHS}
    
    scraper = APNewsScraper(search_phrase, news_category, num_months)
    scraper.scrape()
