import requests
from requests.auth import HTTPBasicAuth
import time
import os
import pandas as pd
from sodapy import Socrata
import datetime as dt

NY_DATA_ENDPOINT = 'https://data.cityofnewyork.us/resource/'
NY_DATA_API_KEY = os.environ['NY_DATA_API_KEY']
NY_DATA_API_KEY_SECRET = os.environ['NY_DATA_API_KEY_SECRET']
DEMOGRAPHICS = 'kku6-nxdu'
TRAIN_STATIONS = 'kk4q-3rt2'
COLLISIONS = "h9gi-nx95"
TURNSTILE_ACCESS = "py8k-a8wg"

TOM_TOM_ENDPOINT = 'https://api.tomtom.com/search/2/reverseGeocode/'
TOM_TOM_API_KEY = os.environ['TOM_TOM_API_KEY']

JSON = '.json?'

FILE_LOCATION = 'data'

zip_borough = {}
borough_bid = {'Brooklyn': 1, 'Bronx': 2, 'Manhattan': 3, 'Queens': 4, 'Staten Island': 5}


def zip_codes_to_boroughs():
    with open("data/zip_borough.csv", "r") as file:
        lines = file.readlines()
        for line in lines:
            zip = line.split(',')[0]
            borough = line.split(',')[1]
            borough = borough.strip('\n')
            if zip == 'zip':
                continue
            zip_borough[int(zip)] = borough


def zip_codes_is_in():
    query = 'jurisdiction_name='
    table = []
    schema = ','.join(['bid', 'females', 'males', 'gender_unknown', 'american_indians', 'asians', 'blacks',
                       'hispanic_latinos', 'pacific_islanders', 'whites', 'other', 'ethnicity_unknown'])
    table.append(schema)
    for zip_code in zip_borough.keys():
        print(zip_code)
        url = ''.join([NY_DATA_ENDPOINT, DEMOGRAPHICS, JSON, query, str(zip_code)])
        response = requests.get(url, auth=HTTPBasicAuth(NY_DATA_API_KEY, NY_DATA_API_KEY_SECRET))
        data = response.json()
        borough = zip_borough[zip_code]
        bid = borough_bid[borough]
        if response.status_code == requests.codes.ok:
            if len(data) > 0:
                data = data[0]
                females = data['count_female']
                males = data['count_male']
                gender_unknown = data['count_gender_unknown']
                american_indians = data['count_american_indian']
                asians = data['count_asian_non_hispanic']
                blacks = data['count_black_non_hispanic']
                hispanic_latinos = data['count_hispanic_latino']
                pacific_islanders = data['count_pacific_islander']
                whites = data['count_white_non_hispanic']
                other_ethnicity = data['count_other_ethnicity']
                ethnicity_unknown = data['count_ethnicity_unknown']
                tuple = ','.join([str(zip_code), str(bid), str(females), str(males), str(gender_unknown),
                                  str(american_indians), str(asians), str(blacks), str(hispanic_latinos),
                                  str(pacific_islanders), str(whites), str(other_ethnicity), str(ethnicity_unknown)])
            else:
                tuple = ','.join([str(zip_code), str(bid), '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'])

            table.append(tuple)

    with open(os.path.join(FILE_LOCATION, "zip_codes_is_in.csv"), "w+") as file:
        file.write('\n'.join(table))
    file.close()


def get_zip_code(latitude, longitude):
    url = ''.join([TOM_TOM_ENDPOINT, str(latitude), '%2C', str(longitude), JSON, 'key=', TOM_TOM_API_KEY])
    response = requests.get(url)
    data = response.json()
    return data['addresses'][0]['address']['postalCode']


