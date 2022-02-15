

from bs4 import BeautifulSoup
import requests
import re

# need a function that returns soup given a url.

def scrape_name_rating_price_tag(soup):
    '''
    '''

    # restaurant name
    name = soup.find_all('h1', class_="css-1x9iesk")[0].text
    # number of reviews
    tags = soup.find_all('span', class_="css-1yy09vp")
    num_review_str = tags[0].text
    num_review = re.search('^[0-9]+', num_review_str)[0]
    # hours
    time = tags[-1].text
    rest_tags = set()
    for i in range(1, len(tags)-1):
        rest_tags.add(tags[i].find_all('a', class_= "css-1422juy")[0].text)
    # rating
    rating_tag = soup.find_all('div', class_="css-i-stars__09f24__foihJ i-stars--large-4__09f24__jGrzl border-color--default__09f24__NPAKY overflow--hidden__09f24___ayzG")
    rating_str = re.findall('"([\w\s]+) star rating', str(soup))[0]
    # price
    price = -1
    price_tags = soup.find_all('span', class_="css-oyv5ea")
    for price_tag in price_tags:
        if '$' in price_tag.text:
            price = len(price_tag.text)
