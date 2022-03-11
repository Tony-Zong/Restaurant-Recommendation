# Restaurant-Recommendation
This is the group project repository for CMSC 12200. The project aims to create a software that provides restaurant recommendations in Chicago and tracks the ordering history and eating habits of the user. 

## Introduction and Background
* There exist many different platforms for ordering food (i.e. GrubHub, UberEats, etc.) and this is a way to centralize all your orders (take-out & dine-in) and see them together 
* Restaurant recommendations are particularly useful in urban and metropolitan areas like Chicago that have high densities of restaurants 
* Can be applicable to a large audience since everyone has to eat and the personalization of the recommendations makes it that everyone can enjoy it 
* The project is based on the restaurants in Chicago 

## Software Description 
The application provides a text-based user-interface for storing information about user eating history, providing useful data visualization for users to understand their eating habits, and providing restaurant recommendations to users based on search parameters and eating history. A focus is placed on restaurants in the greater Chicago area. The interface is currently based in terminal.

Upon application start-up, users register a user id of their choosing, which is then associated with their eating history. When a user inputs their eating history, they will be asked for the following information: username, restaurant name, cuisine type, a user rating, and finally the cost of the meal. This data is stored for use in data visualization and restaurant recommendation, and is retained for future uses of the application. 

Users are given the option of viewing data visualizations based on their inputted eating history, and the parameters of start and end date, which take a subset of the user's inputted data between the given dates, if they exist. Three data visualizations will be produced by interacting with this feature. The first visualization shows a user's eating frequency by cuisine type, the second shows a user's total spending by cuisine type, and the third shows a user's ratings by cuisine type that they have given to restaurants.

Users are also given the option of requesting "Standard" or "Try Something New" restaurant recommendations, along with desired search parameters including keywords, opening times, minimum star rating, price, etc. In the former, recommendations are based soley upon search parameters at the time of the request. In the latter, the user's eating history is considered alongside search parameters to recommend restaurants that differ from what the user has eaten recently. 10 recommendations are initially made, with an additional 20 recommendations given if desired. Recommendations are initially given as a list of restaurant names, after which users may request further information about the restaurants including address, hours, price, and rating.

## Running the Application
From the `Restaurant-Recommendation` directory, run the follwing command to access the user interface: `python3 UI/interface.py`. From there, follow the prompts to create or enter existing user id, enter user eating history, and request restaurant recommendations.

## Description of the files 

### `scraping` folder 

