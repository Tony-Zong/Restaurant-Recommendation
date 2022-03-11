import datetime
from datetime import date as dt
import dataviz_final as df
import recommendation as r
import pandas as pd
import pickle5 as p

'''
The following functions pertain to visualizing the data
'''

def get_data(userID):
    '''
    Creates data visualisation for the user. Takes in the userID.
    '''
    user_info = load_pickle()
    print("""\nYou will be asked to input a range of dates on which you would like data on. 
If for either start or end date you would like it to not have bounds just press enter""")

    #gets the upper and lower bound dates from the user
    start_check = get_lower_date()
    end_check = get_upper_date()

    #ensures the range of dates is valid
    if end_check != None and start_check != None:
        if end_check < start_check:
            print("\nThe end date preceds the start date, please try again")
            get_date()

    #the data is visualized through pop up windows and a PDF of the data is added to the directory
    print("Please close all pop up windows before proceeding")
    df.all_viz(user_info, userID, start_check, end_check)
    print("\nThe data was successfully added to the directory.")


def load_pickle():
    '''
    Opens the pickle file containing the user information and returns it
    '''
    f = open(df.DF_FILENAME, 'rb')
    user_info = p.load(f)
    return user_info

def get_lower_date():
    '''
    Gets the lower bound date from the user to visualized data. 
    Returns the data as a date object or returns None if there is no bound
    '''
    print("\nWhat date would you like the data to start from?")
    start_date = input()

    if start_date == '':
        start_check = None

    else:
        start_check = check_date(start_date)
        if start_check == None:
            print("\nInvalid start date, please try again")
            start_check = get_lower_date()

    return start_check


def get_upper_date():
    '''
    Gets the lower bound date from the user to visualized data. 
    Returns the data as a date object or returns None if there is no bound
    '''
    print("\nWhat date would you like the data to end on?")
    end_date = input()

    if end_date == '':
        end_check = None

    else:
        end_check = check_date(end_date)
        if end_check == None:
            print("\nInvalid end date, please try again")
            end_check = get_upper_date()

    return end_check


'''
The following functions pertain to inputing a new entry
'''


def new_entry(userID):
    '''
    Creates a new entry for the user. Takes in the userID
    '''
    #gets all the user inputs from helper functions
    date = get_date()
    restaurant = get_restaurant()
    price = get_price()
    user_rating = get_user_rating()
    cuisine = get_cuisine()

    #adds the new entry to the user database
    df.add_row(userID, date, restaurant, cuisine, user_rating, price)
    print('Your entry was successfully added')


def get_date():
    '''
    Gets the date for which the entry will be submitted. Returns a date object
    '''
    print("""\nInput the day you ate the entry you would like to submit. 
(Input it in mm/dd/yyyy format)""")
    date = input()

    date_check = check_date(date)

    if date_check == None:
        print("\nNot a valid date inputed, please try again")
        checked = get_date()
    else:
        checked = date_check

    return checked


def get_restaurant():
    '''
    Gets the restaurant for the entry that will be added. Returns a string for the 
    restaurant or None if N/A
    '''
    print("\nInput the name of the restaurant you ate at for this entry. (Press enter if N/A)")
    restaurant = input()

    return restaurant


def get_price():
    '''
    Gets the price of the meal for the entry that will be added. Returns a float
    '''
    print("""\nInput the price of the meal you ate for this entry. 
(Only input numbers with two decimal points eg. 10.30 for $10.30)""")
    price = input()

    #ensures the price was inputed in the format requested
    if len(price) >= 3:
        if price[len(price) - 3] == '.' and price[len(price) - 2:].isnumeric() and price[:len(price) - 3].isnumeric():
            good_price = float(price)
        else:
            print("\nNot a valid price, please try again")
            good_price = get_price()

    else:
        print("\nNot a valid price, please try again")
        good_price = get_price()

    return good_price


