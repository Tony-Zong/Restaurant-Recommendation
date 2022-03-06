# Provides functions to recommend
# MAYBE DO PANDAS TO SQL INSEAD OF CSV TO SQL

# Import libraries
import os
import sqlite3
import pandas as pd


# Path to database
DATA_DIR = os.path.dirname(__file__)
DATABASE_FILENAME = os.path.join(DATA_DIR, 'course-info.db')


# Take in inputs
# tags/words (from search bar, this assumes its comoing from a fat string), time_start, time_end, city, zipcode, 
#   star rating (0-5), price (1-3) upper and lower bounds, boolean for standard or new
# uery = 'SELECT rest_info.* FROM ' + ' WHERE ' + 'ORDER BY rest_info.bayes DESC LIMIT 10'

def recommend(user_id, words = None, time_start = None, time_end = None, zipcode = None, rating = None, price_low = None, price_high = None, try_new = False):
    query = gen_query(user_id, words = None, time_start = None, time_end = None, zipcode = None, rating = None, price_low = None, price_high = None, try_new = False)

    


def gen_query(db_fname, user_id, words = None, time_start = None, time_end = None, zipcode = None, rating = None, price_low = None, price_high = None, try_new = False):
    '''
    Inputs:
        db_fname (str): string indicating db filename
        words (str)
        time_start (str)
        time_end (str)
        zipcode (str)
        rating (str)
        price (str)
        try_new (bool)
    '''
    query = 'SELECT * FROM rest_info'

    if words:
        query += ' JOIN words_table ON rest_info.id == words_table.id'
    
    where_args = []

    # Where arguments, CHANGE TO BETTER LOOKING THAN 30000 IFS LATER pakistani/irani
    words_used = False
    word_args = '' # don't forget to append AND on the back
    if words:
        word_checks = []
        for word in words.split():
            print(word)
            if len(word) > 2:
                word_checks.append('word LIKE \'%' + word + '%\'')
                print('appended word')
        word_args = '(' + ' OR '.join(word_checks) + ')'
        print(word_args)
        if not word_checks:
            word_args = ''
        # else:
        #     words_used = True
    
    non_word_param = False

    if time_start:
        where_args.append('time_start >= ' + time_start)
        non_word_param = True

    if time_end:
        where_args.append('time_end <= ' + time_end)
        non_word_param = True

    if zipcode:
        where_args.append('zipcode == ' + zipcode)
        non_word_param = True

    if rating:
        where_args.append('rating >= ' + rating)
        non_word_param = True

    if price_low:
        where_args.append('price <= ' + price_low)
        where_args.append('price != ' + '-1')
        non_word_param = True

    if price_high:
        where_args.append('price <= ' + price_high)
        where_args.append('price != ' + '-1')
        non_word_param = True

    if words and non_word_param:
        word_args += ' AND '
    
    # Query

    # limit is 10 if no words provided, if words provided see comment below
    query += ' WHERE ' + word_args + ' AND '.join(where_args) + ' ORDER BY bayes DESC LIMIT 100' + ';'

    return query



def process_query(query):
    '''
    '''
    db = sqlite3.connect(db_fname)

    df = pd.read_sql_query(query, db)
    db.close()

    print(df[['rest_name', 'bayes', 'word']])

    #print(query)
    #need to detecet when u have words and other input, if thats the case add the AND to end of word_args, otherwise dont

    # FIND LENGTH OF WORDS TABLE (15360), get average tags per word (15360 / 3183) (maybe add 1), MULTUPLY THIS BY NUMBER OF TAGS THAT THEY INPUT

    # take df, summarize by rest_name (get all the tags into like a list or something in one column, maybe just add strings),
    # write function to cmopare user input words to the tags, produce column for number of overlaps

    # sort  bayes to nearest int or 0.5 int or something, then sort using two conditions 1. bayes, and 2. tag overlaps
    # split function up

