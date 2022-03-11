import pickle
import pickle5 as p
import matplotlib
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_pdf import PdfPages

## TASK 1
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

# reduced list of tags
all_tags_edit = ['African', 'American (New)', 'American (Traditional)',
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

country_tags = ['African', 'American (New)', 'American (Traditional)',
 'Argentine', 'Asian Fusion', 'Australian', 'Brazilian', 
 'British', 'Cantonese', 'Caribbean', 'Chinese',
 'Colombian', 'Cuban', 'Czech', 'Dominican', 'Ethiopian',
 'Filipino','French', 'Georgian', 'German', 'Greek', 
 'Hawaiian', 'Himalayan/Nepalese', 'Honduran', 'Indian', 'Irish', 'Italian',
 'Japanese', 'Korean', 'Laotian', 'Latin American', 'Lebanese',
 'Malaysian', 'Mediterranean', 'Mexican', 'Middle Eastern', 'Modern European',
 'Mongolian', 'Moroccan', 'New Mexican Cuisine', 'Pakistani', 'Pan Asian',
 'Persian/Iranian', 'Peruvian', 'Polish', 'Portuguese','Puerto Rican', 
 'Russian', 'Salvadoran', 'Scandinavian', 'Scottish', 'Seafood', 
 'South African', 'Southern', 'Spanish', 'Taiwanese','Thai', 'Turkish', 
 'Ukrainian', 'Uzbek', 'Venezuelan', 'Vietnamese']

dietary_tags = ['Gluten-Free', 'Greek', 'Halal','Kosher', 'Vegan', 'Vegetarian']

other_tags = ['Barbeque', 'Breakfast & Brunch', 'Buffets', 'Cafes', 
'Cajun/Creole', 'Fast Food', 'Seafood','Sushi Bars', 'Tapas Bars']

# tags have been split into three categories. Country/Ethnic tags, tags related
# to dietary restrictions, and then other tags (len = 77 , 62 , 6 , 9)

## TASK 2
#cuisine, frequency of orders in last month , user rating for cuisine, order likelihood
dict1 = {'cuisine': ['Hawaiian', 'Fast Food', 'Filipino', 'Asian Fusion', 'Mexican'] ,
    'num_orders': [ 3 , 5 , 2 , 1 , 4] ,
    'user_rating': [9 , 5 , 8 , 7 , 10],
    'avg_price': [10, 12 , 8 , 15 , 7],
    'est_total': [30 , 60 , 16 ,15 , 28]}
dict2 = {'cuisine': ['Argentine', 'Asian Fusion', 'Australian', 'Brazilian', 
 'British', 'Cantonese', 'Caribbean', 'Chinese'] ,
    'num_orders': [ 8 , 4 , 6 , 7 , 25 , 3 , 1 , 2] ,
    'user_rating': [1 , 5 , 2 , 7 , 10 , 6 , 8 , 0],
    'avg_price': [9, 12 , 13 , 10 , 12 , 9, 10 , 7],
    'est_total': [72 , 48, 78, 70, 300, 27,  10, 14]}

def create_dummy(dict1):
    '''
    Creates dummy data pandas dataframe from dictionaries above for testing data
    visualizations.
    '''
    return pd.DataFrame.from_dict(dict1)


## TASK 3
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