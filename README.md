# Restaurant-Recommendation
This is the group project repository for CMSC 12200. The project aims to create a software that provides restaurant recommendations in Chicago and tracks the ordering history and eating habits of the user. 

## Introduction and Background
* There exist many different platforms for ordering food (i.e. GrubHub, UberEats, etc.) and this is a way to centralize all your orders (take-out & dine-in) and see them together 
* Restaurant recommendations are particularly useful in urban and metropolitan areas like Chicago that have high densities of restaurants 
* Can be applicable to a large audience since everyone has to eat and the personalization of the recommendations makes it that everyone can enjoy it 
* The project is based on the restaurants in Chicago 


## Progress 

Originally, the data sources we were considering were Yelp and OpenTable. Yelp contains the info of the most restaurants, while OpenTable is a site for making reservations (and we originally wanted to provide info about this in our software). However, after we examined Opentable for hours, we concluded that it contains relatively little information we want (since it only has info for restaurants that's in its 'business network') and since it's also not very feasible to scrape, we decided to choose another data source; 

Then, we looked for alternative data sources and decided to use the [Chicago Health Inspection data](https://www.kaggle.com/chicago/chi-restaurant-inspections). It contains information on health risk level and violations noted during the inspection for probably all the restaurants in the greater Chicago area. So presumbaly the restaurant coverage of this datset and Yelp would be approximatey the same. Also, health risk information would always be helpful for consumers.   

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

Then, we merged the Yelp data (`data_processing/yelp_data.pickle`) with the inspection data (`data_processing/health-inspections.zip`) and got this data frame (`data_processing/yelp_and_inspection.pickle`). 

Then we cleaned this data frame (see `data_processing/clean_df.py`) and get the final data frame (`data_processing/clean_df.pickle`).

Next, we created the tables for the database (see `data_processing/split_table.py`). See `data_processing/words_table.csv`, `data_processing/rest_info.csv` for the two tables in .csv format. We also have them in .pickle format as well in the `data_processing` folder. 

Then, we created the database (`rest_db.db`) for reastaurant recommendation (see `data_processing/create_rest_db.sql`).
