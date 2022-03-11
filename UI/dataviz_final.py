import pickle
import pickle5 as p
import matplotlib
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_pdf import PdfPages
from datetime import date , timedelta
from os.path import exists
import os

DATA_DIR = os.path.dirname(__file__)
USER_DATABASE_FILENAME = os.path.join(DATA_DIR, 'user_info.pickle')
# DF_FILENAME = 'user_info.pickle' #REMOVE THIS LINE

ALL_TAGS_EDIT = ['African', 'American (New)', 'American (Traditional)',
 'Argentine', 'Asian Fusion', 'Australian', 'Barbeque', 'Brazilian', 'Breakfast & Brunch',
 'British', 'Buffets', 'Cafes', 'Cajun/Creole', 'Cantonese', 'Caribbean', 'Chinese',
 'Colombian', 'Cuban', 'Czech', 'Desserts', 'Dominican', 'Ethiopian', 'Fast Food',
 'Filipino', 'French', 'Georgian', 'German', 'Gluten-Free', 'Greek', 'Halal',
 'Hawaiian', 'Himalayan/Nepalese', 'Honduran', 'Indian', 'Irish', 'Italian',
 'Japanese', 'Korean', 'Kosher', 'Laotian', 'Latin American', 'Lebanese',
 'Malaysian', 'Mediterranean', 'Mexican', 'Middle Eastern', 'Modern European',
 'Mongolian', 'Moroccan', 'New Mexican Cuisine', 'Pakistani', 'Pan Asian',
 'Persian/Iranian', 'Peruvian', 'Polish', 'Portuguese', 'Puerto Rican',
 'Russian', 'Salvadoran', 'Scandinavian', 'Scottish', 'Seafood', 'South African',
 'Southern', 'Spanish', 'Sushi Bars', 'Taiwanese', 'Tapas Bars',
 'Tex-Mex', 'Thai', 'Turkish', 'Ukrainian', 'Uzbek', 'Vegan', 'Vegetarian',
 'Venezuelan', 'Vietnamese']

def get_tags(csv):
    '''
    Gets all possible tags from the csv of all restaurant info.
    '''
    all_tags = set()
    f = open(csv, 'rb')
    all_rest = p.load(f)
    for rest in all_rest.values():
       for tag in rest['tags']:
           all_tags.add(tag)
    return all_tags


def check_user_exists(username):
    '''
    Check whether the inputted username already exists.
    '''

    f = open(USER_DATABASE_FILENAME, 'rb')
    user_info = p.load(f)
    return username in user_info['user'].unique()


def check_user_info_df_exists():
    '''
    Check that user_info.pickle exists. If not, create one.
    '''

    if not exists(USER_DATABASE_FILENAME): 
        df = pd.DataFrame(columns = ['user','date','rest','cuisine','user_rating','cost'])
        f = open(USER_DATABASE_FILENAME, 'wb')
        pickle.dump(df, f, pickle.HIGHEST_PROTOCOL)
        f.close()


def add_row(user, date, rest, cuisine, user_rating, cost):
    '''
    Update the user_info data frame when the user inputs information about a meal.
    '''

    f = open(USER_DATABASE_FILENAME, 'rb')
    user_info = p.load(f)

    to_append = pd.DataFrame({'user': [user], 'date': [date], 'rest': [rest], 'cuisine': [cuisine], \
                 'user_rating': [user_rating], 'cost': [cost]})

    user_info = pd.concat([user_info, to_append], ignore_index = True)

    f2 = open(USER_DATABASE_FILENAME, 'wb')
    pickle.dump(user_info, f2, pickle.HIGHEST_PROTOCOL)
    f2.close()


# DATAVIZ
def func(pct, allvals):
    '''
    Formatting for percentage and orders in function "pie"
    '''
    absolute = int(np.round(pct/100.*np.sum(allvals)))
    return "{:.1f}%({:d})".format(pct, absolute)


def func2(pct, allvals):
    '''
    Formatting for percentage and orders in function "costs"
    '''
    absolute = int(np.round(pct/100.*np.sum(allvals)))
    return "{:.1f}%(${:d})".format(pct, absolute)


def get_subset(df , user , start_date , end_date):
    '''
    '''
    if start_date != None and end_date != None:
        subset_df = df.loc[(df['user'] == user) & (df['date'] \
                                >= start_date) & (df['date'] <= end_date)]
    elif start_date == None and end_date != None:
        subset_df = df.loc[(df['user'] == user) & (df['date'] <= end_date)]
    elif start_date != None and end_date == None:
        subset_df = df.loc[(df['user'] == user) & (df['date'] >= start_date)]
    elif start_date == None and end_date == None:
        subset_df = df.loc[df['user'] == user]
    return subset_df