`cook_zips.csv`: CSV that stores all the zipcodes in Cook County. We got it from [Zillow](https://www.zillow.com/browse/homes/il/cook-county/). The zipcodes will be used when we crawl Yelp for restaurant URLs. 

`url_crawler.py`: script that crawls the Yelp website to get the URLs for restaurants. We crawl Yelp by first specifying the zipcode in the searching URL and then going through all the pages under this zipcode and extracting the links to restaurants. 

`restaurant_urls3.csv`: CSV that stores all the restaurant URLs. 

`scraping_all.py`: script that scrapes the information about each restaurant in each's website page. The information includes phone, address, website, num_review, hours, tags, rating, price, words (words in the restaurant name). 

`scraping_final.py`: script that goes through all the restaurant URLs, scrapes each page, and stores all the information into a master dictionary. The dictionary is then dumped into `yelp_data.pickle`, which is now stored in the `data_processing` folder. 

`numbered_urls.py`: script that finds all the URLs among the first 1050 that ends with a number. We needed to re-scrape these due to some reasons that has to do with how the scraping function works. We then iterated through the URLs in this file and scraped these restaurants again. 

### `data_processing` folder 

`process_inspection_data.ipynb`: script that loads in the inspection data and conducts some basic data pre-processing.  

`inspection_data.pkl`: Pandas data frame that stores the inspection data.

`merge_inspection.py`: script that reads in the inspection data and merge it with the Yelp data. 

`yelp_and_inspection.pickle`: Pandas data frame that stores the merged data. 

`clean_df.py`: scripts that further cleans the data frame for it to be ready to be split into the tables for the database. 

`clean_df.pickle`: Pandas data frame that stores the cleaned, finalized data frame. 

`split_table.py`: scripts that splits the cleaned data frame into two tables. `words_table.csv` has two columns: `id` for restaurnt id; `word` for tags and words in the restaurant name. `rest_info.csv` stores the rest of the information about each restaurant (`rest_name`, `phone`, `street`, `city`, `zipcode`, `website`, `num_review`, `bayes`, `vio_occ`, `time_start`, `time_end`, `risk_val`, `rating`, `price`). 

`create_rest_db.sql`: SQL that specifies the scheme of the database. 

### `UI` folder 

`rest_db.db`: SQL database storing all information associated with restaurants for possible recommendation. Consists of two tables. `rest_info` holds restaurant information to be displayed any time information is requested. `words_table` stores the culinary tags and words associated with the restaurant, to be used for keyword searches.

`dataviz_final.py`: script providing data visualization as prompted by `interface.py`, displays visualizations in window and writes to pdf in the directory. Also holds functions for storage of user data. 

`recommendation.py`: script providing back-end functions to `interface.py`, specifically recommendation functions that return top restaurants based on search parameters along with relevant information

`interface.py`: provides the text-based user interface for the application, with input dictated by keyboard input to the terminal

### `archive` folder

Other files that we created during the development process. They are now archived. 



## Progress 

Originally, the data sources we were considering were Yelp and OpenTable. Yelp contains the info of the most restaurants, while OpenTable is a site for making reservations (and we originally wanted to provide info about this in our software). However, after we examined Opentable for hours, we concluded that it contains relatively little information we want (since it only has info for restaurants that's in its 'business network') and since it's also not very feasible to scrape, we decided to choose another data source; 

Then, we looked for alternative data sources and decided to use the [Chicago Health Inspection data](https://www.kaggle.com/chicago/chi-restaurant-inspections). It contains information on health risk level and violations noted during the inspection for probably all the restaurants in the greater Chicago area. So presumably the restaurant coverage of this datset and Yelp would be approximatey the same. Also, health risk information would always be helpful for consumers.   

Then we scraped the Yelp website for data about restaurants in the pan-Chicago area: 

1. we first crawled the Yelp website for URLs of the restaurant webpages (see `scraping/url_crawler.py`);

2. then we wrote the script to scrape restaurant webpages iteratively (see `scraping/scraping_all`, `scraping/scraping_final`). There are many variations since some restaurants' pages don't have certain information. We resolved this by first setting a default value for each variable;  

3. since Yelp will block your IP address if you make too many requests in one time, we also experimented with different solutions to prevent getting blocked, including rotating the free proxies online and adding random time intervals between each request;

we considered the following resources on rotating proxies and free proxy lists online: 

1. https://www.scrapehero.com/how-to-rotate-proxies-and-ip-addresses-using-python-3/ 
2. https://free-proxy-list.net/ 
3. https://geonode.com/free-proxy-list/ 

but, unfortunately, it didn't work out really well 

In the end, we chose to use a somewhat complicated random time interval distribution between requests to ensure the success of making requests and scraping for the data. 

Then, we merged the Yelp data (`data_processing/yelp_data.pickle`) with the inspection data (`data_processing/health-inspections.zip`, `data_processing/inspection_data.pkl`) and got this data frame (`data_processing/yelp_and_inspection.pickle`). The merging is done in `data_processing/merge_inspection.py`. 

Then we cleaned this data frame (see `data_processing/clean_df.py`) to get the final data frame (`data_processing/clean_df.pickle`).

Next, we created the tables for the database (see `data_processing/split_table.py`). See `data_processing/words_table.csv`, `data_processing/rest_info.csv` for the two tables in .csv format. We also have them in .pickle format as well in the `data_processing` folder. 

Then, we created the database (`UI/rest_db.db`) for restaurant recommendation (see `data_processing/create_rest_db.sql`).

While doing that, we have one of our team members working on the data visualization feature (see `UI/dataviz_final.py`). `dataviz_final.py` has two primary purposes: to construct a dataframe out of user-entered eating history and information, and then to subsequently construct 3 types of visualizations to return to the user and store in a PDF. The data frame of user information is stored in `UI/user_info.pickle`. An earlier version of this implementation can be found in the `archive` folder called `data_viz.py`. We discarded it since the way it stores the user data is not tidy. 

Then, we start developing the recommendation algorithm (see `UI/recommendation.py`). It has two parts. One is the standard recommendation, which provides recommendations soley based on the one-time preference of the user provided at the time of request. The other is Try Something New, which also connects with the data frame that stores the user's eating history and provides recommendations that are different from what they ate recently. Broadly, recommendation algorithm calculates a bayesian average for the entire set of restaurants based on star rating and number of reviews. For each request, the bayesian average is weighted alongside the number of keywords that match search parameters. Restaurants are then sorted based on these criteria to provide the top 10 (or 30) restaurant recommendations.

In the meantime, another team member works on the implementation of the UI (see `UI/interface.py`) and iteratively updates it as `UI/recommendation.py` and `dataviz.py` are updated. 

## Remarks 

