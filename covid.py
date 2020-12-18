
import requests
import string
import os
from os import path
from datetime import datetime
import json

URL = "https://services7.arcgis.com/mOBPykOjAyBO2ZKk/arcgis/rest/services/RKI_Landkreisdaten/FeatureServer/0/query?where=1%3D1&outFields=GEN,cases,deaths,cases7_per_100k,last_update,EWZ,cases_per_population,cases_per_100k,death_rate&returnGeometry=false&outSR=4326&f=json"

# What cities shall be shown in the table
CITIES_TO_DISPLAY = ['Neumarkt', 'Würzburg', 'Haßberge']

def get_data():

    # Creating the data dir if if does not exist
    if not path.exists("covid-tracker/data"):
        os.mkdir("covid-tracker/data")

    date = datetime.today().strftime('%Y-%m-%d')
    print("Current Date: {}".format(date))

    if not path.exists("covid-tracker/data/{}.json".format(date)):
        with open("covid-tracker/data/{}.json".format(date), "w") as df:
            print("yeet")
            # API request
            response = requests.get(URL).json()
            json.dump(response, df)
    else:
        print("antiyeet")
        with open("covid-tracker/data/{}.json".format(date)) as df:
            response = json.load(df)
    
    # Contains the data for all cities
    cities = response['features']

    data = {}

    # Data for germany
    total_cases = 0
    total_deaths = 0
    total_incidence = 0

    # Iterating over all cities
    for current_city in cities:

        curr = current_city['attributes']

        # City attributes
        name = curr['GEN']
        cases = curr['cases']
        deaths = curr['deaths']
        incidence = curr['cases7_per_100k']
        population = curr['EWZ']

        # Data for germany
        total_cases += cases
        total_deaths += deaths
        total_incidence +=incidence

        entry = {'cases': cases, 'incidence': incidence, 'deaths': deaths, 'population': population}

        # If two cities have the same name we pick the one with the higher population
        if any(c for c in CITIES_TO_DISPLAY if c in curr['GEN']):
            if name in data:
                if data[name]['population'] < population:
                    data[name] = entry
            else:
                data[name] = entry

    # Avg incidence in germany
    incidence = int(total_incidence / len(cities))

    # Appending data for germany
    data['Deutschland'] = {'cases': total_cases, 'incidence': incidence, 'deaths': total_deaths}

    return data

def create_table():

    data = get_data()

    # Table head
    table="<table><tr><th></th><th>Fälle (Gesamt)</th><th>Inzidenz</th><th>Tote</th></tr>"

    # Adding data to the table
    for table_row in sorted(data.keys()):
        table += "<tr>"
        table += "<td>{}</td>".format(table_row)
        table += "<td>{}</td>".format(data[table_row]['cases'])
        table += "<td>{}</td>".format(int(data[table_row]['incidence']))
        table += "<td>{}</td>".format(data[table_row]['deaths'])
        table += "</tr>"

    # End of table
    table += "</table>"

    return table


if __name__ == "__main__":

    # Creating a table and printing it
    table = create_table()
    print(table)
