*** Settings ***
Library  robot.api.deco

*** Task ***
Scrape APNews  search_phrase=business  num_months=3
