from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from django.contrib.staticfiles.templatetags.staticfiles import static
from . import conversation as cn
import sys
import js2py
# from urllib2 import urlopen
import pprint
import json
import csv
from bs4 import BeautifulSoup
import requests

import pandas as pd
import csv

# Create your views here.
crop = []
prod = []
rain_year = []
rain = []
total_states = []


def home(request):
    global crop
    global prod
    global rain
    global rain_year
    global total_states
    data = pd.read_csv('csv_files/check.csv')
    state = "madhya pradesh"
    year = "2011"
    crop = []
    prod = []
    rain = []
    rain_year = []
    total_states = []
    rain_state = "madhya pradesh"
    for d in data['state']:
        if(d not in total_states):
            total_states.append(d)
    # print("helllloooooo")
    # print(total_states)
    try:
        if(request.method == "POST"):
            state = request.POST['state']
            # print(state)
        elif(state == ""):
            state = "madhya pradesh"
    
        if(request.method == "POST"):
            year = request.POST['year']
            # print(year)
            if(year == ""):
                year = 2010
    except:
        if(request.method == "POST"):
            rain_state = request.POST['rain_state']
            if(rain_state == ""):
                rain_state = "madhya pradesh"

    data = data.groupby(['state', 'crop', 'year'], as_index = False)['production '].sum()
    data = data.loc[(data['state'] == state) & (data['year'] == int(year))]
    data = data.sort_values('production ', ascending = False)
    data = data.head()
    for obj in data['crop']:
        crop.append(obj)
    for obj in data['production ']:
        prod.append(obj)

    
        
    data = pd.read_csv('csv_files/rainfall_data.csv')
    data = data.loc[data['SUBDIVISION'] == rain_state]
    data = data.fillna(data.mean())
        
    for r in data['ANNUAL']:
        rain.append(r)
    for y in data['YEAR']:
        rain_year.append(str(y))

    # print(rain)
    # print(rain_year)

    object = {
        "crop" : crop,
        "prod" : prod,
        "state" : state,
        "year" : year,
        "rain" : rain,
        "rain_year" : rain_year,
        "rain_state" : rain_state,
        "total_states" : total_states,
    }
    return render(request, 'bot/index.html', object)

def get_response(request):
    query = request.POST['query']

    response = cn.chatDriver(query)

    return JsonResponse(response, safe=False)

# def plot(request):
    

#     # df = pd.DataFrame({'production' : prod}, index = crop)
#     # plot = df.plot.pie(y='production', figsize=(10, 10))
#     # print(plot)
#     return render(request, 'bot/index.html', {"crop" : crop, "prod" : prod, "state" : state, "year" : year})

# def rainfall_patterns(request):
#     global rain
#     global rain_year
#     rain = []
#     rain_year = []
#     if(request.method == "POST"):
#         rain_state = request.POST['rain_state']
#         if(rain_state == ""):
#             rain_state = "madhya pradesh"
    
#     data = pd.read_csv('csv_files/rainfall_data.csv')
#     data = data.loc[data['SUBDIVISION'] == rain_state]
#     data = data.fillna(data.mean())
    
#     for r in data['ANNUAL']:
#         rain.append(r)
#     for y in data['YEAR']:
#         rain_year.append(str(y))

#     # print(rain)
#     # print(rain_year)
#     return render(request, 'bot/index.html', {"rain" : rain, "rain_year" : rain_year, "rain_state" : rain_state})