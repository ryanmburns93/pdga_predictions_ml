# -*- coding: utf-8 -*-
"""
Created on Tue Nov 17 14:25:21 2020

@author: samta
"""


import numpy as np
import pandas as pd
import lxml.html
from lxml.cssselect import CSSSelector
import requests
#from selenium import webdriver
#from selenium.webdriver.common.keys import Keys
#from webdriver_manager.chrome import ChromeDriverManager



# Read In List of Top Pro PDGA Numbers
pro_pdga_players = pd.read_csv("data/all_fields_2019_pro.csv")



pro_pdga_players = pro_pdga_players.sort_values(by = ['rating'],ascending = False)


# Output a list of PDGA numbers in Model Data

pro_pdga_numbers = pro_pdga_players[['pdga_number']].drop_duplicates()

pro_pdga_numbers_150 = pro_pdga_numbers.head(150)


str_pdga_list = pro_pdga_numbers_150.pdga_number.astype(str)



# Define Function to Read CSS Data and return as a dataset
def css_reader(css):
    temp = CSSSelector(css)
    results = temp(tree)
    df = [result.text for result in results]
    return df


all_rating = pd.DataFrame(columns=(['pdga_number','rating_date','rating']))

for number in str_pdga_list:    
    url = 'https://www.pdga.com/player/'+number+'/history'     
    r = requests.get(url)   
    tree = lxml.html.fromstring(r.text)
        
    #Pull background info on tourneys
    rating_date = css_reader('td.date')
    rating = css_reader('td.player-rating')
    
    all_rating_temp = pd.DataFrame(
        {
         'pdga_number':number,   
         'rating_date':rating_date,
         'rating':rating
        })

    all_rating = all_rating.append(all_rating_temp)
    



all_rating.to_csv("data/pro_rating_history.csv")