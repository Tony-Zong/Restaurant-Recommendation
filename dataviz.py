import pickle
import pickle5 as p

# Tasks
# 1. create a set of all the tags types / other relevant info
# 2. design dummy data for data viz
# 3. code for each type of data viz based on data
# 4. design UI / prompts for user to input data from database

# Types of Data Viz:
# 1. A pie chart that summarizes how often the diner eats each type of food (such as Asian food, Mexican food, etc.) 
# 2. A bar chart summarizing the ratings a user gives to each type of food
# 3. A bar chart that summarizes the frequencies of ordering on each weekday over the past month
# 3. A rating from (least liked)0-10(most liked) given to each type of food: 
#       a weighted score calculated from “user’s frequency of ordering this type of 
#       food” and “user’s rating given to this type of food”
# 4. A rating from (least likely to order)0-10(most likely to order) 
#       given to each period of day“mean +- 1 stdev” to summarize the average 
#       price range of all the user’s orders
# 5. Which type of food gains the highest rating from the user?
# 6. Which restaurant does the user order from most frequently?
# 7. Which specific cuisine does the user most frequently order?

#f = open('data.pickle', 'rb')
#all_rest = p.load(f)

#f = open('data.pickle', 'wb')
#pickle.dump(all_rest, f, pickle.HIGHEST_PROTOCOL)
#f.close()




## TASK 1
def find_info(csv):
    '''
    '''
    f = open(csv, 'rb')
    all_rest = p.load(f)
    for rest in all_rest:
        return rest




















