import scraping_all as sa
import csv
import bs4
from bs4 import BeautifulSoup
import csv
import requests
import time
import random
import pickle
import pickle5 as p

def scrape(csv_filename, all_rest = {}):
    '''
    '''
    
    #current_id = 1
    csv_read = open(csv_filename, 'r')
    reader = csv.reader(csv_read)
    for url in reader:
        complete_url = 'https://www.yelp.com' + url[0]
        time.sleep(random.randint(1, 3))

        proxies = {'https': '149.19.224.49:3128'}

        r = requests.get(complete_url, proxies=proxies)
        html_doc = r.text.encode('utf-8')
        soup = bs4.BeautifulSoup(html_doc, "html5lib")
        rest_name, rest_dict = sa.get_info(soup)
        if rest_name is None:
            return None
        #rest_id = current_id
        #rest_dict['rest_id'] = rest_dict.get('rest_id', 0)
        #rest_dict['rest_id'] = rest_id
        #current_id += 1
        all_rest[rest_name] = all_rest.get(rest_name, {})
        all_rest[rest_name] = rest_dict
        print(rest_name)
    
    #return all_rest
