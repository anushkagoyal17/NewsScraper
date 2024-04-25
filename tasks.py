from APNewsScraper import APNewsScraper

def Scrape_APNews():
    search_phrase = "delhi"
    news_category = "test"
    num_months = 1
    
    scraper = APNewsScraper(search_phrase, news_category, num_months)
    scraper.scrape()
