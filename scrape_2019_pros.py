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
import os


# Get working directory

working = os.getcwd()


url_base = "https://www.pdga.com/players/stats?Year=2019&player_Class=1&Gender=Male&Bracket=MPO&continent=All&Country=All&StateProv=All&page="

url_list = []
for i in range(347):
    url_list.append(url_base + str(i))    


all_fields = pd.DataFrame(columns=(['player_name','pdga_number','rating','year','gender','pdga_class',
                                    'division','country','player_state','events','points','cash']))


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
        



# Export To CSV


all_fields.to_csv("data/all_fields_2019_pro.csv")






