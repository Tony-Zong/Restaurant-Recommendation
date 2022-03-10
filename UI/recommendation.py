# Provides functions to recommend
# MAYBE DO PANDAS TO SQL INSEAD OF CSV TO SQL

# TO DO: finish get_limit, fix bayes rounding by converting to int, account for try_new (need to wait for data structure), get group_by to work

# Import libraries
import os
import sqlite3
from tokenize import Ignore
import pandas as pd
import pickle5 as p


# Path to database
DATA_DIR = os.path.dirname(__file__)
DATABASE_FILENAME = os.path.join(DATA_DIR, 'rest_db.db')
USER_DATABASE_FILENAME = os.path.join(DATA_DIR, 'user_info.pickle')


# Take in inputs
# tags/words (from search bar, this assumes its comoing from a fat string), time_start, time_end, city, zipcode, 
#   star rating (0-5), price (1-3) upper and lower bounds, boolean for standard or new
# uery = 'SELECT rest_info.* FROM ' + ' WHERE ' + 'ORDER BY rest_info.bayes DESC LIMIT 10'

def recommend(user_id, words = None, time_start = None, time_end = None, zipcode = None, rating = None, price_low = None, price_high = None, try_new = False):
    '''
    '''
    if try_new:
        user_words = find_user_words(user_id)
        query = gen_query(user_words, time_start, time_end, zipcode, rating, price_low, price_high, try_new)
    else:
        query = gen_query(words, time_start, time_end, zipcode, rating, price_low, price_high, try_new)
    return process_query(query)
    

def find_user_words(user_id):
    '''
    '''
    f = open(USER_DATABASE_FILENAME, 'rb')
    df = p.load(f)
    f.close()

    df = df[df['user'] == user_id]
    
    user_words = list(df['rest'].unique()) + list(df['cuisine'].unique())
    user_words = [word.lower() for word in user_words]

    return ' '.join(user_words)


def gen_query(words = None, time_start = None, time_end = None, zipcode = None, rating = None, price_low = None, price_high = None, try_new = False):
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


    
    where_args = []

    # Build query for words
    words_used = False
    word_args = ''
    if words:

        if try_new:
            word_checks = []

            for word in words.split():
                if len(word) > 2:
                    word_checks.append('word NOT LIKE \'%' + word.lower() + '%\'')

            word_args = '(' + ' AND '.join(word_checks) + ')'

            if not word_checks:
                word_args = ''
            else:
                words_used = True

        else:
            word_checks = []

            for word in words.split():
                if len(word) > 2:
                    word_checks.append('word LIKE \'%' + word + '%\'')

            word_args = '(' + ' OR '.join(word_checks) + ')'

            if not word_checks:
                word_args = ''
            else:
                words_used = True
    
    non_word_param = False

    # Build query for other paramaters
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

    # Account for interactions between word arguments and non word arguments
    include_word_query = False
    if words_used or try_new:
        query += ' JOIN words_table ON rest_info.id == words_table.id'  
        include_word_query = True
          
    if include_word_query or non_word_param:
        query += ' WHERE '
        if include_word_query and non_word_param:
            word_args += ' AND '

    # limit is 10 if no words provided, if words provided see comment below
    # if words:
    #     limit = get_limit()
    # else:
    #     limit = 10

    # Assemble completed query
    query += word_args + ' AND '.join(where_args) + ' ORDER BY bayes' #' DESC LIMIT ' + limit + ';'

    return query


# def get_limit():
#     '''
#     '''
#     # FIND LENGTH OF WORDS TABLE (15360), get average tags per word (15360 / 3183) (maybe add 1), MULTUPLY THIS BY NUMBER OF TAGS THAT THEY INPUT
#     db = sqlite3.connect(DATABASE_FILENAME)
#     num_tags = 0
#     num_rest = 0
#     return str(200)


def process_query(query):
    '''
    Produces final recommendation output.

    Inputs:
        query (str)
    
    Outputs:
        pandas df of top restaurants in order and relevant information
    '''
    print(query)
    # Read SQL output to pandas df
    db = sqlite3.connect(DATABASE_FILENAME)
    df = pd.read_sql_query(query, db)
    db.close()

    # Remove stray duplicate columns
    df = df.loc[:,~df.columns.duplicated()]

    df.drop('word', axis=1, inplace=True, errors='ignore')

    # take df, summarize by rest_name (get all the tags into like a list or something in one column, maybe just add strings),
    # write function to cmopare user input words to the tags, produce column for number of overlaps
    df['id'] = pd.to_numeric(df['id'])
    df['tag_overlaps'] = 1
    output_cols = ['id', 'rest_name', 'phone', 'street', 'city', 'zipcode', 'bayes', 'vio_occ', 'time_start', 'time_end', 'risk_val', 'rating', 'price']
    df = df.groupby(output_cols)['tag_overlaps'].count().reset_index() # right now the only words found are the words that are searched for, somehow need to get all the words

    # Sort bayes to nearest 0.5 int
    df['bayes'] = pd.to_numeric(df['bayes'])
    df['rounded_bayes'] = df['bayes'].mul(2).round().div(2)

    # Sort using three conditions 1. Rounded bayes, 2. tag overlaps, and 3. bayes (non-rounded)
    df.sort_values(['rounded_bayes', 'tag_overlaps', 'bayes'], ascending=False, inplace=True)

    return df

