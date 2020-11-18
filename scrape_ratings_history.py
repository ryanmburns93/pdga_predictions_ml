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

from bs4 import BeautifulSoup
from bs4.dammit import EncodingDetector

import re #Regex for lists


# Read In List of Top Pro PDGA Numbers
pro_pdga_numbers = pd.read_csv(r"C:\Users\samta\Documents\Python Scripts\disc_golf\data\top_pro_pdga_number.csv")

str_pdga_list = pro_pdga_numbers.pdga_number.astype(str)



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
    



all_rating.to_csv(r"C:\Users\samta\Documents\Python Scripts\disc_golf\data\pro_rating_history.csv")