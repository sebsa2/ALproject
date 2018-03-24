# std
from io import StringIO
import time

# 3rd
import pandas as pd
import requests

api_base = 'https://www.renewables.ninja/api/'
token = '5670bc214220f76f9f19680709d516a89efe1bbb'
s = requests.session()
# Send token header with each request
s.headers = {'Authorization': 'Token ' + token}

df = pd.read_csv('test.csv')
df['Latitude'] = df['Latitude'].astype(float)
df['Longitude'] = df['Longitude'].astype(float)
df['Total nominal power'] = df.apply(lambda row: float(row['Total nominal power'].replace(' kW', '').replace(',', '')), axis=1)
subset = df[['Wind farm name', 'Latitude', 'Longitude', 'Total nominal power']]
tuples = [tuple(x) for x in subset.values]
for t in tuples:
	name, latitude, longitude, power = t
	print('Fetching {} (power : {}) at lat {} and long {}'.format(name, power, latitude, longitude))
	args = {
		'lat': latitude,
	    'lon': longitude,
    	'format': 'csv',
	    'header': True,
	    'capacity': power,
	    'local_time': True,
	    'date_from': '2016-01-01',
		'date_to': '2016-12-31',
		'height': 80,
		'turbine': 'Vestas V90 2000',
	}
	r = s.get(api_base + 'data/wind?', params=args)
	place_df = pd.read_csv(StringIO(r.text))
	place_df.columns = place_df.iloc[0]
	place_df = place_df.iloc[2:]
	place_df['new_output'] = place_df.apply(lambda row: float(row['output']) / float(power), axis=1)
	place_df.to_csv('outputs/wind/{}.csv'.format(name.replace(' ', '_')))
	print('Data for {} stored at data/{}.csv, now sleeping {} seconds'.format(name, name.replace(' ', '_'), 3600/50))
	time.sleep(3600/50)
