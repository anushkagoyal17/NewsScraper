*** Settings ***
Library    APNewsScraper.py

*** Tasks ***
Scrape APNews
    [Documentation]    Scrapes APNews for given search phrase, news category, and number of months
    Initialize APNewsScraper    ${SEARCH_PHRASE}    ${NEW_CATEGORY}    ${NUM_MONTHS}
    Scrape
