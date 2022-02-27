# Cleans dataframe of yelp and health inspection data, prepares for splitting into 

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pickle5


# TO DO: CHECK STREET VALUES AND CONVERT TO NAN CORRECTLY


# Load df
f = open('yelp_and_inspection.pickle', 'rb')
df = pickle5.load(f)
f.close()


# Fix column data types, may have to do others later
df['num_review'] = pd.to_numeric(df['num_review'])


# Change default not-found values to NaN
replace_dict = {'num_review': {-1: np.nan}, 'rating': {-1: np.nan}} # add the others later
df.replace(replace_dict, inplace=True)


# Calculate Bayesian Average from num reviews and avg rating
df['weighted'] = df['num_review'] * df['rating']
C = df['num_review'].quantile(q=0.4) # may want to adjust this, show everyone else
m = df['rating'].sum() / df['num_review'].sum()
df['bayes'] = (df['rating'] * df['num_review'] + C * m) / (df['num_review'] + C)

# plt.hist(df['bayes'])
# plt.show()


# Convert Risk to numbers and make numeric (only one integer in each value, 1 is high risk 3 is low)
# might not need to do this


#Clean up
df.drop(['weighted'], axis=1, inplace=True)


# Store in pickle
f = open('clean_df.pickle', 'wb')
pickle5.dump(df, f, pickle5.HIGHEST_PROTOCOL)
f.close()