import datetime
import dataviz_final as df
import dataviz as d

existing_user, userID = find_user_info()
if existing_user == False:
    print("As a new user, you have to input an eating entry before proceeding")
    new_entry(userID)
else:
    looking_for(userID)
something_else = something_else
while something_else:
    looking_for()
    something_else = something_else()

def find_user_info():
    '''
    Prompts the user for their userID. If the userID exists in the database, returns True and their userID.
    If the userID doesn't exist in the database returns False and their userID
    '''
    print("Input your user ID (formatted as firstnamelastname with your corresponding information)")
    userID = input()
    matching_info = df.check_user_exists(userID)
    if not matching_info:
        print("""We do not have a matching user ID. 
            \nIf you are a new user input yes otherwise input no to try again""")
        new_user = input()
        if new_user == 'no':
            find_user_info()
        elif new_user == 'yes':
            return False, userID
        else:
            print("Invalid input, please try again")
            find_user_info()
    else:
        return True, userID

def looking_for(userID):
    '''
    Prompts the user to input what they are looking for and does what they request
    '''
    print("""Input entry if you want to submit a new eating entry
        \nInput recommendation if you want a recommendation
        \nInput data if you want to view the exisitng data on your eating habits""")
    looking_for = input()
    if looking_for == 'entry':
        new_entry(userID)
    elif looking_for == 'recommendation':
        #ensure try_new works
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
    '''
    Asks the user if they want to do something. Returns True if yes and False if no
    '''
    print("Would you like to do something else? Input yes or no")
    something_else = input
    if something_else == 'yes':
        return True
    elif something_else == 'no':
        return False
    else:
        print("Invalid input, please try again")
        something_else()

def new_entry(userID):
    '''
    Creates a new entry for the user. Takes in the userID
    '''
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
    print("""You will be asked to input a range of dates on which you would like data on. 
        \nIf for either start or end date you would like it to not have bounds just press enter""")
    print("What date would you like the data to start from?")
    start_date = input()
    if start_date == '':
        start_check = None
    else:
        start_check = check_date(start_date)
        if start_check == None:
            print("Invalid start date, please try again")
            get_data()
    print("What date would you like the data to end on?")
    end_date = input()
    if end_date == '':
        end_check = None
    else:
        end_check = check_date(end_date)
        if end_check == None:
            print("Invalid end date, please try again")
            get_data()
    if end_check != None and start_check != None:
        if end_check > start_check:
            print("The end date preceds the start date, please try again")
            get_date()
    #get the data visualisation based on start_check and end_check
    #put the print statement of data being successfully visualised

def get_recomendation(userID, try_new):
    '''
    Gets a reccomendation for the user. Takes in the userID and a boolean True 
    if they want to try something new and False if they want to input what they
    are looking for
    '''
    if not try_new:
        tags = get_tags()
        #empty string if no tags inputed
    else:
        tags = None
        #check which type of input will go into tags if the user wants a new rec
    open_time = get_open_time()
    close_time = get_close_time()
    zipcode = get_zipcode()
    rating = get_rating()
    price_range = get_price_range()
    #get the reccomendations
    #put the print statment of reccomendations being successfully recieved

def get_try_new():
    '''
    Asks the user if they would like a reccomendation based on specific inputs
    or based on things they haven't tried yet. Returns True if they want something
    new or False if they want something specific
    '''
    print("""Input 1 if you would like to get restaurant recomendations based on specific inputs
        \nInput 2 if you would like restaurant recommendations selected based on things you haven't tried yet""")
    try_new = input()
    if try_new == '1':
        return False
    elif try_new == '2':
        return True
    else:
        print("Invalid input, please try again")
        get_try_new()

def check_date(date):
    '''
    Checks to see if a date is valid
    Returns the date as a date object if yes and returns None if no
    '''
    if len(date) == 10 and date[2] == '/' and date[5] == '/':
        if date[0:2].ismmumeric() and date[3:5].isnumeric() and date[6:10].isnumeric():
            month = int(date[0:2])
            day = int(date[3:5])
            year = int(date[6:10])
            if month >= 1 and month <= 12:
                if day >= 1 and day <= 31:
                    date_object = datetime(year, month, day)
                    if date_object <= datetime.now():
                        return date_object
    else:
        return None

'''
The following functions are helpers for inputing a new entry
'''

def get_date():
    '''
    Gets the date for which the entry will be submitted. Returns a date object
    '''
    print("""Input the day you ate the entry you would like to submit. 
        \n(Input it in mm/dd/yyyy format)""")
    date = input()
    date_check = check_date(date)
    if date_check == None:
        print("Not a valid date inputed, please try again")
        get_date()
    else:
        return date_check

