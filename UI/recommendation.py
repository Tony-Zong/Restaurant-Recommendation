# Import libraries
import datetime
import os
import sqlite3
from tokenize import Ignore
import pandas as pd
import pickle5 as p


# Path to databases
DATA_DIR = os.path.dirname(__file__)
DATABASE_FILENAME = os.path.join(DATA_DIR, 'rest_db.db')
USER_DATABASE_FILENAME = os.path.join(DATA_DIR, 'user_info.pickle')


def recommend(user_id, words = None, time_start = None, time_end = None, zipcode = None, rating = None, price_low = None, price_high = None, try_new = False):
    '''
    Given parameters, recommends top restaurants for user that fit given criteria.

    Inputs:
        user_id (str)
        words (str)
        time_start (str)
        time_end (str)
        zipcode (str)
        rating (str)
        price_low (str)
        price_high (str)
        try_new (bool)
    
    Outputs:
        pandas df of top restaurants in order and relevant information
    '''
    if try_new:
        user_words = find_user_words(user_id)
        query = gen_query(user_words, time_start, time_end, zipcode, rating, price_low, price_high, try_new)
    else:
        query = gen_query(words, time_start, time_end, zipcode, rating, price_low, price_high, try_new)
    return process_query(query)
    

def find_user_words(user_id):
    '''
    Extracts tags associated with user's prior eating history for use in
        search criteria for try_new recommendation

    Inputs:
        user_id (str)
    
    Outputs:
        String of words and tags associated with user's eating history separated by spaces.
    '''
    f = open(USER_DATABASE_FILENAME, 'rb')
    df = p.load(f)
    f.close()

    # Account for info from last 60 days only
    today = datetime.date.today()
    df['date'] = pd.to_datetime(df['date']).dt.date
    df['time_difference'] = today - df['date']

    # Filter by user id and time
    df = df[(df['user'] == user_id) & (df['time_difference'] < datetime.timedelta(days=60))]
    
    # Extract word list from cuisines and restaurant names for search
    user_words = list(df['rest'].unique()) + list(df['cuisine'].unique())
    user_words = [word.lower() for word in user_words]

    return ' '.join(user_words)


def gen_query(words = None, time_start = None, time_end = None, zipcode = None, rating = None, price_low = None, price_high = None, try_new = False):
    '''
    Constructs SQL query given user parameters.

    Inputs:
        words (str)
        time_start (str)
        time_end (str)
        zipcode (str)
        rating (str)
        price_low (str)
        price_high (str)
        try_new (bool)
    
    Outputs:
        String representing the query to be made.
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
        where_args.append('time_start <= ' + time_start)
        non_word_param = True

    if time_end:
        where_args.append('time_end >= ' + time_end)
        non_word_param = True

    if zipcode:
        where_args.append('zipcode == ' + zipcode)
        non_word_param = True

    if rating:
        where_args.append('rating >= ' + rating)
        non_word_param = True
    
    if price_low or price_high:
        where_args.append('price != ' + '-1')
        non_word_param = True
        if price_low:
            where_args.append('price <= ' + price_low)
        if price_high:
            where_args.append('price <= ' + price_high)

    # Account for interactions between word arguments and non word arguments
    include_word_query = False
    if words_used or try_new:
        query += ' JOIN words_table ON rest_info.id == words_table.id'  
        include_word_query = True
          
    if include_word_query or non_word_param:
        query += ' WHERE '
        if include_word_query and non_word_param:
            word_args += ' AND '


    # Assemble completed query
    query += word_args + ' AND '.join(where_args) + ' ORDER BY bayes' #' DESC LIMIT ' + limit + ';'

    return query


def process_query(query):
    '''
    Produces final recommendation output.

    Inputs:
        query (str)
    
    Outputs:
        pandas df of top restaurants in order and relevant information
    '''
    # Read SQL output to pandas df
    db = sqlite3.connect(DATABASE_FILENAME)
    df = pd.read_sql_query(query, db)
    db.close()

    # Remove stray duplicate columns and change column types for grouping
    df = df.loc[:,~df.columns.duplicated()]
    df.drop('word', axis=1, inplace=True, errors='ignore')
    df['id'] = pd.to_numeric(df['id'])

    # For each restaurant, count number of tags matching search criteria
    df['tag_overlaps'] = 1
    output_cols = ['id', 'rest_name', 'phone', 'street', 'city', 'zipcode', 'bayes', 'vio_occ', 'time_start', 'time_end', 'risk_val', 'rating', 'price']
    df = df.groupby(output_cols)['tag_overlaps'].count().reset_index() # right now the only words found are the words that are searched for, somehow need to get all the words

    # Sort bayes to nearest 0.5 int
    df['bayes'] = pd.to_numeric(df['bayes'])
    df['rounded_bayes'] = df['bayes'].mul(2).round().div(2)

    # Sort using three conditions 1. Rounded bayes, 2. tag overlaps, and 3. bayes (non-rounded)
    df.sort_values(['rounded_bayes', 'tag_overlaps', 'bayes'], ascending=False, inplace=True)

    return df.head(30)

