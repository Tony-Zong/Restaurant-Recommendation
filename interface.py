def find_user_info():
    print("What is you user ID?")
    userID = input()
    #userinfo will be the dataframe with all the information
    #get matching_info from function
    if matching_info == None:
        print("We do not have a matching userID. If you are a new user input yes otherwise input no to try another userID")
        new_user = input()
        if new_user == 'no':
            find_user_info()
        elif new_user == 'yes':
            print("As a new user, you have to input some of your eating preferences before proceeding")
            #call function to get a new entry in
            new_entry()
        else:
            print("Incorrect input, please try again")
            find_user_info()
    else:
        print("Input entry if you want to submit a new eating entry or input reccomendation if you want a reccomendation")
        looking_for = input()
        if looking_for == 'entry':
            #call function to get a new entry in
            new_entry()
        elif looking_for == 'reccomendation':
            try_new = get_try_new()
            print("You will be prompted for inputs. Please follow the format indicated and if you don't have a preference press enter")
            if try_new == False:
                tags = get_tags()
            questions_for_reccomendation()
            #call function to get a reccomendation
        else:
            print("Incorrect input, please try again")
            find_user_info()

def new_entry():
    print("Information asked about what they ate")
    #returns needed information on what was eaten

def questions_for_reccomendation():
    open_time = get_open_time()
    close_time = get_close_time()
    zipcode = get_zipcode()
    rating = get_rating()
    price = get_price()

def get_tags():
    print("What kind of restaurant are you looking for? (Input tags with a space in between or input suggest to get a list of suggested tags)")
    tags_words = input()
    if tags_words == 'suggest':
        #get list of all tags and words and print it
        get_tags()
    elif tags_words == '':
        return None
    else:
        return tags_words

def get_open_time():
    print("What time would you like the restaurant to be open by? (input in 24 hour format eg. 1400 for 2:00PM)")
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
    print("What time would you like the restaurant to be closed by? (input in 24 hour format eg. 1400 for 2:00PM. If you want it to close after midnight, add additional hours to 2400 eg 2700 for 3:00AM)")
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
    print("What is the minimum rating you are looking for? (rated out of 5 and a decimal can be inputed)")
    rating = input()
    if rating.isnumeric() and float(rating) >= 0 and float(rating) <= 5:
        return rating
    elif rating == '':
        return None
    else:
        print("Incorrect input, please try again")
        get_rating()

def get_price():
    print("What price range are you looking for? (input an integer between 1 and 4 where 1 represents under $10, 2 represents $11-$30, 3 represents $31-$60, and 4 represents above $61)")
    price = input()
    if price.isnumeric() and (int(price) == 1 or int(price) == 2 or int(price) == 3 or int(price) == 4):
        return price
    elif price == '':
        return None
    else:
        print("Incorrect input, please try again")
        get_price()

def get_try_new():
    print("Input 1 if you would like to get a reccomendation based on specific inputs or 2 if you would like a randomly selected restaurant based on things you haven't tried yet")
    try_new = input()
    if try_new == 1:
        return True
    elif try_new == 2:
        return False
    else:
        print("Incorrect input, please try again")
        get_try_new()