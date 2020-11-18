# -*- coding: utf-8 -*-
"""
Created on Sat Nov 14 15:34:26 2020

@author: samta
"""

import numpy as np
import pandas as pd
import lxml.html
from lxml.cssselect import CSSSelector
import requests
from bs4 import BeautifulSoup
from bs4.dammit import EncodingDetector

import re #Regex for lists


# Define Function to Read CSS Data and return as a dataset
def css_reader(css):
    temp = CSSSelector(css)
    results = temp(tree)
    df = [result.text for result in results]
    return df


# Funcion to find which links are tour events
def str_filter(datalist):
    # Search data based on regular expression in the list
    return [val for val in datalist
        if re.search(r'.*/tour/event/.*', val)]


# Import Data Website



all_elite = pd.DataFrame(columns=(['tourney_name','location','dates']))

all_links = []                         

for i in range(5):                        
    url = 'https://www.pdga.com/tour/search?date_filter[min][date]=2010-11-17&date_filter[max][date]=2020-12-31&EventType[0]=E&page='+str(i)     
    r = requests.get(url)   
    tree = lxml.html.fromstring(r.text)
    
    #Pull background info on tourneys
    tourney_name = css_reader('td.views-field-OfficialName a')
    #status = css_reader('td.views-field-StatusIcons')
    location = css_reader('td.views-field-Location')
    dates = css_reader('td.views-field-StartDate')
    
    
    all_elite_temp = pd.DataFrame(
        {'tourney_name':tourney_name,
         'location':location,
         'dates':dates
         })
    
    all_elite = all_elite.append(all_elite_temp)

    # Find All Tour Event Links on Page
    parser = 'html.parser'  # or 'lxml' (preferred) or 'html5lib', if installed
    resp = requests.get(url)
    http_encoding = resp.encoding if 'charset' in resp.headers.get('content-type', '').lower() else None
    html_encoding = EncodingDetector.find_declared_encoding(resp.content, is_html=True)
    encoding = html_encoding or http_encoding
    soup = BeautifulSoup(resp.content, parser, from_encoding=encoding)
        
    for link in soup.find_all('a', href=True):
        all_links.append(link['href'])
    
    
# Subset to event links 
tour_events = str_filter(all_links)
tour_events = np.unique(tour_events)
event_urls = ['https://www.pdga.com' + str(x) for x in tour_events]



# Visit Each Event and Pull Data

event_details = pd.DataFrame(columns=(['event_name','place','pdga_number','prize','event_url']))
for k in event_urls:
    event_url = k
    
    r = requests.get(event_url)
    
    tree = lxml.html.fromstring(r.text)




    
    place = css_reader('td.place')
    pdga_number = css_reader('td.pdga-number')
    prize = css_reader('td.prize')
    #date = css_reader('.tournament-date')
    #headers = css_reader('.tournament-date')
    #round_scores = css_reader('td.round') Need to write code to figure out  how many rounds

    event_name = css_reader('h1')[0]
    
    #If the number of places and pdga_numbers dont match, skip the event since it is a doubles event
    if(len(place)!=len(pdga_number)):
        continue
    
    print(event_url)
    print("Number of places %d" % len(place))
    print("Number of pdga_number %d" % len(pdga_number))
    print("Number of prize %d" % len(prize))
    
    
    
    event_details_temp = pd.DataFrame(
        {
         'event_name':event_name,
         'place':place,
         'pdga_number':pdga_number,
        # 'prize':prize,  Excluding prize data since some events dont have prizes for all divisions
         'event_url':event_url     
        })

    event_details = event_details.append(event_details_temp)



#Merge Tourney List with A-tiers list

events_unique = event_details[['event_name','event_url']].drop_duplicates()
events_unique['event_pdga_number'] = events_unique['event_url'].str[32:].astype(int)
events_unique = events_unique.sort_values(by = ['event_name','event_pdga_number'])
events_unique['event_rank'] = events_unique.groupby(['event_name']).cumcount()+1
all_elite['event_rank'] = all_elite.groupby(['tourney_name']).cumcount()+1
#all_pro_a = all_pro_a.sort_values(by = ['tourney_name','event_rank'])

all_elite_url = all_elite.merge(events_unique,left_on=['tourney_name','event_rank'],
                              right_on=['event_name','event_rank'],
                              how = 'right')


# Add Dates and Location to event_details

all_elite_merge = all_elite_url[['event_url','location','dates']]
event_details_export = event_details.merge(all_elite_merge,
                                     on = 'event_url')



# Write to CSV

event_details_export.to_csv("data/a_tier_event_details.csv")







