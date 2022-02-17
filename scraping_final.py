import scraping_all as sa
import csv
import bs4
from bs4 import BeautifulSoup
import csv
import requests

def scrape(csv_filename):
    '''
    '''
    
    current_id = 1
    all_rest = {}
    csv_read = open(csv_filename, 'r')
    reader = csv.reader(csv_read)
    for url in reader:
        complete_url = 'https://www.yelp.com' + url[0]
        r = requests.get(complete_url)
        html_doc = r.text.encode('utf-8')
        soup = bs4.BeautifulSoup(html_doc, "html5lib")
        rest_name, rest_dict = sa.get_info(soup)
        rest_id = current_id
        current_id += 1
        all_rest[rest_name] = all_rest.get(rest_name, {})
        all_rest[rest_name] = rest_dict
    
    return all_rest