def get_user_rating():
    '''
    Gets the user rating for the meal entry. Returns a float
    '''
    print("\nInput your rating of this meal entry. (Input an integer between 1-5)")
    user_rating = input()

    try:
        float_user_rating = float(user_rating)
        if float_user_rating >= 1 and float_user_rating <= 5:
                good_user_rating = float_user_rating

    except:
        ("\nInvalid rating, please try again")
        good_user_rating = get_user_rating()

    else:
        print("\nInvalid rating, please try again")
        good_user_rating = get_user_rating()

    return good_user_rating
    

def get_cuisine():
    '''
    Gets the cuisine for the meal entry. Returns a string of the cuisine
    '''
    print("\nInput the cuisine for this meal entry. (See below for cuisine options and input it as listed)")

    #gets the list of possible cuisines
    cuisine_options = df.ALL_TAGS_EDIT
    list_cuisines = ''

    #prints the list of possible cuisines
    for index, option in enumerate(cuisine_options):
        if index % 10 == 0:
            list_cuisines += "\n"
        list_cuisines += option + ", "

    print(list_cuisines[:-2])

    cuisine = input()

    if cuisine in cuisine_options:
        good_cuisine = cuisine
    else:
        print("\nNot a valid cuisine, please try again")
        good_cuisine = get_cuisine()

    return good_cuisine


'''
The following functions pertain to getting reccomendations
'''

def get_recommendation(userID, try_new):
    '''
    Gets a reccomendation for the user. Takes in the userID and a boolean True 
    if they want to try something new and False if they want to input what they
    are looking for
    '''
    #only asks the user for an input on tags assosciated to the restaurant if they didn't want something new
    if not try_new:
        tags = get_tags()
    else:
        tags = None

    #gets the input from the user using helper functions
    open_time, close_time = get_times()
    zipcode = get_zipcode()
    rating = get_rating()
    price_low, price_high = get_price_range()

    #gets the reccomendations based on the user's inputs
    recs = r.recommend(userID, tags, open_time, close_time, zipcode, rating, price_low, price_high, try_new)

    #ensures that there are restaurants that can be reccomended otherwise tells the user there isn't
    if len(recs) == 0:
        print("The search terms you inputted were too narrow and we couldn't find any matching restaurants.")

    #prints the recommendations
    else:
        starting_rec = 0
        starting_rec, final_rec = print_recs(recs, starting_rec)

        #asks the user if there is more information they are looking for until they say they're done
        done = add_info(recs, starting_rec, final_rec)

        while not done[0]:
            done = add_info(recs, done[1], done[2])


def print_recs(recs, starting_rec):
    '''
    Prints the recommendations for the user. Takes in as input the dataframe of restaurants that will be recommended
    and an int, starting_rec which is the index for the first restaurant we will recommend.
    '''
    #checks if there are restaurants left to recommend
    if starting_rec >= len(recs):
        print("\nThese are all the restaurants we can reccomend based on your inputs")
    
    else:
        print("\nThese are the restaurants we recommend:")

    final_rec = starting_rec

    for row in recs:
        if final_rec >= len(recs):
            break

        #prints the name of the restaurant we are recommending along with an assosciated digit betweeen 1 and 10
        restaurant = recs.iloc[final_rec]["rest_name"]
        print(str(final_rec % 10 + 1) + ". " + restaurant)
        final_rec += 1

        #stops after 10 restaurants have been recommended
        if final_rec % 10 == 0:
            break

    #checks if there were less than 10 restaurants that could be recommended
    if final_rec % 10 != 0:
        "\nThese are all the restaurants we can recommend based on your inputs"

    return starting_rec, final_rec


