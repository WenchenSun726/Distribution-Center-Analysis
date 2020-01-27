# -*- coding: utf-8 -*-
"""
Created on Mon Sep 23 12:10:58 2019

@author: Sandy Sun
"""
import pandas as pd
import json
import requests
from geopy.distance import geodesic
from geopy.distance import great_circle

raw = pd.ExcelFile('raw.xlsx').parse(1)
raw=raw[(raw['City Pair'].str.contains('SOUTHAVEN, MS')) | (raw['City Pair'].str.contains('CAMBRIDGE, OH'))]
raw.to_excel('only DC.xlsx',index = False)

data= pd.ExcelFile('only DC.xlsx').parse(0)

#         ****check how many invalid post codes****                 
##        1. 0 & nan
s_code = list(data['Source Postal Code'].drop_duplicates())
d_code = list(data['Destination Postal Code'].drop_duplicates())
s_code.extend(d_code)
total_code = list(set(s_code)) #7209
total_code = [x for x in total_code if x != 0 and str(x) != 'nan'] #7207

##        2. using web scraping to extract information
def GetGeocode(postcode):
    url = 'https://www.mapdevelopers.com/data.php?operation=geocode&address='+str(postcode)
    res = requests.get(url)
    data = json.loads(res.text)
    country = data['data']['country']
    state = data['data']['state_code']
    country_code = data['data']['country_code']
    zipcode = data['data']['postcode']
    latitude = data['data']['lat']
    longitude = data['data']['lng']
    return (state,country,country_code,zipcode,latitude,longitude)

state_2_zip = {}
country_2_zip = {}
ccode_2_zip = {}
zip_2_zip = {}
la_to_zip = {}
long_to_zip = {}

for i in range(len(total_code[:])):
    url = 'https://www.mapdevelopers.com/data.php?operation=geocode&address=' + str(total_code[i])
    res = requests.get(url)
    data = json.loads(res.text)
    if len(data['data'])==0:
        continue
    else:
        country_2_zip[total_code[i]] = data['data']['country']
        ccode_2_zip[total_code[i]] = data['data']['country_code']
        zip_2_zip[total_code[i]] = data['data']['postcode']
        la_to_zip[total_code[i]] = data['data']['lat']
        long_to_zip[total_code[i]] = data['data']['lng']
        state_2_zip[total_code[i]] = data['data']['state_code']

state = pd.DataFrame(list(state_2_zip.items()))
country = pd.DataFrame(list(country_2_zip.items()))
ccode = pd.DataFrame(list(ccode_2_zip.items()))
postcode = pd.DataFrame(list(zip_2_zip.items()))
la = pd.DataFrame(list(la_to_zip.items()))
long = pd.DataFrame(list(long_to_zip.items()))

all_info = state.merge(country, on = 0)
all_info = all_info.merge(ccode, on = 0)
all_info = all_info.merge(postcode, on = 0)
all_info = all_info.merge(la, on = 0)
all_info = all_info.merge(long,on = 0)

all_info.to_excel('zipcode info.xlsx',index = False) #reference for all city relate info 

##use this all_info and vlookup back to only_DC data and filter matching data - 18956 cannot find correct info



#                           ***** Distance Calculation****            
cleaned_data = pd.ExcelFile("Cleaned_data_Sandy_Final.xlsx").parse(0)
cleaned_data['s_geocode'] = cleaned_data.apply(lambda x:(x['S_La'], x['S_Lo']),axis=1)
cleaned_data['d_geocode'] = cleaned_data.apply(lambda x:(x['D_La'], x['D_Lo']),axis=1)
cleaned_data['miles'] = cleaned_data.apply(lambda x:geodesic(x['s_geocode'],x['d_geocode']).miles,axis=1)
cleaned_data['circle_miles'] = cleaned_data.apply(lambda x:great_circle(x['s_geocode'],x['d_geocode']).miles,axis=1)

def GetDistance(postcode1, postcode2):
    url = 'https://www.mapdevelopers.com/distance_from_to.php?&from='+str(postcode1)+'&to='+str(postcode2)
    res = requests.get(url)
    data = json.loads(res.text)
    country = data['data']['country']
    state = data['data']['state_code']
    country_code = data['data']['country_code']
    zipcode = data['data']['postcode']
    latitude = data['data']['lat']
    longitude = data['data']['lng']
    return (state,country,country_code,zipcode,latitude,longitude)




