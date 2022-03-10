import datetime
import dataviz_final as df
import dataviz as d
import recommendation as r
import pandas as pd

def find_user_info():
    '''
    Prompts the user for their userID. If the userID exists in the database, returns True and their userID.
    If the userID doesn't exist in the database returns False and their userID
    '''
    #needs to be checked
    print("Input your user ID (formatted as firstnamelastname with your corresponding information)")
    userID = input()
    matching_info = df.check_user_exists(userID)
    if not matching_info:
        print("""We do not have a matching user ID. 
            \nIf you are a new user input yes otherwise input no to try again""")
        new_user = input()
        if new_user == 'no':
            exits, userID = find_user_info()
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
    #needs to be checked
    print("""Input entry if you want to submit a new eating entry
        \nInput recommendation if you want a recommendation
        \nInput data if you want to view the exisitng data on your eating habits""")
    looking_for = input()
    if looking_for == 'entry':
        new_entry(userID)
    elif looking_for == 'recommendation':
        try_new = get_try_new()
        print("""You will be prompted for inputs.
            \nPlease follow the format indicated and if you don't have a preference press enter""")
        get_recommendation(userID, try_new)
    elif looking_for == 'data':
        get_data()
    else:
        print("Invalid input, please try again")
        looking_for()

def something_else():
    #WORKS
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

def new_entry(userID):
    '''
    Creates a new entry for the user. Takes in the userID
    '''
    #needs to be checked
    date = get_date()
    restaurant = get_restaurant()
    price = get_price()
    user_rating = get_user_rating()
    cuisine = get_cuisine()
    df.add_row(userID, date, restaurant, cuisine, user_rating, price)
    print('Your entry was successfully added')

def get_data(userID):
    '''
    Creates data visualisation for the user. Takes in the userID.
    '''
    #needs to be checked
    print("""\nYou will be asked to input a range of dates on which you would like data on. 
If for either start or end date you would like it to not have bounds just press enter""")
    start_check = get_lower_date()
    end_check = get_upper_date()
    if end_check != None and start_check != None:
        if end_check > start_check:
            print("\nThe end date preceds the start date, please try again")
            get_date()
    #get the data visualisation based on start_check and end_check
    #put the print statement of data being successfully visualised

def get_lower_date():
    #needs to be checked
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
    #needs to be checked
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

def get_recomendation(userID, try_new):
    #needs to be checked
    '''
    Gets a reccomendation for the user. Takes in the userID and a boolean True 
    if they want to try something new and False if they want to input what they
    are looking for
    '''
    if not try_new:
        tags = get_tags()
    else:
        tags = None
    open_time, close_time = get_times()
    zipcode = get_zipcode()
    rating = get_rating()
    price_low, price_high = get_price_range()
    recs = r.recommend(userID, tags, open_time, close_time, zipcode, rating, price_low, price_high, try_new)
    starting_rec = 0
    starting_rec, final_rec = print_recs(recs, starting_rec)
    done = add_info(recs, starting_rec, final_rec)
    while not done:
        done = add_info(recs, starting_rec, final_rec)

def add_info(recs, starting_rec, final_rec):
    #needs to be checked
    print("""\nWould you like to get additional information on any of these restaurants?
Input the integer corresponding for the restaurant if yes.
If you would like to get the subsequent ten restaurants input 0
If you are satisfied with the information press enter""")
    add_info = input()
    possible_rest_nums = list(range(1, 10+1))
    if not add_info.isnumeric() or add_info != '':
        print("\nInvalid input, please try again")
        done = add_info(recs, starting_rec, final_rec)
    elif add_info == '':
        done = True
    elif add_info == '0':
        starting_rec, final_rec = print_recs(recs, starting_rec)
        done = add_info(recs, starting_rec, final_rec)
    elif int(add_info) in possible_rest_nums:
        current_rest = final_rec - int(add_info)
        print(recs.iloc[current_rest])
        done = False
    else:
        print("\nInvalid input, please try again")
        done = add_info(recs, starting_rec, final_rec)
    return done