def add_info(recs, starting_rec, final_rec):
    '''
    Asks the user if they would like additional restaurant recommendations or additional information on the restaurant.
    Takes in as input the dataframe of recommendations and a starting_rec value, an int of the index for the first 
    recommendation in the currently displayed recommendations and final_rec, an int of the index of the last recommendation 
    in the currently displayed recommendations.
    Returns a tuple of a boolean True if they do not want additional information or False if they do want more information,
    an int of the index for the first recommendation in the currently displayed recommendations and an int of the index of 
    the last recommendation in the currently displayed recommendations.
    '''
    print("""\nWould you like to get additional information on any of these restaurants?
Input the integer corresponding for the restaurant if yes.
If you would like to get the subsequent ten restaurants input 0
If you are satisfied with the information press enter""")
    add_info_input = input()

    possible_rest_nums = list(range(1, 11))

    #checks if the users doesn't want additional information
    if add_info_input == '':
        done = (True, starting_rec, final_rec)

    elif add_info_input.isnumeric():
        if int(add_info_input) == 0:
            #checks if more restaurants can be recommended
            if final_rec >= len(recs):
                print("\nThese are all the restaurants we can reccomend based on your inputs")
                done = (True, starting_rec, final_rec)
            
            else:
                starting_rec, final_rec = print_recs(recs, final_rec)
                done = add_info(recs, starting_rec, final_rec)

        #cleans the data we have on the additional information on the restaurant and prints it for the user
        elif int(add_info_input) in possible_rest_nums:
            current_rest = final_rec - 11 + int(add_info_input)
            default_val = {None, '', 'Unknown', "Not available", '-1'}

            if recs.iloc[current_rest]["rest_name"] in default_val:
                rest_name = 'Unknown'
            else:
                rest_name = recs.iloc[current_rest]["rest_name"]

            if recs.iloc[current_rest]["phone"] in default_val:
                phone_num = 'Unknown'
            else:
                phone_num = recs.iloc[current_rest]["phone"]

            if recs.iloc[current_rest]["street"] in default_val:
                street = 'Unknown'
            else:
                street = recs.iloc[current_rest]["street"]

            if recs.iloc[current_rest]["zipcode"] in default_val:
                zipcode = 'Unknown'
            else:
                zipcode = str(recs.iloc[current_rest]["zipcode"])

            if recs.iloc[current_rest]["city"] in default_val:
                city = 'Unknown'
            else:
                city = recs.iloc[current_rest]["city"]

            if recs.iloc[current_rest]["time_start"] in default_val:
                open_time = 'Unknown'
            else:
                df_open_time = str(recs.iloc[current_rest]["time_start"])

                if int(df_open_time) < 1000:
                    first_half = df_open_time[:1]
                    second_half = df_open_time[1:]

                elif int(df_open_time) == 2400:
                    first_half = '00'
                    second_half = '00'

                else:
                    first_half = df_open_time[:2]
                    second_half = df_open_time[2:]

                open_time = str(first_half) + ":" + str(second_half)

            if recs.iloc[current_rest]["time_end"] in default_val:
                close_time = 'Unknown'
            else:
                df_close_time = str(recs.iloc[current_rest]["time_end"])

                if int(df_close_time) < 1000:
                    first_half = df_close_time[:1]
                    second_half = df_close_time[1:]

                elif int(df_close_time) == 2400:
                    first_half = '00'
                    second_half = '00'

                elif int(df_close_time) > 2400:
                    first_half = df_close_time[:2] - 24
                    second_half = df_close_time[2:]

                else:
                    first_half = df_close_time[:2]
                    second_hald = df_close_time[2:]

                close_time = str(first_half) + ":" + str(second_half)

            if recs.iloc[current_rest]["rating"] in default_val:
                rating = 'Unknown'
            else:
                rating = str(recs.iloc[current_rest]["rating"])
            
            print("\nRestaurant name: " + rest_name)
            print("Phone number: " + phone_num)
            print("Street: " + street)
            print('Zipcode: ' + zipcode)
            print('City: ' + city)
            print("Opening time: " + open_time)
            print("Closing time: " + close_time)
            print("Yelp rating: " + rating)

            done = (False, starting_rec, final_rec)

        else:
            print("\nInvalid input, please try again")
            done = add_info(recs, starting_rec, final_rec)

    else:
        print("\nInvalid input, please try again")
        done = add_info(recs, starting_rec, final_rec)

    return done


def get_try_new():
    '''
    Asks the user if they would like a reccomendation based on specific inputs
    or based on things they haven't tried yet. Returns True if they want something
    new or False if they want something specific
    '''
    print("""\nInput 1 if you would like to get restaurant recomendations based on specific inputs
Input 2 if you would like restaurant recommendations selected based on things you haven't tried yet""")
    try_new = input()

    if try_new == '1':
        wants_new = False
    elif try_new == '2':
        wants_new = True
    else:
        print("\nInvalid input, please try again")
        wants_new = get_try_new()
        
    return wants_new

