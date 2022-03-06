def find_user_info():
    print("What is you user ID?")
    userID = input()
    #userinfo will be the dataframe with all the information
    matching_info = userinfo.loc[userinfo['UserId'] == userID]
    if matching_info == None:
        print("We do not have a matching userID. If you are a new user input yes otherwise input no to try another userID")
        new_user = input()
        if new_user == 'no':
            find_user_info()
        elif new_user == 'yes':
            print("As a new user, you have to input some of your eating preferences before proceeding")
            new_entry()
        else:
            print("Incorrect input, please try again")
            find_user_info()
    else:
        print("Input entry if you want to submit a new eating entry or input reccomendation if you want a reccomendation")
        looking_for = input()
        if looking_for == 'entry':
            new_entry()
        elif looking_for == 'reccomendation':
            print("You will be prompted for inputs. Please follow the format indicated and if you don't have a preference press enter")
            questions_for_reccomendation()
        else:
            print("Incorrect input, please try again")
            find_user_info()

def new_entry():
    print("Information asked about what they ate")
    #get info on what they ate and add it to the dataframe of user data

def questions_for_reccomendation():
    tags = get_tags()
    open_time = get_open_time()
    close_time = get_close_time()

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