def get_restaurant():
    '''
    Gets the restaurant for the entry that will be added. Returns a string for the 
    restaurant or None if N/A
    '''
    print("Input the name of the restaurant you ate at for this entry. (Press enter if N/A)")
    restaurant = input()
    if restaurant == '':
        return None
    else:
        return restaurant

def get_price():
    '''
    Gets the price of the meal for the entry that will be added. Returns a float or None
    if N/A
    '''
    print("""Input the price of the meal you ate for this entry. 
        \n(Only input numbers with two decimal points eg. 10.30 for $10.30 or press enter if N/A)""")
    price = input()
    if price[len(price) - 3] == '.' and price.isnumeric():
        return float(price)
    elif price == '':
        return None
    else:
        print("Not a valid price, please try again")
        get_price()

def get_user_rating():
    '''
    Gets the user rating for the meal entry. Returns a float
    '''
    print("Input your rating of this meal entry. (Input a value between 1-5 and you may input a decimal.)")
    user_rating = input()
    if user_rating.isnumeric():
        if int(user_rating) >= 1 and int(user_rating) <= 5:
            return float(user_rating)
    else:
        print("Not a valid rating, please try again")
        get_user_rating()
    
def get_cuisine():
    '''
    Gets the cuisine for the meal entry. Returns a string of the cuisine
    '''
    print("Input the cuising for this meal entry. (See below for cuisine options and input it as listed)")
    cuisine_options = d.get_tags()
    #find a more succint way of showing cuisine options
    print(cuisine_options)
    cuisine = input()
    if cuisine in cuisine_options:
        return cuisine
    else:
        print("Not a valid cuisine, please try again")
        get_cuisine()


'''
The following functions are helpers for getting reccomendations
'''

def get_tags():
    '''
    Gets the tags for the type of restaurant the user is looking for.
    Returns the tags as a string or None if N/A
    '''
    print("""What kind of restaurant are you looking for? 
        \nInput tags with a space in between or input suggest to get a list of suggested tags""")
    tags_words = input()
    if tags_words == 'suggest':
        #get list of all tags and words and print it
        get_tags()
    else:
        return tags_words

def get_open_time():
    '''
    Gets the latest time the user would like the restaurant to open by.
    Returns a string of the time or None if N/A
    '''
    print("""What is the latest time you would like the restaurant to be open by? 
        \nInput in 24 hour format eg. 1400 for 2:00PM""")
    open_time = input()
    if len(open_time) == 4 and open_time.isnumeric():
        if int(open_time) >= 0 and int(open_time) <= 2359:
            return open_time
        else:
            print("Incorrect input, please try again")
            get_open_time()
    elif open_time == '':
        return None
    else:
        print("Incorrect input, please try again")
        get_open_time()

def get_close_time():
    '''
    Gets the earliest time the user would like the restaurant to close at.
    Returns None if N/A
    '''
    print("""What is the earliest time would you like the restaurant close by? 
        \nInput in 24 hour format eg. 1400 for 2:00PM. If you want it to close after midnight.
        \nAdd additional hours to 2400 eg 2700 for 3:00AM.""")
    close_time = input()
    if len(close_time) == 4 and close_time.isnumeric():
        if int(close_time) >= 0:
            return close_time
        else:
            print("Incorrect input, please try again")
            get_open_time()
    elif close_time == '':
        return None
    else:
        print("Incorrect input, please try again")
        get_open_time()

def get_zipcode():
    '''
    Asks which zipcode the user would like the restaurant to be in. 
    Returns the zipcode as a string or None if N/A
    '''
    print("Which zipcode would you like the restaurant to be in?")
    zipcode = input()
    if len(zipcode) == 5 and zipcode.isnumeric():
        return zipcode
    elif zipcode == '':
        return None
    else:
        print("Incorrect input, please try again")
        get_zipcode()

def get_rating():
    '''
    Asks the user for the minimum rating they would like for recommendations
    Returns the rating as a string or None if N/A
    '''
    print("""What is the minimum rating you would like for the restaurants? 
        \nInput a rating between 1 and 5 and a decimal can be inputed""")
    rating = input()
    if rating.isnumeric() and float(rating) >= 0 and float(rating) <= 5:
        return rating
    elif rating == '':
        return None
    else:
        print("Incorrect input, please try again")
        get_rating()

def get_price_range():
    '''
    Asks the user what price range they would like the recommendations to be in.
    Returns the price range as a string or None if N/A
    '''
    print("""What price range are you looking for? 
        \nInput an integer between 1 and 4
        \n1 represents under $10, 2 represents $11-$30, 3 represents $31-$60, and 4 represents above $61""")
    price = input()
    if price.isnumeric() and (int(price) == 1 or int(price) == 2 or int(price) == 3 or int(price) == 4):
        return price
    elif price == '':
        return None
    else:
        print("Incorrect input, please try again")
        get_price()