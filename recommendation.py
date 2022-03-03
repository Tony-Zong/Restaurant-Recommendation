# Provides functions to recommend


# Import libraries
import os
import sqlite3


# Path to database
DATA_DIR = os.path.dirname(__file__)
DATABASE_FILENAME = os.path.join(DATA_DIR, 'course-info.db')


# Take in inputs
# tags/words (from search bar, this assumes its comoing from a fat string), time_start, time_end, city, zipcode, 
#   star rating (0-5), price (1-3), boolean for standard or new


# ORDER BY bayesian average then take limti
select_args = 'rest_info'
from_args = ''
where_args = ''

# figure out what format tags/words comes in
query = 'SELECT rest_info.* FROM ' + ' WHERE ' + 'ORDER BY rest_info.bayes DESC LIMIT 10'



def asdasdasdasd(words, time_start, time_end, city, zipcode, rating, price, ):
    from_args = ''
    where_args = ''

    query = 'SELECT rest_info.* FROM ' + ' WHERE ' + 'ORDER BY rest_info.bayes DESC LIMIT 10'