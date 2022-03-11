# Import libraries
from bs4 import BeautifulSoup
import csv
import requests


# Produce list of zipcodes from CSV

def get_zipcodes(csv_file):
    '''
    Collects zipcodes from a csv file of zipcodes in the CHicago area.
    '''
    zipcodes = []
    with open(csv_file, 'r') as f:
        for row in csv.reader(f):
            zipcodes.append(row[0])
            
    return zipcodes
    
# Search Yelp for every restaurant in every zipcode
# base_search_url = 'https://www.yelp.com/search?cflt=restaurants&find_loc=Chicago%2C+IL+'


def urls(starting_url, zipcodes):
    '''
    Collects urls from Yelp for restaurants in Chicago zipcodes.
    '''
    restaurant_urls = set()
    base_search_url = 'https://www.yelp.com/search?cflt=restaurants&find_loc=Chicago%2C+IL+'
    for zipcode in zipcodes:
        search_url = base_search_url + zipcode[0]
        start_page = 0
        reached_last_page = False

        while(not reached_last_page):
            req = requests.get(search_url + '&start=' + str(start_page))
            soup = BeautifulSoup(req.content, 'html.parser')
            biz_tags = soup.find_all('div', class_ = 'businessName__09f24__EYSZE display--inline-block__09f24__fEDiJ border-color--default__09f24__NPAKY')

            if biz_tags:
                for biz_tag in biz_tags:
                    url = biz_tag.find('a')['href']
                    # the restaurant urls are all relative ones
                    if 'http' not in url:
                        url = url.split('?')[0]
                        restaurant_urls.add(url)
            else:
                reached_last_page = True

    return restaurant_urls


# Write to CSV
def csv(restaurant_urls):
    '''
    Writes a csv for the set of restaurant URLs.
    '''
    with open('restaurant_urls.csv', 'w') as file:
        write = csv.writer(file)
        for restaurant_url in restaurant_urls:
            write.writerow([restaurant_url])
