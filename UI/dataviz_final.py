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


    