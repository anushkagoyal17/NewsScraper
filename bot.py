import requests, openpyxl, os, time, re, logging
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from config import URL, OUTPUT_FILE, SEARCH_PHRASE, NEW_CATEGORY, NUM_MONTHS, LAST_N_DAYS, \
    OUTPUT_SHEETNAME, COMMENTS_SHEETNAME, IMAGES_FOLDER, LOG_FILEPATH

logging.basicConfig(filename=LOG_FILEPATH, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()
logger.removeHandler(logging.StreamHandler())

options = Options()
options.add_argument('--headless')

class APNewsScraper:
    def __init__(self, search_phrase, news_category, num_months):
        self.base_url = URL
        self.search_phrase = search_phrase
        self.news_category = news_category
        self.num_months = num_months

    def get_selenium_response(self, url):
        ''' Get the page source '''
        driver = webdriver.Firefox(options=options)
        driver.get(url)
        time.sleep(3)
        try:
            button = driver.find_element(By.ID, "bx-close-inside-2475153")
            button.click()
            time.sleep(2)
        except:
            # print("No pop-up appeared!")
            pass
        
        response = driver.page_source
        driver.quit()
        return response

    def check_date_criteria(self, news_date):
        ''' Check if the given date meets criteria '''
        current_date = datetime.today().date()
        from_date = (current_date - timedelta(LAST_N_DAYS)).strftime("%Y-%m-%d")
        flag = datetime.strptime(from_date, "%Y-%m-%d").date() <= news_date <= current_date
        return flag

    def scrape(self):
        ''' Fetch complete data '''
        logging.info("Scraping started...")
        search_url = f"{self.base_url}/search?q={(self.search_phrase).replace(' ', '+')}"
        response = requests.get(search_url)
        # response = self.get_selenium_response(search_url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            # news_links = soup.find_all('a', class_='headline')
            pagination = int(soup.find('div', class_='Pagination-pageCounts').text.split(' ')[-1])
            logging.info("Pages: %s", pagination)
            for page in range(1, pagination+1):
                print(page)
                for link in soup.findAll('div', class_='PageList-items-item'):
                    try:
                        news_url = link.find('div', class_='PagePromo-media').a['href']
                        print('News URL: ', news_url)
                        result = self.extract_news(news_url)
                        if result[1] == OUTPUT_SHEETNAME: 
                            self.save_to_excel(result[0], OUTPUT_SHEETNAME)
                        elif result[1] == COMMENTS_SHEETNAME:
                            self.save_to_excel(result[0], COMMENTS_SHEETNAME)
                    except:
                        pass
                        # print('--------ISSUE---------')
                        # breakpoint()
                search_url = f"{self.base_url}/search?q={(self.search_phrase).replace(' ', '+')}&p={page}"
                response = requests.get(search_url)
                soup = BeautifulSoup(response.content, 'html.parser')

        else:
            self.save_to_excel([news_url, "Failed to fetch data from the website."], COMMENTS_SHEETNAME)
            logging.warning(f"{news_url} -> Failed to fetch data from the website.")

    def extract_news(self, news_url):
        ''' Fetch News Details '''
        # breakpoint()
        try:
            # try:
            response = self.get_selenium_response(news_url)
            soup = BeautifulSoup(response, 'html.parser')
            # except:
            #     response = requests.get(news_url)
            #     soup = BeautifulSoup(response.content, 'html.parser')
            try:
                try:
                    date_str = soup.find('div', class_='Page-datePublished').text
                    news_date = datetime.strptime(date_str[date_str.find(',')+1:].strip(), '%B %d, %Y').date()
                except AttributeError:
                    date_str = soup.find('div', class_='Page-dateModified').text
                    news_date = datetime.strptime(date_str[date_str.find(',')+1:].strip(), '%B %d, %Y').date()
            except:
                logging.warning(f"Exception Case-> {news_url}\nIssue: Date not fetched!")
                return [news_url, 'Date not fetched!'], COMMENTS_SHEETNAME

            if self.check_date_criteria(news_date):
                title = soup.find('title').text.split('|')[0].strip()
                try:
                    description = soup.find('div', class_='VideoPage-pageSubHeading').text.strip()
                except:
                    description = soup.find('div', class_='RichTextStoryBody').text.strip()
                try:
                    try:
                        image_url = soup.find('div', class_='CarouselSlide-media').find('img')['src']
                    except:
                        # Video Thumbnail
                        image_element = soup.find('div', class_='jw-preview jw-reset')['style']
                        image_url = image_element[image_element.find('(')+2:image_element.find(')')-1]
                except:
                    image_url = soup.find('figure', class_='Figure').find('img')['src']
                # print('Done-> ', news_url) 
                news_details = [
                    news_url, title, news_date, description, self.download_image(image_url, title), 
                    title.lower().count(self.search_phrase.lower()) + description.lower().count(self.search_phrase.lower()),
                    self.check_money(title, description)
                ]
                return news_details, OUTPUT_SHEETNAME

            return [news_url, f'Old News (Dated): {news_date}'], COMMENTS_SHEETNAME
        except Exception as e:
            # breakpoint()
            # pass
            logging.warning(f"Exception Case-> {news_url}\nIssue:{e}")
            return [news_url, e], COMMENTS_SHEETNAME

    def save_to_excel(self, row, sheet):
        ''' Save the extracted data to excel '''
        wb = openpyxl.load_workbook(OUTPUT_FILE)
        ws = wb[sheet]
        ws.append(row)
        wb.save(OUTPUT_FILE)


    def download_image(self, image_url, title):
        ''' Get image from the web '''
        # try:
        # Downloading image
        image_filename = f"image_{title[:25]}.jpg"
        image_path = os.path.join(IMAGES_FOLDER, image_filename)
        with open(image_path, 'wb') as f:
            image_response = requests.get(image_url)
            f.write(image_response.content)
            # print(f"Image downloaded: {image_filename}")
        return image_url
        # except:
        #     breakpoint()

    def check_money(self, title, description):
        ''' Check if any amount of money is present in the text'''
        pattern_found = False
        pattern = r'\$?\s*((\d{1,3}(,\d{3})*)|(\d+))(\.\d{1,2})?\s*(dollars|USD)?'
        title_match = re.search(pattern, title)
        description_match = re.search(pattern, description)
        
        if title_match or description_match:
            pattern_found = True
        return pattern_found

# Execution begins here
if __name__ == "__main__":
    search_phrase = SEARCH_PHRASE
    news_category = NEW_CATEGORY
    num_months = NUM_MONTHS
    
    scraper = APNewsScraper(search_phrase, news_category, num_months)
    scraper.scrape()

# scraper = APNewsScraper('delhi', '', 1)
# scraper.extract_news('https://apnews.com/article/india-ukraine-foreign-minister-russia-modi-zelenskyy-putin-9fb1954fc84debfa42eb46b4672900a8')
