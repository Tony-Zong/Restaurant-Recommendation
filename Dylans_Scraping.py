
from bs4 import BeautifulSoup
import requests
import re

# Overall Goals:
# Scrape store hours , number of reviews , address , amenities and more

#TEST_URL = https://www.yelp.com/biz/the-purple-pig-chicago?osq=Restaurants

def get(url):
    '''
    gets html from url
    '''
    response = requests.get(url)
    return response.text

def get_soup(html):
    soup = BeautifulSoup(html, 'html5lib')
    return soup

def phone(soup):
    '''
    '''
    #phone number
    tags = soup.find_all('p', class_="css-1h7ysrc")
    return tags[-2].text

def address(soup):
    '''
    '''
    #address
    tags = soup.find_all('p', class_="css-1ccncw")
    return tags[0].text

def amenities(soup):
    '''
    '''
    tags = soup.find_all('span', class_="css-1h7ysrc")
    return tags

    ###????? yo this is kinda weird









