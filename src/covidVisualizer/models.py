from django.db import connection
import sqlite3
import numpy as np
import json
import pandas as pd
import mapclassify
import requests
import csv
import plotly.express as px
# import plotly.io as pio
# pio.renderers.default = 'firefox'
import os
import plotly.express as px

states = []
statesCode = {}
statesCovidData = {}
statesPopulation = {}
conn = connection.cursor()
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

stateDataResponse = requests.get('https://api.covid19india.org/state_district_wise.json')
stateData = stateDataResponse.json()
with open('stateData.json', 'w') as f:
    json.dump(stateData, f)

indiaCovidDataResponse = requests.get('https://api.covid19india.org/v4/data.json')
indiaCovidData = indiaCovidDataResponse.json()
with open('indiaCovidData.json', 'w') as f:
    json.dump(indiaCovidData, f)

state_id_map = {}
path = os.path.join(BASE_DIR, 'static', "india-all-states.geo.json")
india_states = json.load(open(path))


path = os.path.join(BASE_DIR, 'static', "stateData.json")
with open(path, "r") as read_file:
    print("Started converting JSON string document to Python dictionary")
    indiaStateData = json.load(read_file)
    states = list(indiaStateData.keys())
    for state in states:
        statesCode[state] = indiaStateData[state]["statecode"]

path = os.path.join(BASE_DIR, 'static', "indiaCovidData.json")
with open(path, "r") as covid_file:
    print("Started converting JSON string document to Python dictionary")
    indiaCovidData = json.load(covid_file)
    for key,value in statesCode.items():
        try:
            #print(key, value, indiaCovidData[value]["total"])
            statesCovidData[key] = indiaCovidData[value]["total"]
        except KeyError: 
            continue

path = os.path.join(BASE_DIR, 'static', "india.state-population.tsv")
tsv_file = open(path)
read_tsv = csv.reader(tsv_file, delimiter="\t")
for row in read_tsv:
    statesPopulation[row[0]] = row[1]
tsv_file.close()

for feature in india_states['features']:
    feature['id'] = feature['properties']['ID_1']
    state_id_map[feature['properties']['NAME_1']] = feature['id']
print(state_id_map)
    
#opens the database connection
def openDatabase():
    conn = sqlite3.connect('indiaCovidData.db')
    return conn

#deletes the table
def dropTable():
    print("Dropping old table")
    conn = openDatabase()
    conn.execute('''DROP TABLE indiaStateCovidData;''')

#creates the table
def createTable() :
    conn = openDatabase()
    conn.execute('''CREATE TABLE indiaStateCovidData  (ID INT PRIMARY KEY,
                                                       NAME TEXT NOT NULL,
                                                       POPULATION INT, 
                                                       NAMECODE TEXT,
                                                       CONFIRMED INT,
                                                       DECEASED INT,
                                                       RECOVERED INT,
                                                       TESTED INT);''')
    conn.commit()
    print ("Table created successfully");
    conn.close()

#initially populates the table with contactlist present in the file
def fillTable() :
    conn = openDatabase()
    print("Filling Table with initial values")
    states.sort()
    for state in states:
        try:
            if(state == "Odisha"):
                stateIdMap = state_id_map["Orissa"]
            else:
                stateIdMap = state_id_map[state]
            params = (stateIdMap, state, statesPopulation[state], statesCode[state], statesCovidData[state]["confirmed"],
                 statesCovidData[state]["deceased"], statesCovidData[state]["recovered"],
                 statesCovidData[state]["tested"])
            conn.execute("INSERT INTO indiaStateCovidData (ID, NAME, POPULATION, NAMECODE, CONFIRMED, DECEASED, RECOVERED, TESTED) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", params);
        except KeyError:
            continue
    conn.commit()
    conn.close()

def getDataFrame() :
    conn = openDatabase()
    print("Creating dataframe")
    cursor = conn.execute("SELECT * FROM indiaStateCovidData")
    state_id = []
    name = []
    population = []
    namecode = []
    confirmed = []
    deceased = []
    recovered = []
    tested = []
    for row in cursor:
        state_id.append(row[0])
        name.append(row[1])
        population.append(row[2])
        namecode.append(row[3])
        confirmed.append(row[4])
        deceased.append(row[5])
        recovered.append(row[6])
        tested.append(row[7])
    data = {"id": state_id, "Name": name, "Population": population, "Namecode": namecode, "Confirmed": confirmed,
         "Deceased": deceased, "Recovered": recovered, "Tested":tested}
    #print(data)
    conn.close()
    return data

dropTable()
createTable()
fillTable()

def visualize():
    path = os.path.join(BASE_DIR, 'templates', 'confirmed_plot.html')
    df = pd.DataFrame(getDataFrame())
    df['ConfirmedScale'] = np.log10(df['Confirmed'])
    fig = px.choropleth(df, 
                    locations='id', 
                    geojson=india_states, 
                    scope='asia',
                    color="ConfirmedScale",
                    hover_name='Name',
                    hover_data=['Confirmed'])
    fig.update_geos(fitbounds="locations", visible=False)
    fig.write_html(path)

def visualizeDeceased():
    path = os.path.join(BASE_DIR, 'templates', 'deceased_plot.html')
    df = pd.DataFrame(getDataFrame())
    df['DeceasedScale'] = np.log10(df['Deceased'])
    fig = px.choropleth(df, 
                    locations='id', 
                    geojson=india_states, 
                    scope='asia',
                    color="DeceasedScale",
                    hover_name='Name',
                    hover_data=['Deceased'])
    fig.update_geos(fitbounds="locations", visible=False)
    fig.write_html(path)

def visualizeRecovered():
    path = os.path.join(BASE_DIR, 'templates', 'recovered_plot.html')
    df = pd.DataFrame(getDataFrame())
    df['RecoveredScale'] = np.log10(df['Recovered'])
    fig = px.choropleth(df, 
                    locations='id', 
                    geojson=india_states, 
                    scope='asia',
                    color="RecoveredScale",
                    hover_name='Name',
                    hover_data=['Recovered'])
    fig.update_geos(fitbounds="locations", visible=False)
    fig.write_html(path)

def visualizeTested():
    path = os.path.join(BASE_DIR, 'templates', 'tested_plot.html')
    df = pd.DataFrame(getDataFrame())
    df['TestedScale'] = np.log10(df['Tested'])
    fig = px.choropleth(df, 
                    locations='id', 
                    geojson=india_states, 
                    scope='asia',
                    color="TestedScale",
                    hover_name='Name',
                    hover_data=['Tested'])
    fig.update_geos(fitbounds="locations", visible=False)
    fig.write_html(path)

    
    


    
    


    
    




    
    


    
    


    
    


    
    


