from bs4 import BeautifulSoup
import requests
import re

def get_info(soup, rest_dic):
    '''

    '''

    # restaurant name
    name = soup.find_all('h1', class_="css-1x9iesk")[0].text

    # indexer for restaurant name
    lower_name = name.lower()
    name_words = lower_name.split()
    words_set = set(name_words)

    # phone number
    phone = soup.find_all('p', class_="css-1h7ysrc")
    phoneret = phone[-2].text
    
    # address
    address = soup.find_all('p', class_="css-1ccncw")
    addressret = address[0].text

    # restaurant website
    web = soup.find_all('a', class_="css-10y60kr")
    webret = web[2].get('href')
    if len(webret) == 0 or 'map' in webret:
        webret = -1

    # number of reviews
    tags = soup.find_all('span', class_="css-1yy09vp")
    num_review_str = tags[0].text
    num_review = re.search('^[0-9]+', num_review_str)[0]

    # hours
    time = tags[-1].text
    if 'AM' not in time or 'PM' not in time:
        time = -1 

    # restaurant tags
    rest_tags = set()
    for i in range(1, len(tags)):
        tag = tags[i].find_all('a', class_= "css-1422juy")
        if len(tag) != 0:
            tag_text = tag[0].text
            if 'AM' not in tag and 'PM' not in tag_text:
                rest_tags.add(tag_text)

    # rating
    rating_tag = soup.find_all('div', class_="css-i-stars__09f24__foihJ i-stars--large-4__09f24__jGrzl border-color--default__09f24__NPAKY overflow--hidden__09f24___ayzG")
    rating_str = re.findall('"([\w\s]+) star rating', str(soup))[0]

    # price
    price = -1
    price_tags = soup.find_all('span', class_="css-oyv5ea")
    for price_tag in price_tags:
        if '$' in price_tag.text:
            price = len(price_tag.text)

    rest_dic[name] = rest_dic.get(name, {})
    rest_dic[name] = {'phone': phoneret,
                      'address': addressret,
                      'website': webret,
                      'num_review': num_review,
                      'hours': time,
                      'tags': rest_tags,
                      'rating': rating_str,
                      'price': price,
                      'words': words_set}

    return rest_dic

# need to add: indexer, amenities
    