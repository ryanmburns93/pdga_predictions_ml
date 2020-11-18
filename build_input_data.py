# -*- coding: utf-8 -*-
"""
Created on Sun Nov 15 19:05:54 2020

@author: samta
"""


import numpy as np
import pandas as pd
import re
from itertools import compress


# Read in Player List and Event Detail

event_details = pd.read_csv(r"C:\Users\samta\Documents\Python Scripts\disc_golf\data\a_tier_event_details.csv")
all_players = pd.read_csv(r"C:\Users\samta\Documents\Python Scripts\disc_golf\data\all_fields.csv")
rating_history = pd.read_csv(r"C:\Users\samta\Documents\Python Scripts\disc_golf\data\pro_rating_history.csv")

# Clean Up Variables in all_players dataset

all_players['gender_clean'] = np.where(all_players.gender.str.contains("Male"),"male","female")
all_players['pdga_class_clean'] = np.where(all_players.pdga_class.str.contains("Pro"),"pro","am")
all_players['cash_clean'] = all_players.cash.str.findall(r"[0-9]*[,]?[0-9]*\...").str[0].str.replace(",","").astype(float).fillna(0)


#Standardize tournament names in event_details
event_details.loc[(event_details.event_name.str.contains("Texas State"), 'standard_event_name')] = 'texas_state_championship'
event_details.loc[(event_details.event_name.str.contains("Glass Blown Open"), 'standard_event_name')] = 'ddo_gbo'
event_details.loc[(event_details.event_name.str.contains("Dynamic Discs Open"), 'standard_event_name')] = 'ddo_gbo'
event_details.loc[(event_details.event_name.str.contains("Beaver State"), 'standard_event_name')] = 'beaver_state'
event_details.loc[(event_details.event_name.str.contains("Brent Hambrick"), 'standard_event_name')] = 'brent_hambrick_memorial'
event_details.loc[(event_details.event_name.str.contains("Ledgestone"), 'standard_event_name')] = 'ledgestone_insurance_open'
event_details.loc[(event_details.event_name.str.contains("Alabama"), 'standard_event_name')] = 'alabama_championship'
event_details.loc[(event_details.event_name.str.contains("Masters"), 'standard_event_name')] = 'masters_cup'
event_details.loc[(event_details.event_name.str.contains("Memorial Championship"), 'standard_event_name')] = 'memorial_championship'
event_details.loc[(event_details.event_name.str.contains("Kansas"), 'standard_event_name')] = 'kansas_city_wide_open'
event_details.loc[(event_details.event_name.str.contains("Delaware"), 'standard_event_name')] = 'delaware_challenge'
event_details.loc[(event_details.event_name.str.contains("Great"), 'standard_event_name')] = 'great_lakes_open'
event_details.loc[(event_details.event_name.str.contains("Green"), 'standard_event_name')] = 'gmc_championship'
event_details.loc[(event_details.event_name.str.contains("San Francisco"), 'standard_event_name')] = 'sfo'
event_details.loc[(event_details.event_name.str.contains("Portland"), 'standard_event_name')] = 'portland_open'
event_details.loc[(event_details.event_name.str.contains("Idlewild"), 'standard_event_name')] = 'idlewild_open'
event_details.loc[(event_details.event_name.str.contains("Jonesboro"), 'standard_event_name')] = 'jonesboro_open'
event_details.loc[(event_details.event_name.str.contains("Maple Hill"), 'standard_event_name')] = 'maple_hill'
event_details.loc[(event_details.event_name.str.contains("Utah"), 'standard_event_name')] = 'utah'
event_details.loc[(event_details.event_name.str.contains("Waco"), 'standard_event_name')] = 'waco'
event_details.loc[(event_details.event_name.str.contains("Las Vegas"), 'standard_event_name')] = 'las_vegas'
event_details.loc[(event_details.event_name.str.contains("Gentlemen"), 'standard_event_name')] = 'las_vegas'
event_details.loc[(event_details.event_name.str.contains("Vibram"), 'standard_event_name')] = 'maple_hill'
event_details.loc[(event_details.event_name.str.contains("Pittsburgh"), 'standard_event_name')] = 'pittsburgh'
event_details.loc[(event_details.event_name.str.contains("Tour Championship"), 'standard_event_name')] = 'dgpt_tour_championship'
event_details.loc[(event_details.event_name.str.contains("Preserve"), 'standard_event_name')] = 'preserve_championship'
event_details.loc[(event_details.event_name.str.contains("Hall of Fame"), 'standard_event_name')] = 'hall_of_fame_classic'
event_details.loc[(event_details.event_name.str.contains("Steilacoom"), 'standard_event_name')] = 'steilacoom_open'
event_details.loc[(event_details.event_name.str.contains("King"), 'standard_event_name')] = 'king_of_the_lake'
event_details.loc[(event_details.event_name.str.contains("Rochester"), 'standard_event_name')] = 'rochester_open'