def get_tags():
    '''
    Gets the tags for the type of restaurant the user is looking for.
    Returns the tags as a string or None if N/A
    '''
    print("""\nWhat kind of restaurant are you looking for? 
Input tags with a space in between or input suggest to get a list of suggested tags""")
    tags_words = input()

    if tags_words == 'suggest':
        #prints the possible cuisine as tag options
        cuisine_options = df.ALL_TAGS_EDIT

        for index, option in enumerate(cuisine_options):
            if index % 10 == 0:
                list_cuisines += "\n"
            list_cuisines += option + ", "

        print(list_cuisines[:-2])
        final_tags = get_tags()
    else:
        final_tags = tags_words

    return final_tags


def get_times():
    '''
    Gets the minimum time range the user would like the restaurant to be open during.
    Returns a tuple of strings of the times or None if N/A
    '''
    open_check = get_open_time()
    close_check = get_close_time()

    if open_check != None and close_check != None:
        if open_check > close_check:
            print("\nThe closing time was earlier than the opening time, please try again")
            open_check, close_check = get_times()

    return open_check, close_check


def get_open_time():
    '''
    Get the latest opening time from the user and returns it as a string and None if N/A
    '''
    print("""\nWhat is the latest time you would like the restaurant to be open by? 
Input in 24 hour format with leading 0s eg. 1400 for 2:00PM and 0700 for 7:00AM.""")
    open_time = input()

    if len(open_time) == 4 and open_time.isnumeric():
        if int(open_time) >= 0 and int(open_time) <= 2359:
            open_check = open_time
        else:
            print("\nInvalid time, please try again")
            open_check = get_open_time()

    elif open_time == '':
        open_check = None

    else:
        print("\nInvalid time, please try again")
        open_check = get_open_time()	

    return open_check


def get_close_time():
    '''
    Gets the earliest closing time from the user and returns it as a string and None if N/A
    '''
    print("""\nWhat is the earliest time would you like the restaurant close by? 
Input in 24 hour format with leading 0s eg. 1400 for 2:00PM and 0700 for 7:00AM.
If you want it to close after midnight, add additional hours to 2400 eg. 2700 for 3:00AM.""")
    close_time = input()

    if len(close_time) == 4 and close_time.isnumeric():
        if int(close_time) >= 0:
            close_check = close_time
        else:
            print("\nInvalid time, please try again")
            close_check = get_close_time()

    elif close_time == '':
        close_check = None

    else:
        print("\nInvalid time, please try again")
        close_check = get_close_time()

    return close_check


def get_zipcode():
    '''
    Asks which zipcode the user would like the restaurant to be in. 
    Returns the zipcode as a string or None if N/A
    '''
    print("\nWhich zipcode would you like the restaurant to be in?")
    zipcode = input()

    if len(zipcode) == 5 and zipcode.isnumeric():
        good_zipcode = zipcode

    elif zipcode == '':
        good_zipcode = None
        
    else:
        print("\nInvalid zipcode, please try again")
        good_zipcode = get_zipcode()

    return good_zipcode


def get_rating():
    '''
    Asks the user for the minimum rating they would like for recommendations
    Returns the rating as a string or None if N/A
    '''
    print("""\nWhat is the minimum rating you would like for the restaurants? 
Input a number between 1 and 5, a decimal may be entered""")
    rating = input()
    if rating == '':
        good_rating = None

    else:
        try:
            float_rating = float(rating)
            if float_rating >= 1 and float_rating <= 5:
                good_rating = rating

        except:
            print("\nInvalid rating, please try again")
            good_rating = get_rating()

    return good_rating


def get_price_range():
    '''
    Asks the user what price range they would like the recommendations to be in.
    Returns the price range as a tuple of strings or None if N/A
    '''
    print("""\nPrice ranges are represented as integers between 1 and 4.
1 represents under $10, 2 represents $11-$30, 3 represents $31-$60, and 4 represents above $61""")

    low_check = get_low_price()
    high_check = get_high_price()

    if low_check != None and high_check != None:
        if low_check > high_check:
            print("\nThe lowest price range is higher than the highest price range, please try again")
            low_check, high_check = get_price_range()

    return low_check, high_check


