import csv
import pickle
import pickle5 as p
import pandas as pd


def get_rest_info(pickle_file):
    '''
    '''
    
    f = open(pickle_file, 'rb')
    df = p.load(f)
    rest_info_df = df[['id', 'rest_name', 'phone', 'street', 'city', 'website', 
                       'num_review', 'bayes', 'vio_occ', 'time_start', 
                       'time_end', 'risk_val', 'rating', 'price']]
    
    f2 = open('rest_info.pickle', 'wb')
    pickle.dump(rest_info_df, f2, pickle.HIGHEST_PROTOCOL)
    f2.close()


def get_tag_table(pickle_file):
    '''
    '''

    f = open(pickle_file, 'rb')
    df = p.load(f)
    tags_ids= df['id'].tolist()
    tags_list = df['tags'].tolist()
    all_tags = []
    all_ids = []
    tags_info = pd.DataFrame(columns = ['id', 'tag'])
    for index, tags in enumerate(tags_list):
        for tag in tags:
            all_tags.append(tag)
            all_ids.append(tags_ids[index])
    tags_info['id'] = all_ids
    tags_info['tag'] = all_tags

    f2 = open('tag_table.pickle', 'wb')
    pickle.dump(tags_info, f2, pickle.HIGHEST_PROTOCOL)
    f2.close()
    
    
def get_word_table(pickle_file):
    '''
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
            all_words.append(word)
            all_ids.append(words_ids[index])
    words_info['id'] = all_ids
    words_info['word'] = all_words

    f2 = open('word_table.pickle', 'wb')
    pickle.dump(words_info, f2, pickle.HIGHEST_PROTOCOL)
    f2.close() 


def pickle_to_csv(pkl_file, csv_file):
    '''
    '''

    f = open(pkl_file, "rb") 
    df = p.load(f)
    df.to_csv(csv_file)