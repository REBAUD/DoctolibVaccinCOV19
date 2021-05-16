# -*- coding: utf-8 -*-
"""
Created on Sat May 15 16:53:23 2021

@author: vincent.rebaud
"""

import math
import datetime
import time
import requests
import json
import os
import re
import winsound
import webbrowser

# Bip frequency for alert
frequency = 700  # Set Frequency To 2500 Hertz
duration = 1000  # Set Duration To 1000 ms == 1 second

# Localisation
city = 'alfortville'
geoloc = (48.80093, 2.422317) 

# Tolerancy radius
tolerancy_radius = 10 # km

centerList_url = 'https://www.doctolib.fr/vaccination-covid-19/' + city + '?ref_visit_motive_ids[]=6970&ref_visit_motive_ids[]=7005&force_max_limit=2'
searchResults_url = 'https://www.doctolib.fr/search_results/[id].json?ref_visit_motive_ids%5B%5D=6970&ref_visit_motive_ids%5B%5D=7005&speciality_id=5494&search_result_format=json&force_max_limit=2'

# Calculate the distance between 2 GPS points
def distance(geoloc, point):
    R = 6373.0

    lat1 = math.radians(float(geoloc[0]))
    lon1 = math.radians(float(geoloc[1]))
    lat2 = math.radians(float(point[0]))
    lon2 = math.radians(float(point[1]))
    
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    
    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    return (R * c)

# Main logic
index = 0
closePlaces_infos = []
while True:

    # Check list of vaccination center close to us
    if index == 0:
        # Get list of vaccincation center around city
        list_html = requests.get(centerList_url).text
        places_infos = re.findall('data-lat="(\d*.\d*)" data-lng="(\d*.\d*)" id="search-result-(\d*)"', list_html)

        # Check the dictance between 2 points, and return true if closer than tolerance radius
        def nearMe(item):
            dist = distance(geoloc, item)
            return dist < tolerancy_radius

        # Keep only close vaccination center
        closePlaces_infos = list(filter(nearMe, places_infos))

    # Request doctolib for the vaccination center corresponding at index in the close list
    searchRequest_url = searchResults_url.replace('[id]', closePlaces_infos[index][2])
    print('fetching', searchRequest_url)
    response = requests.get(searchRequest_url).text
    
    # Read json
    data = None
    try:
        data = json.loads(response)
    except json.decoder.JSONDecodeError:
        print('error decoding json:')
        print(response.read())

    # Analyse result
    if data != None :
        print('Get result for center ', data['search_result']['name_with_title'])
        if data['total'] > 0:
            print('------ >>>')
            print(datetime.datetime.now().time())
            print(' ')
            print(data['search_result']['name_with_title'])
            print(distance(geoloc, (data['search_result']['position']['lat'], data['search_result']['position']['lng'])))
            print(data['total'], 'slot(s) available')
            print(data['search_result']['visit_motive_name'])
            print(' ')
            print('https://www.doctolib.fr' + data['search_result']['url'])
            print(' ')
            print(json.dumps(data, indent=4, sort_keys=True))
            print(' ')
            print('<<< ------')
            # Open a web page & emit a bip
            webbrowser.open('https://www.doctolib.fr' + data['search_result']['url'])
            winsound.Beep(frequency, duration)
   
    # Increase index
    index += 1
    if index == len(closePlaces_infos[index][2]):
        index = 0
   
    #Wait 2s
    time.sleep(2)