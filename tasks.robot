*** Settings ***
Library    APNewsScraper

*** Variables ***
${SEARCH_PHRASE}    ${search_phrase}
${NEW_CATEGORY}    ${news_category}
${NUM_MONTHS}    ${num_months}

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
