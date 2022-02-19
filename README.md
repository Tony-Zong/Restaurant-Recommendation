# Restaurant-Recommendation
This is the group project repository for CMSC 12200. The project aims to create a software that provides restaurant recommendations in Chicago and tracks the ordering history and eating habits of the user. 


## Progress 
examined Opentable and concluded that using it is not so helpful for our project; (Dylan elaborates)

looked for alternative data sources - Health Inspection data; (Matt elaborates)

scraped the Yelp website for data about restaurants in the pan-Chicago area: 

    1. crawled the Yelp website for URLs of the restaurant webpages; (Matt elaborates)

    2. developed the code to scrape a restaurant webpage iteratively. There are many variations since some restaurants' pages don't have certain information. We resolved this by first setting a default value for each variable;  

    3. spent a lot of time trying different solutions to prevent getting blocked by Yelp website (using proxies, adding random time intervals)

we considered the following resources on rotating proxies and free proxy lists online: 

    1. https://www.scrapehero.com/how-to-rotate-proxies-and-ip-addresses-using-python-3/ 
    2. https://free-proxy-list.net/ 
    3. https://geonode.com/free-proxy-list/ 
but, unfortunately, it didn't work out really well. (Matt elaborates)

In the end, we chose to use a somewhat complicated random time interval distribution between requests to ensure the success of making requests and scraping for the data. 


