import pandas as pd
import pickle5


# Load dictionary from pickle
f = open('yelp_data.pickle', 'rb')
rest_dict = pickle5.load(f)
f.close()


# Convert dictionary to dataframe
df_yelp = pd.DataFrame(rest_dict).transpose()
df_yelp[['street', 'city', 'state', 'zipcode']] = df_yelp['address'].str.rsplit(' ', 3, expand=True)
df_yelp['street'] = df_yelp['street'].str.upper().str.strip()


# Load health_inspection data into dataframe, filter cols to keep
df_inspection = pd.read_csv('food-inspections.csv')

df_inspection.sort_values('Inspection Date', ascending=False, inplace=True)
df_inspection.drop_duplicates(subset='Address', keep='first', inplace=True)

cols_to_keep = ['Address', 'Risk', 'Violations']
df_inspection = df_inspection[cols_to_keep]

df_inspection['street'] = df_inspection['Address'].str.upper().str.strip()


# Ensure same type
df_yelp['street'] = df_yelp['street'].astype('string')
df_inspection['street'] = df_inspection['street'].astype('string')

df_yelp.reset_index(inplace=True)
df_yelp.rename(columns={'index': 'rest_name'}, inplace=True)


# Merge
df_final = pd.merge(df_yelp, df_inspection, on='street', how='left') # will do left join when it works
df_final = df_final[['rest_name', 'phone', 'website', 'num_review', 'hours', 'tags', 'rating', 'price', 'words', 'street', 'city', 'state', 'zipcode', 'Risk', 'Violations']]
df_final.reset_index(inplace=True)
df_final.rename(columns={'index': 'id'}, inplace=True)
df_final['city'] = df_final['city'].str.replace(',','')

# Check if same value is present in both dataframes... they are
#print(df_yelp['street'].str.contains('3357 N LINCOLN AVE').sum())
#print(df_inspection['street'].str.contains('3357 N LINCOLN AVE').sum())

f = open('yelp_and_inspection.pickle', 'wb')
pickle5.dump(df_final, f, pickle5.HIGHEST_PROTOCOL)
f.close()