# Extract Date Information from Event Details
months = ['January','February','March','April','May','June','July','August',
          'September','October','November','December']
    
def month_match(row):
    matches = []
    matches = [test_value in row['dates'] 
               for test_value in months]
    return list(compress(months, matches))

def start_date_maker(row):
    return pd.to_datetime(row['months'][0] + row['begin_day'] +", " + row['year'],infer_datetime_format=True)

def end_date_maker(row):
    if(len(row['months'])==1):
        return pd.to_datetime(row['months'][0] + row['end_day'] +", " + row['year'],infer_datetime_format=True)
    else:
        return pd.to_datetime(row['months'][1] + row['end_day'] +", " + row['year'],infer_datetime_format=True)

event_details['months'] = event_details.apply(month_match,axis=1)
event_details['first_day_raw'] = event_details.dates.str.findall('[0-9]{1,2} -').apply(', '.join)
event_details['begin_day'] = event_details.first_day_raw.str.findall('[0-9]{1,2}').apply(', '.join)
event_details['second_day_raw'] = event_details.dates.str.findall('[0-9]{1,2},').apply(', '.join)
event_details['end_day'] = event_details.second_day_raw.str.findall('[0-9]{1,2}').apply(', '.join)
event_details['year'] = event_details.dates.str.findall('[0-9]{4}').apply(', '.join)
event_details['start_date'] = event_details.apply(start_date_maker,axis=1)
event_details['end_date'] = event_details.apply(end_date_maker,axis=1)



unique_dates = event_details[['dates','start_date','end_date']].drop_duplicates()

#Fix Date in rating_history



rating_history['rating_date_clean'] = pd.to_datetime(rating_history['rating_date'],
                                                     infer_datetime_format=True)



# FInd P Mcbeth in Data

p_mcbeth = all_players[all_players['pdga_number']==27523]



# Inspect Dataset

unique_gender = all_players[['gender','gender_clean']].drop_duplicates()
unique_class = all_players[['pdga_class','pdga_class_clean']].drop_duplicates()
unique_division = all_players[['division']].drop_duplicates()

missing_cash = all_players[pd.isnull(all_players['cash_clean'])]
unique_missing_cash = missing_cash[['cash']].drop_duplicates()

# Filter to top 100 Male Pro Players in 2019

male_players = all_players[all_players['gender_clean']=="male"]
male_pros = male_players[male_players.pdga_class_clean.str.contains("pro")]
male_pros_2019 = male_pros[male_pros["year"]==2019].sort_values(by = ['rating'],ascending = False)
male_pros_2019_t100 = male_pros_2019.drop_duplicates(subset = ['pdga_number']).head(100)



#Merge Top Players with Events Details

top_w_place = male_pros_2019_t100.merge(event_details, how = 'left',
                                        on = 'pdga_number')

#Merge in most recent ratings detail prior to each event.
top_w_place= top_w_place[['player_name','pdga_number','country','player_state',
                         'standard_event_name','location','start_date','end_date','place','event_name','event_url']]

top_w_place = top_w_place[top_w_place['standard_event_name'].notnull()]


all_ratings = top_w_place.merge(rating_history[['pdga_number','rating_date_clean','rating']],
                                 on = ['pdga_number'])

all_ratings = all_ratings[all_ratings['rating_date_clean']<=all_ratings['start_date']]
model_data = all_ratings.drop_duplicates(subset = ['pdga_number','standard_event_name','start_date'])




# Output a list of PDGA numbers in Model Data


unique_players = model_data[['pdga_number']].drop_duplicates()

unique_players.to_csv(r"C:\Users\samta\Documents\Python Scripts\disc_golf\data\top_pro_pdga_number.csv")



# Write model data to csv

model_data.to_csv(r"C:\Users\samta\Documents\Python Scripts\disc_golf\data\model_data.csv")






