import pickle
import pickle5 as p
import matplotlib
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_pdf import PdfPages
from datetime import date , timedelta

DF_FILENAME = 'user_info.pickle'

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

    f = open(DF_FILENAME, 'rb')
    user_info = p.load(f)
    return username in df['user'].unique()


def check_user_info_df_exists():
    '''
    Check that user_info.pickle exists. If not, create one.
    '''

    if not exists(DF_FILENAME): 
        df = pd.DataFrame(columns = ['user','date','rest','cuisine','user_rating','cost'])
        f = open(DF_FILENAME, 'wb')
        pickle.dump(df, f, pickle.HIGHEST_PROTOCOL)
        f.close()


def add_row(user, date, rest, cuisine, user_rating, cost):
    '''
    Update the user_info data frame when the user inputs information about a meal.
    '''

    f = open(DF_FILENAME, 'rb')
    user_info = p.load(f)

    to_append = {'user': user, 'date': date, 'rest': rest, 'cuisine': cuisine, \
                 'user_rating': user_rating, 'cost': cost}

    user_info = user_info.append(to_append, ignore_index = True)

    f2 = open(DF_FILENAME, 'wb')
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
    Formatting for percentage and orders in function "pie"
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


def pie(df , user , start_date , end_date):
    '''
    Returns a pie chart that summarizes how often the diner eats each type of food 
    (such as Asian food, Mexican food, etc.)
    '''
    subset_df = get_subset(df , user , start_date , end_date)
    if start_date != None and end_date != None:
        title = 'User Eating History by Cuisine Type from' + ' ' + \
                    start_date.strftime("%b %d %Y") + ' to ' + \
                    end_date.strftime("%b %d %Y")
    elif start_date == None and end_date != None:
        title = 'User Eating History by Cuisine Type before' + ' ' + \
                    end_date.strftime("%b %d %Y")
    elif start_date != None and end_date == None:
        title = 'User Eating History by Cuisine Type after' + ' ' + \
                    start_date.strftime("%b %d %Y")
    elif start_date == None and end_date == None:
        title = 'User Eating History by Cuisine Type'
    #pie = df.plot.pie(y = 'num_orders' , title = title, \
                        #legend = False, ylabel = '' ,
                        #labels = df.loc[:,"cuisine"],  \
                        #autopct = lambda pct: func(pct,df.loc[:,"num_orders"]))
    #plt.show()
    

def pref(df , user ,  start_date , end_date):
    '''
    Returns a bar chart summarizing the ratings a user gives to each type of food.
    '''
    subset_df = get_subset(df , user , start_date , end_date)
    fig = plt.figure()
    #return subset_df.duplicated(subset=['rest'] , keep = False)
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
    

def costs(df , user , start_date , end_date):
    '''
    Returns a pie chart estimating total spending by cuisine for a user.
    '''
    subset_df = get_subset(df , user , start_date , end_date)
    cuisine_cost_df =  subset_df.loc[:, subset_df.columns!='user_rating'].groupby(['user', 'cuisine']).sum()
    #return cuisine_cost_df
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
                        ylabel = '' , labels = subset_df.loc[:,'cuisine'], \
                        autopct = lambda pct: func2(pct,df.loc[:,'cost']))
    plt.show()


def all_viz(df , user , start_date , end_date):
    '''
    Returns all three types of visualizations listed above and stores as a pdf
    in user's repository.
    '''
    # orders by cuisine
    pie1 = pie(df , user , start_date , end_date)

    #user spending
    pie2 = costs(df , user , start_date , end_date)


    
    pp = PdfPages('dataviz_' + user + '.pdf')
    pp.savefig(pie1.figure)
    pp.savefig(pie2.figure)
    pp.savefig(fig3)
    pp.close()
    