def get_low_price():  
    '''
    Gets the lower bound for the price range. Returns it as a string or None if N/A
    '''
    print("\nWhat is the lowest price range you are looking for?")
    price_low = input()

    if price_low.isnumeric() and (int(price_low) == 1 or int(price_low) == 2 
        or int(price_low) == 3 or int(price_low) == 4):
        low_check = price_low

    elif price_low == '':
        low_check = None

    else:
        print("\nInvalid price, please try again")
        low_check = get_low_price()

    return low_check


def get_high_price():
    '''
    Gets the upper bound for the price range. Returns it as a string or None if N/A
    '''
    print("\nWhat is the highest price range you are looking for?")
    price_high = input()

    if price_high.isnumeric() and (int(price_high) == 1 or int(price_high) == 2 
        or int(price_high) == 3 or int(price_high) == 4):
        high_check = price_high

    elif price_high == '':
        high_check = None

    else:
        print("\nInvalid price, please try again")
        high_check = get_high_price()

    return high_check

'''
The following functions are the main functions to run the whole UI and general helper functions for it
'''

def check_date(date):
    '''
    Checks to see if a date is valid
    Returns the date as a date object if yes and returns None if no
    '''
    if len(date) == 10 and date[2] == '/' and date[5] == '/':
        if date[0:2].isnumeric() and date[3:5].isnumeric() and date[6:10].isnumeric():
            month = int(date[0:2])
            day = int(date[3:5])
            year = int(date[6:10])

            if month >= 1 and month <= 12:
                if day >= 1 and day <= 31:
                    date_object = datetime.date(year, month, day)

                    if date_object <= dt.today():
                        return date_object

    else:
        return None


def find_user_info():
    '''
    Prompts the user for their userID. If the userID exists in the database, returns True and their userID.
    If the userID doesn't exist in the database returns False and their userID
    '''
    print("Input your user ID")
    userID = input()
    matching_info = df.check_user_exists(userID)

    if not matching_info:
        print("""We do not have a matching user ID. 
            \nIf you are a new user, type "yes" otherwise input "no" to try again""")
        new_user = input()
        if new_user == 'no':
            exists = find_user_info()
        elif new_user == 'yes':
            exists = (False, userID)
        else:
            print("Invalid input, please try again")
            exists = find_user_info()

    else:
        exists = (True, userID)

    return exists


def looking_for(userID):
    '''
    Prompts the user to input what they are looking for and does what they request
    '''
    print("")
    print("""Input 1 if you want to submit a new eating entry
        \nInput 2 if you want a recommendation
        \nInput 3 if you want to view the existing data on your eating habits""")

    looking_for = input()

    if looking_for == '1':
        new_entry(userID)

    elif looking_for == '2':
        try_new = get_try_new()
        print("""You will be prompted for inputs.
            \nPlease follow the format indicated and if you don't have a preference press enter""")
        get_recommendation(userID, try_new)

    elif looking_for == '3':
        get_data(userID)

    else:
        print("Invalid input, please try again")
        looking_for()
    

def something_else():
    '''
    Asks the user if they want to do something. Returns True if yes and False if no
    '''
    print("Would you like to do something else? Input yes or no")
    something = input()

    if something == 'yes':
        wants_something = True

    elif something == 'no':
        wants_something = False

    else:
        print("Invalid input, please try again")
        wants_something = something_else()

    return wants_something


def main():
    '''
    The user interface begins here when the interface file is run
    '''
    df.check_user_info_df_exists()
    existing_user, userID = find_user_info()

    print("Welcome, " + userID + "!")

    if existing_user == False:
        print("\nAs a new user, you have to input an eating entry before proceeding")
        new_entry(userID)
    else:
        looking_for(userID)

    something = something_else()
    
    #keeps asking the user if they want something else until they say they are done
    while something:
        looking_for(userID)
        something = something_else()

if __name__ == "__main__":
    main()