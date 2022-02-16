# Import libraries
from bs4 import BeautifulSoup
import csv
import requests

# Produce list of zipcodes from CSV
zipcodess = []
with open('cook_zips.csv', newline = '') as f:
    for row in csv.reader(f):
        zipcodes.append(row[0])

# Search Yelp for every restaurant in every zipcode
restaurant_urls = []
base_search_url = 'https://www.yelp.com/search?cflt=restaurants&find_loc=Chicago%2C+IL+'

for zipcode in zipcodes:
    search_url = base_search_url + zipcode
    start_page = 0
    reached_last_page = False

    while(not reached_last_page):
        # <div class=" businessName__09f24__EYSZE display--inline-block__09f24__fEDiJ border-color--default__09f24__NPAKY"