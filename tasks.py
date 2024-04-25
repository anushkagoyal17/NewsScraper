*** Settings ***
Library    APNewsScraper.py
Library    Collections

*** Variables ***
${SEARCH_PHRASE}    delhi
${NEW_CATEGORY}    test
${NUM_MONTHS}    1

*** Tasks ***
Scrape APNews
    [Documentation]    Scrapes APNews for given search phrase, news category, and number of months
    Initialize APNewsScraper    ${SEARCH_PHRASE}    ${NEW_CATEGORY}    ${NUM_MONTHS}
    Scrape

*** Keywords ***
Scrape
    ${scraper}=    Initialize APNewsScraper    ${SEARCH_PHRASE}    ${NEW_CATEGORY}    ${NUM_MONTHS}
    ${result}=    Scrape    ${scraper}
    Log    ${result}
