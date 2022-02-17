from bs4 import BeautifulSoup
import requests
import re

def get_info(soup):
    '''

    '''

    # restaurant name
    name = soup.find_all('h1', class_="css-1x9iesk")
    # this is used for detecting whether the Yelp site is blocking us
    if len(name) == 0:
        return (None, None)
    name = name[0].text

    # indexer for restaurant name
    lower_name = name.lower()
    name_words = lower_name.split()
    words_set = set(name_words)

    # phone number
    phone = -1
    phone_tag = soup.find_all('p', class_="css-1h7ysrc")
    if len(phone_tag) >= 2:
        if '(' in phone_tag[-2].text:
            phone = phone_tag[-2].text
        elif '(' in phone_tag[-1].text:
            phone = phone_tag[-1].text
    
    # address
    address = 'Not available'
    address_tag = soup.find_all('p', class_="css-1ccncw")
    if len(address_tag) != 0:
        address = address_tag[0].text
    else:
        address_tag = soup.find_all('span', class_="raw__09f24__T4Ezm")
        if len(address_tag) >= 2:
            if 'Chicago' in address_tag[1].text:
                address = address_tag[0].text + ' ' + address_tag[1].text

    # restaurant website
    website = 'Not available'
    webs = soup.find_all('a', class_="css-10y60kr")
    if len(webs) >= 2:
        potential = webs[2].get('href')
        if potential is not None and 'biz' in potential:
            website = potential[0]

    # number of reviews
    num_review = -1
    tags = soup.find_all('span', class_="css-1yy09vp")
    if len(tags) != 0:
        num_review_str = tags[0].text
        num_review_search = re.search('^[0-9]+', num_review_str)
        if num_review_search is not None:
            num_review = num_review_search[0]

    # hours
    time = 'Unknown'
    if len(tags) != 0:
        potential_time = tags[-1].text
        if potential_time is not None:
            if 'AM' in potential_time or 'PM' in potential_time:
                time = potential_time

    # restaurant tags
    rest_tags = set()
    if len(tags) >= 2:
        for i in range(1, len(tags)):
            tag = tags[i].find_all('a', class_= "css-1422juy")
            if len(tag) != 0:
                tag_text = tag[0].text
                if 'AM' not in tag and 'PM' not in tag_text:
                    rest_tags.add(tag_text)

    # rating
    # rating_tag = soup.find_all('div', class_="css-i-stars__09f24__foihJ i-stars--large-4__09f24__jGrzl border-color--default__09f24__NPAKY overflow--hidden__09f24___ayzG")
    rating = -1
    potential_rating_str = re.findall('"([\w\s.]+) star rating', str(soup))
    if len(potential_rating_str) != 0:
        rating_str = potential_rating_str[0]
        rating = float(rating_str)

    # price
    price = -1
    price_tags = soup.find_all('span', class_="css-oyv5ea")
    for price_tag in price_tags:
        if '$' in price_tag.text:
            price_text = price_tag.text.strip()
            price = len(price_text)

    rest_dic = {'phone': phone,
                'address': address,
                'website': website,
                'num_review': num_review,
                'hours': time,
                'tags': rest_tags,
                'rating': rating,
                'price': price,
                'words': words_set}

    return (name, rest_dic)

# need to add: amenities
    