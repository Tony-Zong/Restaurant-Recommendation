# Restaurant-Recommendation
This is the group project repository for CMSC 12200. The project aims to create a software that provides restaurant recommendations in Chicago and tracks the ordering history and eating habits of the user. 

## Progress 
examined Opentable (and then finding alternative data sources - Health Inspection data); 
developed the scraping code iteratively (scrape for restaurant urls as well as the real data); 
spent a lot of time trying different solutions to prevent getting blocked by Yelp website (using proxies, adding random time intervals)

we considered the following resources on rotating proxies and free proxy lists online: 
1. https://www.scrapehero.com/how-to-rotate-proxies-and-ip-addresses-using-python-3/ 
2. https://free-proxy-list.net/ 
3. https://geonode.com/free-proxy-list/ 
but, unfortunately, it didn't work out really well. 

In the end, we chose to use a somewhat complicated random time interval distribution between requests to ensure the success of making requests and scraping for the data. 