def train_stations_have_and_stops_at():
    query = '$select=name, the_geom, line'
    url = ''.join([NY_DATA_ENDPOINT, TRAIN_STATIONS, JSON, query])
    response = requests.get(url, auth=HTTPBasicAuth(NY_DATA_API_KEY, NY_DATA_API_KEY_SECRET))
    data = response.json()
    train_stations = []
    train_stations_schema = ','.join(['name', 'zip_code'])
    train_stations.append(train_stations_schema)
    stops_at = []
    stops_at_schema = ','.join(['station_name', 'line_name'])
    stops_at.append(stops_at_schema)

    train_lines = []
    if response.status_code == requests.codes.ok:
        for station in data:
            print(station['name'])
            name = station['name']
            coordinates = station['the_geom']['coordinates']
            latitude = round(coordinates[1], 3)
            longitude = round(coordinates[0], 3)
            zip_code = get_zip_code(latitude, longitude)
            lines = station['line'].split(' ')[0].split('-')
            lines = set(lines)
            train_station_tuple = ','.join([name, zip_code])

            for line in lines:
                stops_at_tuple = ','.join([name, line])
                stops_at.append(stops_at_tuple)
                if line not in train_lines:
                    train_lines.append(line)
            time.sleep(1)
            train_stations.append(train_station_tuple)

    with open(os.path.join(FILE_LOCATION, "train_stations_have.csv"), "w+") as file:
        file.write('\n'.join(train_stations))
    file.close()

    with open(os.path.join(FILE_LOCATION, "stops_at.csv"), "w+") as file:
        file.write('\n'.join(stops_at))
    file.close()

    with open(os.path.join(FILE_LOCATION, "train_lines.csv"), "w+") as file:
        file.write('\n'.join(train_lines))
    file.close()


def covid_casualties():
    url = 'https://raw.githubusercontent.com/nychealth/coronavirus-data/master/totals/data-by-modzcta.csv'
    response = requests.get(url)
    lines = response.text.split('\n')
    ZIP_CODE_INDEX = 0
    NEIGHBORHOOD_INDEX = 1
    CASES_INDEX = 3
    DEATHS_INDEX = 6
    covid_tuples = []

    for line in lines:
        data = line.split(',')
        if len(data) == 10:
            zip_code = data[ZIP_CODE_INDEX]
            neighborhood = data[NEIGHBORHOOD_INDEX]
            cases = data[CASES_INDEX]
            deaths = data[DEATHS_INDEX]
            covid_tuple = ','.join([zip_code, neighborhood, cases, deaths])
            covid_tuples.append(covid_tuple)

    with open(os.path.join(FILE_LOCATION, "covid_casualties.csv"), "w+") as file:
        file.write('\n'.join(covid_tuples))

def accidents_occurred_In():
  client = Socrata("data.cityofnewyork.us", NY_DATA_API_KEY_SECRET)
  response = client.get(COLLISIONS, where="crash_date >= '2020-01-01'",limit=10000000)
  data_df = pd.DataFrame.from_records(response)
  data_2020 = data_df[['collision_id', 'crash_date', 'crash_time', 'zip_code', 'on_street_name', 'contributing_factor_vehicle_1']].dropna(subset=['zip_code'])
  data_2020[['on_street_name', 'contributing_factor_vehicle_1']] = data_2020[['on_street_name', 'contributing_factor_vehicle_1']].fillna('MISSING')
  data_2020.reset_index()
  data_2020.columns = ['collision_id', 'date', 'time', 'zip_code', 'street_name', 'contributinng_factor']
  data_2020.to_csv('accidents_occured_in.csv', index=False)

def turnstiles_access(): 
  client = Socrata("data.ny.gov", NY_DATA_API_KEY_SECRET)
  response = client.get(TURNSTILE_ACCESS, limit=10000000)
  data_df = pd.DataFrame.from_records(response)
  data_df['date'] = pd.to_datetime(data_df['Date'])
  data_df = data_df[data_df['date'] >= '2020-1-1']
  turnstile_access = data_df.sort_values('date', ascending=False).drop_duplicates(['C/A'])
  turnstile_access = turnstile_access[['C/A', 'Unit', 'Station', 'Date', 'Time', 'Entries', 'Exits                                                     ']]
  turnstile_access.columns = ['turnstile_id', 'station_id', 'station_name', 'date', 'time', 'entries', 'exits']
  turnstile_access.to_csv('turnstiles_access.csv', index=False)

zip_codes_to_boroughs()
zip_codes_is_in()
train_stations_have_and_stops_at()
covid_casualties()
accidents_occurred_In()
turnstiles_access()
