# -*- coding: utf-8 -*-
"""
Created on Wed Nov 11 21:16:29 2020

@author: samta
"""

import numpy as np
import pandas as pd
import lxml.html
from lxml.cssselect import CSSSelector
import requests
from bs4 import BeautifulSoup
import urllib.parse 
import collections 
from collections import deque

# Build a crawler to find all pages of the style we want
# https://www.freecodecamp.org/news/how-to-build-a-url-crawler-to-map-a-website-using-python-6a287be1da11/

url = "https://www.pdga.com/players/stats?Year=2019&player_Class=All&Gender=All&Bracket=All&continent=All&Country=All&StateProv=All&page=1"


last_pages = [365,400,360,438,500,565,661,724,835,927,1009,1115,1278,1444,1739,2174,2609,2942,
                3362,3756,3454]





last_page_years = [2000,2001,2002,2003,2004,2005,2006,2007,2008,2009,2010,2011,2012,
                     2013,2014,2015,2016,2017,2018,2019,2020]




pages_long = []
years_long = []
url_list = []


for i in range(len(last_pages)):
    for j in range(last_pages[i]+1):
        url_list.append('https://www.pdga.com/players/stats?Year='+str(last_page_years[i])+
                        '&player_Class=All&Gender=All&Bracket=All&continent=All&Country=All&StateProv=All&page='
                        +str(j))
        
        #pages_long.append(last_pages[i])
        #years_long.append(last_page_years[i])

result = [i for i in url_list if re.search(r"2013", i)]

print(url_list[23467])



# Import Data Website

url_read = []
url_unread = url_list

all_fields = pd.DataFrame(columns=(['player_name','pdga_number','rating','year','gender','pdga_class',
                                    'division','country','player_state','events','points','cash']))

for i in range(305):
    for x in url_list:     
        #url = 'https://www.pdga.com/players/stats?Year=2019&player_Class=All&Gender=All&Bracket=All&continent=All&Country=All&StateProv=All&page=' + str(x)
        url = x
        #url_read.append(url)
        
        #url_unread.remove(url)
        r = requests.get(url)
        
        # build the DOM Tree
        tree = lxml.html.fromstring(r.text)
        
        def css_reader(css):
            temp = CSSSelector(css)
            results = temp(tree)
            df = [result.text for result in results]
            return df
        
        
        player_name = css_reader('.player-name a')
        pdga_number = css_reader('.pdga-number')
        rating = css_reader('.player-rating')
        year = css_reader('td.views-field-Year')
        gender = css_reader('td.views-field-player-Gender')
        pdga_class = css_reader('td.views-field-views-conditional')
        division = css_reader('td.views-field-Bracket')
        country = css_reader('td.views-field-player-Country')
        player_state = css_reader('td.views-field-player-AdministrativeArea')
        events = css_reader('td.views-field-TournCnt')
        points = css_reader('td.active.views-align-center')
        cash = css_reader('td.views-align-right')
        
        
        
        all_fields_temp = pd.DataFrame(
            {'player_name':player_name,
            'pdga_number':pdga_number,
            'rating':rating,
            'year':year,
            'gender':gender,
            'pdga_class':pdga_class,
            'division':division,
            'country':country,
            'player_state':player_state,
            'events':events,
            'points':points,
            'cash':cash}
            )
        
        all_fields = all_fields.append(all_fields_temp)
        





tail = all_fields.tail(20)



#Filter out 2019

is_2020 = all_fields.year.str.contains("2020",regex=False)

not_2020 = [not elem for elem in is_2020] 

all_fields = all_fields[not_2020]

# Export To CSV

all_fields.to_csv(r"C:\Users\samta\Documents\Python Scripts\disc_golf\data\all_fields.csv")







