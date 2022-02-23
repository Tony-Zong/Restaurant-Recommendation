import pickle
import pickle5 as p


# Token : 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
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
def get_tags(csv):
    '''
    '''
    all_tags = set()
    f = open(csv, 'rb')
    all_rest = p.load(f)
    for rest in all_rest.values():
       for tag in rest['tags']:
           all_tags.add(tag)
    return all_tags

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













