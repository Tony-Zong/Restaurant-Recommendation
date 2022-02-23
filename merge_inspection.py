import pandas as pd
import pickle5

# Load dictionary from pickle
f = open('data.pickle', 'rb')
rest_dict = pickle5.load(f)

# Convert dictionary to dataframe
df_yelp = pd.DataFrame(rest_dict).transpose()

df_yelp[['street', 'city', 'state', 'zipcode']] = df_yelp['address'].str.rsplit(' ', 3, expand=True)
df_yelp['street'] = df_yelp['street'].str.upper()
#df_yelp['zipcode'] = df_yelp['address'].str.split(' ',)[-1] # inefficient but not that much data so it's lit
#df_yelp['state'] = df_yelp['address'].str.split(' ')[-2].upper()
#df_yelp['city'] = df_yelp['address'].str.split(' ')[-3][:-1].upper()
#df_yelp['street'] = df_yelp['address'].str.split(' ')[:-3].upper()
print(df_yelp.columns)
#print(df_yelp.dtypes)

print(len(df_yelp))

# Load health_inspection data into dataframe, filter cols to keep
df_inspection = pd.read_csv('food-inspections.csv')
df_inspection.sort_values('Inspection Date', ascending=False, inplace=True)
df_inspection.drop_duplicates(subset='Address', keep='first', inplace=True)
cols_to_keep = ['Address', 'Risk', 'Violations']
df_inspection = df_inspection[cols_to_keep]
df_inspection['street'] = df_inspection['Address'].str.upper()
print(df_inspection.columns)
#print(df_inspection.dtypes)

# Merge
df_yelp['street'] = df_yelp['street'].astype('string')
df_inspection['street'] = df_inspection['street'].astype('string')

#print(df_yelp.dtypes)
#print(df_inspection.dtypes)
print(df_yelp['street'])
print(df_inspection['street'])

df_final = pd.merge(df_yelp, df_inspection, on='street')

print(df_final)

print(df_inspection['street'].str.contains('3357 N LINCOLN AVE').sum())