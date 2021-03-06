# only for testing in ipython3
%load_ext autoreload
%autoreload 2

import bs4
from bs4 import BeautifulSoup
import csv
import requests
import scraping_all as sa
import scraping_final as sf
import pickle
import pickle5 as p
import pandas as pd

url1 = "https://www.yelp.com/biz/italian-fiesta-pizzeria-dolton-dolton"
r = requests.get(url1)
html_doc = r.text.encode('utf-8')
soup = bs4.BeautifulSoup(html_doc, "html5lib")

url2 = "https://www.yelp.com/biz/tacos-el-pastor-53-chicago?osq=Restaurants"
r2 = requests.get(url2)
html_doc2 = r2.text.encode('utf-8')
soup2 = bs4.BeautifulSoup(html_doc2, "html5lib")

url3 = "https://www.yelp.com/biz/western-tacos-chicago"
r3 = requests.get(url3)
html_doc3 = r3.text.encode('utf-8')
soup3 = bs4.BeautifulSoup(html_doc3, "html5lib")

url4 = "https://www.yelp.com/biz/the-purple-pig-chicago"
r4 = requests.get(url4)
html_doc4 = r4.text.encode('utf-8')
soup4 = bs4.BeautifulSoup(html_doc4, "html5lib")

url5 = "https://www.yelp.com/biz/se%C3%B1or-pan-caf%C3%A9-chicago-3"
r5 = requests.get(url5)
html_doc5 = r5.text.encode('utf-8')
soup5 = bs4.BeautifulSoup(html_doc5, "html5lib")

url6 = "https://www.yelp.com/biz/la-exclusiva-la-michoacana-cicero-2"
r6 = requests.get(url6)
html_doc6 = r6.text.encode('utf-8')
soup6 = bs4.BeautifulSoup(html_doc6, "html5lib")

####
import pickle
import pickle5 as p

f = open('user_info.pickle', 'wb')
pickle.dump(users, f, pickle.HIGHEST_PROTOCOL)
f.close()

f = open('user_info.pickle', 'rb')
users = p.load(f)







DF_FILENAME = 'user_info.pickle'

def check_user_exists(username):
    '''
    Check whether the inputted username already exists.
    '''

    f = open(DF_FILENAME, 'rb')
    user_info = p.load(f)
    return username in df['user'].unique()


def add_row(user, date, rest, cuisine, user_rating, cost):
    '''
    Update the user_info data frame when the user inputs information about a meal.
    '''

    f = open(DF_FILENAME, 'rb')
    user_info = p.load(f)

    to_append = {'user': user, 'date': date, 'rest': rest, 'cuisine': cuisine,
                 'user_rating': user_rating, 'cost': cost}

    user_info = user_info.append(to_append, ignore_index = True)

    f2 = open(DF_FILENAME, 'wb')
    pickle.dump(user_info, f2, pickle.HIGHEST_PROTOCOL)
    f2.close()



                