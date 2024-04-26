*** Settings ***
Library  robot.api.deco

*** Tasks ***
Scrape APNews
    [Documentation]  Scrape APNews with fixed arguments
    [Arguments]  search_phrase=business  num_months=3
    Scrape APNews