def print_recs(recs, starting_rec):
    #needs to be checked
    print("\nThese are the restaurants we reccomend:")
    final_rec = startin_rec
    for row in recs:
        restaurant = recs.iloc[final_rec]["rest_name"]
        print(str(final_rec % 10 + 1) + ". " + restaurant)
        final_rec += 1
        if final_rec % 10 == 0:
            break
    if final_rec % 10 != 0:
        "\nThese are all the restaurants we can reccomend based on your inputs"
    return starting_rec, final_rec

def get_try_new():
    #WORKS
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

def check_date(date):
    #WORKS
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
                    date_object = datetime.datetime(year, month, day)
                    if date_object <= datetime.datetime.now():
                        return date_object
    else:
        return None

'''
The following functions are helpers for inputing a new entry
'''

def get_date():
    #WORKS
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
    #WORKS
    '''
    Gets the restaurant for the entry that will be added. Returns a string for the 
    restaurant or None if N/A
    '''
    print("\nInput the name of the restaurant you ate at for this entry. (Press enter if N/A)")
    restaurant = input()
    return restaurant

def get_price():
    #WORKS
    '''
    Gets the price of the meal for the entry that will be added. Returns a float or None
    if N/A
    '''
    print("""\nInput the price of the meal you ate for this entry. 
(Only input numbers with two decimal points eg. 10.30 for $10.30 or press enter if N/A)""")
    price = input()
    if price == '':
        good_price = None
    elif len(price) >= 3:
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
    #works
    '''
    Gets the user rating for the meal entry. Returns a float
    '''
    print("\nInput your rating of this meal entry. (Input an integer between 1-5)")
    user_rating = input()
    if user_rating.isnumeric():
        if int(user_rating) >= 1 and int(user_rating) <= 5:
            good_user_rating = float(user_rating)
        else:
            print("\nNot a valid rating, please try again")
            good_user_rating = get_user_rating()
    else:
        print("\nNot a valid rating, please try again")
        good_user_rating = get_user_rating()
    return good_user_rating
    
def get_cuisine():
    #NEEDS FIXING
    '''
    Gets the cuisine for the meal entry. Returns a string of the cuisine
    '''
    print("\nInput the cuising for this meal entry. (See below for cuisine options and input it as listed)")
    cuisine_options = d.get_tags()
    #find a more succint way of showing cuisine options
    print(cuisine_options)
    #doesn't have the cusine options outputting
    cuisine = input()
    if cuisine in cuisine_options:
        good_cuisine = cuisine
    else:
        print("\nNot a valid cuisine, please try again")
        good_cuisine = get_cuisine()
    return good_cuisine


'''
The following functions are helpers for getting reccomendations
'''

def get_tags():
    #WORKS but still need to implement the get list of tag words
    '''
    Gets the tags for the type of restaurant the user is looking for.
    Returns the tags as a string or None if N/A
    '''
    print("""\nWhat kind of restaurant are you looking for? 
Input tags with a space in between or input suggest to get a list of suggested tags""")
    tags_words = input()
    if tags_words == 'suggest':
        #get list of all tags and words and print it
        final_tags = get_tags()
    else:
        final_tags = tags_words
    return final_tags

def get_times():
    #WORKS
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
    #WORKS
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
    #WORKS
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
    #WORKS
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
    #WORKS
    '''
    Asks the user for the minimum rating they would like for recommendations
    Returns the rating as a string or None if N/A
    '''
    print("""\nWhat is the minimum rating you would like for the restaurants? 
Input an integer between 1 and 5""")
    rating = input()
    if rating.isnumeric() and float(rating) >= 1 and float(rating) <= 5:
        good_rating = rating
    elif rating == '':
        good_rating = None
    else:
        print("\nInvalid rating, please try again")
        good_rating = get_rating()
    return good_rating

def get_price_range():
    #WORKS
    '''
    Asks the user what price range they would like the recommendations to be in.
    Returns the price range as a string or None if N/A
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
    #WORKS
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
    #WORKS
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

def main():
    #needs to be checked
    df.check_user_info_df_exists()
    existing_user, userID = find_user_info()
    if existing_user == False:
        print("\nAs a new user, you have to input an eating entry before proceeding")
        new_entry(userID)
    else:
        looking_for(userID)
    something_else = something_else
    while something_else:
        looking_for()
        something_else = something_else()