import os
import openpyxl
from datetime import datetime

SEARCH_PHRASE = os.getenv('SEARCH_PHRASE', default='default_search_phrase')
NEW_CATEGORY = os.getenv('NEW_CATEGORY', default='default_category')
NUM_MONTHS = int(os.getenv('NUM_MONTHS', default='6'))

LAST_N_DAYS = NUM_MONTHS * 30

URL = 'https://apnews.com/'
URL = URL[:-1] if URL[-1] == '/' else URL

OUTPUT_COLUMNS = ['News URL', 'Title', 'Date', 'Description', 'Image Filename', 'Search Phrase Count', 'Money Present']
OUTPUT_FILE = f'{SEARCH_PHRASE}_news_data_{datetime.today().date()}.xlsx'
OUTPUT_SHEETNAME = f'{SEARCH_PHRASE}_news_details'

COMMENTS_COLUMNS = ['News URL', 'Comment']
COMMENTS_SHEETNAME = 'comments'
if not os.path.exists(OUTPUT_FILE):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = OUTPUT_SHEETNAME
    ws.append(OUTPUT_COLUMNS)
    ws_comments = wb.create_sheet(title=COMMENTS_SHEETNAME)
    ws_comments.append(COMMENTS_COLUMNS)
    wb.save(OUTPUT_FILE)

IMAGES_FOLDER = 'Images'
if not os.path.exists(IMAGES_FOLDER):
    os.makedirs(IMAGES_FOLDER)

LOG_FILEPATH = 'app.log'
