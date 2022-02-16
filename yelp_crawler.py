# Import libraries
from bs4 import BeautifulSoup
import csv
import requests


# Produce list of zipcodes from CSV
zipcodes = []
with open('cook_zips.csv', newline = '') as f:
    for row in csv.reader(f):
        zipcodes.append(row[0])


# Search Yelp for every restaurant in every zipcode
restaurant_urls = set()
base_search_url = 'https://www.yelp.com/search?cflt=restaurants&find_loc=Chicago%2C+IL+'

for zipcode in zipcodes:
    search_url = base_search_url + zipcode
    start_page = 0
    reached_last_page = False

    while(not reached_last_page):
        req = requests.get(search_url + '&start=' + str(start_page))
        print(req.content)
        soup = BeautifulSoup(req.content, 'html.parser')
        biz_tags = soup.find_all('div', class_ = 'businessName__09f24__EYSZE display--inline-block__09f24__fEDiJ border-color--default__09f24__NPAKY')
        if biz_tags:
            for biz_tag in biz_tags:
                restaurant_urls.add(biz_tag.find('a')['href'])
        else:
            reached_last_page = True


# Write to CSV
with open('restaurant_urls.csv', 'w') as file:
    write = csv.writer(file)
    for restaurant_url in restaurant_urls:
        write.writerow([restaurant_url])
