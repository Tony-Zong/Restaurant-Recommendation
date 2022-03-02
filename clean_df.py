# Cleans dataframe of yelp and health inspection data, prepares for splitting into 
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pickle5
import re


# TO DO: CHECK STREET VALUES AND CONVERT TO NAN CORRECTLY, split hours to opening and clsoing, convert risk to numbers, 


# Load df
f = open('yelp_and_inspection.pickle', 'rb')
df = pickle5.load(f)
f.close()


# Change column names for consistency
df.rename(columns={'Risk': 'risk', 'Violations': 'violations'}, inplace=True)


# Fix column data types, may have to do others later
convert_dict = {
    'rest_name': str,
    'phone': str,
    'website': str,
    'num_review': int,
    'hours': str,
    'risk': str,
    'violations': str
}
df = df.astype(convert_dict)



# Change default not-found values to NaN
replace_dict = {'num_review': {-1: np.nan}, 'rating': {-1: np.nan}, 'phone': {-1: 'Not available'}} # add the others later
df.replace(replace_dict, inplace=True)


# Calculate Bayesian Average from num reviews and avg rating
df['weighted'] = df['num_review'] * df['rating']
C = df['num_review'].quantile(q=0.4) # adjusted manually by looking at resulting distribution
m = df['rating'].sum() / df['num_review'].sum()
df['bayes'] = (df['rating'] * df['num_review'] + C * m) / (df['num_review'] + C)


# Split hours to opening and closing
# If unknown, set time start and end 
def split_start(row):
    if row['hours'] == 'Unkown' or row['hours'] == 'Unknown':
        return 'Unknown'
    return row['hours'].split(' - ')[0]

def split_end(row):
    if row['hours'] == 'Unkown' or row['hours'] == 'Unknown':
        return 'Unknown'
    #print(row['hours'].split(' - '))
    return row['hours'].split(' - ')[1]

def convert_start(row):
    if row['time_start'] == 'Unknown':
        return 'Unknown'
    #print(tuple(row['time_start'].split(' ')))
    time, am = tuple(row['time_start'].split(' '))
    time = int(time.replace(':', ''))
    if am == 'pm':
        time += 1200
    return time

def convert_end(row):
    if row['time_end'] == 'Unknown':
        return 'Unknown'
    if len(row['time_end'].split(' ')) > 2:
        return 'Unknown'
    time, am = tuple(row['time_end'].split(' '))
    time = int(time.replace(':', ''))
    if am == 'pm':
        time += 1200
    else:
        time += 2400
    return time
    
df['time_start'] = df.apply(lambda row: split_start(row), axis=1)
df['time_end'] = df.apply(lambda row: split_end(row), axis=1)
print(df['time_end'])
df['time_end'].to_csv(r'time_end.txt', header=None, index=None, sep=' ', mode='a')
df['time_start'] = df.apply(lambda row: convert_start(row), axis=1)
df['time_end'] = df.apply(lambda row: convert_end(row), axis=1)

print(df['time_start'])
print(df['time_end'])


# Create boolean column indicating if health violation was found during inspection
df['vio_occ'] = df['violations'].any()


# Convert Risk to numbers and make numeric (only one integer in each value, 1 is high risk 3 is low)
# might not need to do this
def output_risk_val(row):
    if not row['risk']:
        return -1
    first_digit = re.search(r'\d', row['risk'])
    if not first_digit:
        return -1
    return first_digit.group(0)

df['risk_val'] = df.apply(lambda row: output_risk_val(row), axis=1)
print(df['risk'])
print(df['risk_val'])
print(df['vio_occ'])

#Clean up
df.drop(['weighted', 'state', 'risk', 'violations'], axis=1, inplace=True)


# Store in pickle
f = open('clean_df.pickle', 'wb')
pickle5.dump(df, f, pickle5.HIGHEST_PROTOCOL)
f.close()