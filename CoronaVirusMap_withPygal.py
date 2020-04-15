import pygal_maps_world.maps
import pygal.style
import json
import urllib.request
import pandas as pd


wm_style = pygal.style.RotateStyle('#336699', base_style=pygal.style.LightColorizedStyle)
wm = pygal_maps_world.maps.World(style=wm_style)
wm.title = 'Corona Virus Situation'
# with open('corona_situation_org_20200414') as local_data:
#     org_data = (json.load(local_data))['locations']
resp = urllib.request.urlopen('https://coronavirus-tracker-api.herokuapp.com/v2/locations')
org_data = (json.loads(resp.read()))['locations']
json_data = pd.json_normalize(org_data)

dict_data_confirmed = {}
dict_data_deaths = {}
for country_no in json_data.id:
    dict_value_confirmed = dict_data_confirmed.get(str(json_data.country_code[country_no]).lower())
    dict_value_deaths = dict_data_deaths.get(str(json_data.country_code[country_no]).lower())
    if dict_value_confirmed is not None:
        dict_value_confirmed += json_data['latest.confirmed'][country_no]
        dict_value_deaths += json_data['latest.deaths'][country_no]
    else:
        dict_value_confirmed = json_data['latest.confirmed'][country_no]
        dict_value_deaths = json_data['latest.deaths'][country_no]
    dict_data_confirmed[str(json_data.country_code[country_no]).lower()] = dict_value_confirmed
    dict_data_deaths[str(json_data.country_code[country_no]).lower()] = dict_value_deaths
# wm.add('Deaths', dict_data_deaths)
wm.add('Confirmed', dict_data_confirmed)

wm.render_to_file('corona_map.svg')