def freq(df , user , start_date , end_date):
    '''
    Returns a pie chart that summarizes how often the diner eats each type of food 
    (such as Asian food, Mexican food, etc.)
    '''
    subset_df = get_subset(df , user , start_date , end_date)
    subset_df = subset_df.reset_index()
    subset_df = subset_df[['cuisine']].value_counts().rename_axis('cuisine').reset_index(name='counts')
    if start_date != None and end_date != None:
        title = 'Percent and Number of User Entries by Cuisine Type from' + ' ' + \
                    start_date.strftime("%b %d %Y") + ' to ' + \
                    end_date.strftime("%b %d %Y")
    elif start_date == None and end_date != None:
        title = 'Percent and Number of User Entries by Cuisine Type before' + ' ' + \
                    end_date.strftime("%b %d %Y")
    elif start_date != None and end_date == None:
        title = 'Percent and Number of User Entries by Cuisine Type after' + ' ' + \
                    start_date.strftime("%b %d %Y")
    elif start_date == None and end_date == None:
        title = 'Percent and Number of User Entries by Cuisine Type'
    pie = subset_df.plot.pie(y = 'counts' , title = title, \
                        legend = False, ylabel = '' ,
                        labels = subset_df.loc[:,"cuisine"],  \
                        autopct = lambda pct: func(pct,subset_df.loc[:,"counts"]))
    plt.show()
    return pie

def pref(df , user ,  start_date , end_date):
    '''
    Returns a bar chart summarizing the ratings a user gives to each type of food.
    '''
    # get subset of dataframe based on username and start/end date
    duplicate_indices = {}
    subset_df = get_subset(df , user , start_date , end_date)
    subset_df = subset_df.reset_index()
    # finds indexes where duplicate restaraunts and maps them to rest key
    for i , row in enumerate(subset_df.duplicated(subset=['rest'] , keep = False)):
        if row is True:
            rest = subset_df.iloc[i]['rest']
            if rest not in duplicate_indices.keys():
                duplicate_indices[rest] = [i]
            else:
                i_list = duplicate_indices[rest]
                i_list.append(i)
                duplicate_indices[rest] = i_list
    # adds a row to df of average of ratings for same rest
    for rest , i_list in duplicate_indices.items():
        sum_ratings = 0
        for i in i_list:
            rating = subset_df.iloc[i]['user_rating']
            sum_ratings += rating
        avg_rating = sum_ratings / len(i_list)
        to_append = pd.DataFrame({'user': [user], 'date': ['N/A'], 'rest': [rest], \
                    'cuisine': [subset_df.iloc[i]['cuisine']], \
                    'user_rating': [avg_rating], 'cost': ['N/A']})
        subset_df = pd.concat([subset_df, to_append], ignore_index = True)
    # removes all rows of a given rest besides the row of average rating
    for rest , i_list in duplicate_indices.items():
        for i in i_list:
            subset_df = subset_df.drop(index = i)
    # actual dataviz construction
    fig = plt.figure()
    cuisine = subset_df.loc[:,"cuisine"]
    ratings = subset_df.loc[:,"user_rating"]
    plt.bar(cuisine , ratings)
    plt.ylabel('User Ratings (1-5)')
    plt.xlabel('Cuisine Type')
    if start_date != None and end_date != None:
        plt.title('User Ratings by Cuisine Type from' + ' ' + \
                    start_date.strftime("%b %d %Y") + ' to ' + \
                    end_date.strftime("%b %d %Y"))
    elif start_date == None and end_date != None:
        plt.title('User Ratings by Cuisine Type before' + ' ' + \
                    end_date.strftime("%b %d %Y"))
    elif start_date != None and end_date == None:
        plt.title('User Ratings by Cuisine Type after' + ' ' + \
                    start_date.strftime("%b %d %Y"))
    elif start_date == None and end_date == None:
        plt.title('User Ratings by Cuisine Type')               
    fig.autofmt_xdate()
    plt.show()
    return fig


def costs(df , user , start_date , end_date):
    '''
    Returns a pie chart estimating total spending by cuisine for a user.
    '''
    subset_df = get_subset(df , user , start_date , end_date)
    cuisine_cost_df =  subset_df.loc[:, subset_df.columns!='user_rating'].groupby(['user', 'cuisine']).sum()
    cuisine_cost_df = cuisine_cost_df.reset_index()
    if start_date != None and end_date != None:
        title = 'User Spending by Cuisine Type from' + ' ' + \
                    start_date.strftime("%b %d %Y") + ' to ' + \
                    end_date.strftime("%b %d %Y")
    elif start_date == None and end_date != None:
        title = 'User Spending by Cuisine Type before' + ' ' + \
                    end_date.strftime("%b %d %Y")
    elif start_date != None and end_date == None:
        title = 'User Spending by Cuisine Type after' + ' ' + \
                    start_date.strftime("%b %d %Y")
    elif start_date == None and end_date == None:
        title = 'User Spending by Cuisine Type'
    pie = cuisine_cost_df.plot.pie(y = 'cost' , title = title,  legend = False, \
                        ylabel = '' , labels = cuisine_cost_df['cuisine'] ,
                        autopct = lambda pct: func2(pct,cuisine_cost_df.loc[:,'cost']))
    
    plt.show()
    return pie


def all_viz(df , user , start_date , end_date):
    '''
    Returns all three types of visualizations listed above and stores as a pdf
    in user's repository.
    '''
    # orders by cuisine type
    fig1 = freq(df , user , start_date , end_date)
    # user spending by cuisine type
    fig2 = costs(df , user , start_date , end_date)
    # user ratings by cuisine type
    fig3 = pref(df , user , start_date , end_date)
    # saving PDF of visualizations in UI repository
    pp = PdfPages('dataviz_' + user + '.pdf')
    pp.savefig(fig1.figure)
    pp.savefig(fig2.figure)
    pp.savefig(fig3)
    pp.close()