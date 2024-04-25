*** Settings ***
Library    tasks.py
Library    Collections

*** Variables ***
${SEARCH_PHRASE}    delhi
${NEW_CATEGORY}    test
${NUM_MONTHS}    1

*** Tasks ***
Scrape APNews
    [Documentation]    Scrapes APNews for given search phrase, news category, and number of months
    Scrape APNews
