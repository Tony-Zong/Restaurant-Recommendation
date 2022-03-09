import pickle
import pickle5 as p
import matplotlib
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_pdf import PdfPages
from datetime import date , timedelta

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

    

# start date and end date are None by default. if this is the case return dataviz
# for all dates in date range

def date_range(start_date , end_date):
    '''
    '''
    day_set = set()
    delta = end_date - start_date  # as timedelta
    days = [start_date + timedelta(days=i) for i in range(delta.days + 1)]
    for day in days:
        day_set.add(day)
    return day_set

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


def pie(df):
    '''
    Returns a pie chart that summarizes how often the diner eats each type of food 
    (such as Asian food, Mexican food, etc.)
    '''
    pie = df.plot.pie(y = 'num_orders' , title = 'Recent Orders by Cuisine Type (in last week)\n Order % (Order #)', \
                        legend = False, ylabel = '' ,
                        labels = df.loc[:,"cuisine"],  \
                        autopct = lambda pct: func(pct,df.loc[:,"num_orders"]))
    plt.show()
    

def pref(df):
    '''
    Returns a bar chart summarizing the ratings a user gives to each type of food.
    '''
    fig = plt.figure()
    cuisine = df.loc[:,"cuisine"]
    ratings = df.loc[:,"user_rating"]
    plt.bar(cuisine , ratings , color = 'rgbkymc')
    plt.ylabel('User Rating 0-10 (least liked - most liked')
    plt.xlabel('Cuisine Type')
    plt.title('User Ratings by Cuisine Type')
    fig.autofmt_xdate()
    plt.show()
    

def costs(df):
    '''
    Returns a pie chart estimating total spending by cuisine for a user.
    '''
    pie = df.plot.pie(y = 'est_total' , \
            title = 'Estimated Total Spending by Cuisine (in last week) \n (# orders * avg price)', \
                        legend = False, ylabel = '' ,
                        labels = df.loc[:,"cuisine"],
                        autopct = lambda pct: func2(pct,df.loc[:,"est_total"]))
    plt.show()


def all_viz(df):
    '''
    Returns all three types of visualizations listed above and stores as a pdf
    in user's repository.
    '''
    # orders by cuisine
    pie1 = df.plot.pie(y = 'num_orders' , title = 'Recent Orders by Cuisine Type (in last week)\n Order % (Order #)', \
                        legend = False, ylabel = '' ,
                        labels = df.loc[:,"cuisine"],  \
                        autopct = lambda pct: func(pct,df.loc[:,"num_orders"]))
    #user spending
    pie2 = df.plot.pie(y = 'est_total' , \
            title = 'Estimated Total Spending by Cuisine (in last week) \n (# orders * avg price)', \
                        legend = False, ylabel = '' ,
                        labels = df.loc[:,"cuisine"],
                        autopct = lambda pct: func2(pct,df.loc[:,"est_total"]))
    #user preferences
    fig3 = plt.figure()
    cuisine = df.loc[:,"cuisine"]
    ratings = df.loc[:,"user_rating"]
    plt.bar(cuisine , ratings , color = 'rgbkymc')
    plt.ylabel('User Rating 0-10 (least liked - most liked')
    plt.xlabel('Cuisine Type')
    plt.title('User Ratings by Cuisine Type')
    fig3.autofmt_xdate()
    plt.show()
    pp = PdfPages('dataviz.pdf')
    pp.savefig(pie1.figure)
    pp.savefig(pie2.figure)
    pp.savefig(fig3)
    pp.close()
    