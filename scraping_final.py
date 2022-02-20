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

    # use cnt to add another level of random stops
    cnt = 1
    csv_read = open(csv_filename, 'r')
    reader = csv.reader(csv_read)
    for url in reader:
        url = url[0]
        
        # restaurant name
        name_str = url[5:]
        name_lst = name_str.split('-')
        name = ''
        for name_seg in name_lst:
            name += (name_seg[0].upper() + name_seg[1:] + ' ')
        rest_name = name.strip()
        if rest_name in all_rest:
            continue

        # use cnt to add another level of random stops
        if cnt % 15 == 0:
            time.sleep(random.random()*10)
        if cnt % 25 == 0:
            time.sleep(random.random()*15)
        complete_url = 'https://www.yelp.com' + url
        rand_num = random.random()*15 + 5
        # random time interval between each consecutive requests
        time.sleep(rand_num)

        # make request and scrape the data
        r = requests.get(complete_url)
        html_doc = r.text.encode('utf-8')
        soup = bs4.BeautifulSoup(html_doc, "html5lib")
        rest_dict = sa.get_info(soup, url)
        if rest_dict is None:
            return 'Scraping has been stopped. Please see the printing result above to know where it ends.'
        all_rest[rest_name] = all_rest.get(rest_name, {})
        all_rest[rest_name] = rest_dict
        cnt += 1

        # automatically update `data.pickle`
        f = open('data.pickle', 'wb')
        pickle.dump(all_rest, f, pickle.HIGHEST_PROTOCOL)
        f.close()
        print(rest_name)

    

