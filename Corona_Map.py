# -*- coding: UTF-8 -*-
# Ver 0.2

import numpy as np
import folium
import os
import pandas as pd
from folium.plugins import HeatMap
import json
import urllib.request

# GPS of current location
latitude = 31.19
longitude = 121.32
map_data = folium.Map(location=[latitude, longitude], zoom_start=4)

# Read Dataset
resp = urllib.request.urlopen('https://coronavirus-tracker-api.herokuapp.com/v2/locations')
org_data = (json.loads(resp.read()))['locations']
json_data = pd.json_normalize(org_data)

# Instantiate a feature group for the incidents in the dataframe
incidents = folium.map.FeatureGroup()

# Add circle on the map
for country_no in json_data.id:
    incidents.add_child(
        folium.CircleMarker(
            [json_data["coordinates.latitude"][country_no],
             json_data["coordinates.longitude"][country_no]],
            radius=7,
            color='yellow',
            fill=True,
            fill_color='red',
            fill_opacity=0.4
        )
    )
map_data.add_child(incidents)

# Add pop-up text to circles
for country_no in json_data.id:
    if json_data.province[country_no] != '':
        label_tooltip = "{}{}{}{}{}".format(
            str(json_data.province[country_no]),
            ' CONFIRM:',
            str(json_data["latest.confirmed"][country_no]),
            ' DEATH:',
            str(json_data["latest.deaths"][country_no]))
    else:
        label_tooltip = "{}{}{}{}{}".format(
            str(json_data.country[country_no]),
            ' CONFIRM:',
            str(json_data["latest.confirmed"][country_no]),
            ' DEATH:',
            str(json_data["latest.deaths"][country_no]))
    folium.RegularPolygonMarker(
        [json_data["coordinates.latitude"][country_no],
         json_data["coordinates.longitude"][country_no]],
        tooltip=label_tooltip,
        number_of_sides=10,
        radius=5).add_to(map_data)

# Convert data format
lat = np.array(json_data["coordinates.latitude"][0:255], dtype=float)
lon = np.array(json_data["coordinates.longitude"][0:255], dtype=float)
confirm = np.array(json_data["latest.confirmed"][0:255], dtype=float)
heatdata = [[lat[i], lon[i], confirm[i]] for i in range(255)]

# add incidents to map
HeatMap(heatdata, radius=40).add_to(map_data)

map_data.save(os.path.join(r'F:\python\Folium', "Heatmap.html"))
