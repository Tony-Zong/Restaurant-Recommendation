import csv
from operator import index
import pickle
import pickle5 as p
import pandas as pd
import re


def get_rest_info(pickle_file):
    '''
    Create a dataframe of the information on the restaurants
    '''
    
    f = open(pickle_file, 'rb')
    df = p.load(f)
    rest_info_df = df[['id', 'rest_name', 'phone', 'street', 'city', 'zipcode', 
                       'website', 'num_review', 'bayes', 'vio_occ', 'time_start', 
                       'time_end', 'risk_val', 'rating', 'price']]
    
    f2 = open('rest_info.pickle', 'wb')
    pickle.dump(rest_info_df, f2, pickle.HIGHEST_PROTOCOL)
    f2.close()
    pickle_to_csv('rest_info.pickle', 'rest_info.csv')


def get_tag_table(pickle_file):
    '''
    Create dataframe of the tags assosciated with each restaurants
    '''

    f = open(pickle_file, 'rb')
    df = p.load(f)
    tags_ids= df['id'].tolist()
    tags_list = df['tags'].tolist()
    all_tags = []
    all_ids = []
    tags_info = pd.DataFrame(columns = ['id', 'word'])
    for index, tags in enumerate(tags_list):
        for tag in tags:
            all_tags.append(tag.lower())
            all_ids.append(tags_ids[index])
    tags_info['id'] = all_ids
    tags_info['word'] = all_tags

    f2 = open('tag_table.pickle', 'wb')
    pickle.dump(tags_info, f2, pickle.HIGHEST_PROTOCOL)
    f2.close()


def get_word_table(pickle_file):
    '''
    Create a dataframe of all the words assosciated to the restaurants
    '''

    f = open(pickle_file, 'rb')
    df = p.load(f)
    words_ids= df['id'].tolist()
    words_list = df['words'].tolist()
    all_words = []
    all_ids = []
    words_info = pd.DataFrame(columns = ['id', 'word'])
    for index, words in enumerate(words_list):
        for word in words:
            if bool(re.match(r'^[a-zA-Z]+$', word)) and len(word)>1:
                all_words.append(word)
                all_ids.append(words_ids[index])
    words_info['id'] = all_ids
    words_info['word'] = all_words

    f2 = open('word_table.pickle', 'wb')
    pickle.dump(words_info, f2, pickle.HIGHEST_PROTOCOL)
    f2.close()


def combine_tables(tag_table_file, word_table_file):
    '''
    Combines the dataframe of the tags assosciated to the restaurant with the dataframe
    of the words assosciated to the restaurants
    '''

    f1 = open(tag_table_file, 'rb')
    f2 = open(word_table_file, 'rb')
    tag_table = p.load(f1)
    word_table = p.load(f2)
    words_table = pd.concat([tag_table, word_table], ignore_index=True)
    f3 = open('words_table.pickle', 'wb')
    pickle.dump(words_table, f3, pickle.HIGHEST_PROTOCOL)
    pickle_to_csv('words_table.pickle', 'words_table.csv')
    f1.close()
    f2.close()
    f3.close()


def pickle_to_csv(pkl_file, csv_file):
    '''
    Converts a pickle file to a csv file
    '''

    f = open(pkl_file, "rb") 
    df = p.load(f)
    df.to_csv(csv_file, index = False)