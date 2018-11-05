import sys
import watson_developer_cloud
import pywapi
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
from math import sqrt
from random import seed
from random import randrange
from csv import reader
import datetime
import time
from scipy import stats
import numpy as np
from sklearn import datasets,linear_model
from pprint import pprint
import pandas as pd
import json

from sklearn.tree import DecisionTreeClassifier

DATA_GOV_API ='579b464db66ec23bdd000001f4159aa056f849bb6c7922a7a5c2cc99'

conversation = watson_developer_cloud.ConversationV1(

    username='6c3fe2ff-40bd-4cc4-968a-a2d5f282e5ec',
    password='hWIJrde0H551',
    version='2018-03-08'
)

def get_response(chat):

    ''' Calls the Watson API for responses'''

    workspace_id = '650f9948-7391-4a98-bf15-996caee0fb0a'
    response = conversation.message(workspace_id=workspace_id, input={'text': chat})
    return response

def chatDriver(query):

    intents = []
    entities = []

    try:
        watson_replies = get_response(query)
        response = watson_replies.result
        pprint(response)
    except:
        return response_encoder('Sorry! Not available right now.')

    for intent in response['intents']:
        intents.append(intent['intent'])

    for entity in response['entities']:
        entities.append(entity)

    if 'hello' in intents:
        return greeting(response)

    if 'weather' in intents:
        return location_suggestions(entities)

    if 'crop_forecasting' in intents:
        return crop_forecasting(entities)

    if 'cost' in intents:
        return minimum_support_price_prediction(response)

    if 'pesticide' in intents:
        return pesticide(entities)

    if 'goodbyes' in intents:
        return bye()

    if not intents:
        return rephrase(response)

# Functions are defined below

def rephrase(response):

    ''' asks user to rephrase itself'''

    return response_encoder(response['output']['text'][0])

def greeting(response):

    ''' returns greetings messages'''

    return response_encoder(response['output']['text'][0])

def weather(location_id):

    ''' returns weather conditions for a given location id '''
    weather_data = pywapi.get_weather_from_weather_com(location_id)
    pprint(weather_data)

    response = {}
    response['temperature'] = "Temperature : " + str(weather_data['current_conditions']['temperature']) + " C"
    response['humidity'] = "Humidity : " + str(weather_data['current_conditions']['humidity'])
    response['windspeed'] = "Wind Speed : " + str(weather_data['current_conditions']['wind']['speed'])

    return response

def location_suggestions(entities):

    ''' facilitates search of location '''
    try:
        location = entities[0]['value']
    except:
        location = entities

    data = pywapi.get_location_ids(location)
    print(data)
    if len(data) is 1:
        for loc_id, location in data.items():
            return response_encoder(weather(loc_id))
    else:
        for loc_id, location in data.items():
            if 'India' in location:
                return response_encoder(weather(loc_id))
            else:
                print ('There are number quite a few location with similar set of name, please be specific')
                return response_encoder(data)

def pesticide(entities):

    ''' returns pesticide information '''

    value = entities[0]['value']
    pesticide = pd.read_csv('csv_files/pesticides.csv')
    data = pesticide.loc[pesticide['disease'] == value]
    return response_encoder(data.iloc[0]['pesticide'])

def minimum_support_price_prediction(response):

    ''' provides a predicted minimum support price '''

    print(response['entities'][0])
    crop = response['entities'][0]['value']

    dataframe = pd.read_csv('csv_files/crops.csv')
    msp_cost = -1
    now = datetime.datetime.now()

    try:
        crop_price_history = dataframe.loc[dataframe['crop'] == crop]
    except:
        crop_price_history = []
        return 0

    crop_price_history = crop_price_history.drop(columns="crop")
    crop_price_history = pd.melt(crop_price_history, var_name='year', value_name='price')

    x = crop_price_history['year'].tolist()
    y = crop_price_history['price'].tolist()

    x = np.array(x).astype(np.float)
    y = np.array(y).astype(np.float)

    slope, intercept, r_value, p_value, std_err = stats.linregress(x,y)

    print (slope, intercept, r_value, p_value, std_err)

    try:
    	current_year = now.year
    	predicition = current_year*slope + intercept

    	if(predicition <= 0):
    		print (' * ')
    		output = str('Sorry! no prediction avialable')
    	else:
    		output = str('Minimum selling price of '+ crop+ ' ' +str(predicition))
    except:
    	output = str('Sorry! no prediction avialable')
    return response_encoder(output)

def crop_forecasting():

	data = pd.read_csv('csv_files/crop_production.csv')
	now = datetime.datetime.now()

	if(now.month >= 7 and now.month <= 10):
		season = 'kharif'
	elif(now.month >= 10 and now.month <= 11):
		season = 'autumn'
	elif((now.month >= 11 and now.month <= 12) or now.month <= 1):
		season = 'rabi'
	else:
		season = 'whole year'

	if(True):
		# print (str(season).lower() + " " + str(location).lower())
		Crop = {}
		for i in range(1,len(data)):
			#print (str(data[i][1]).lower() + " " + str(data[i][3]).lower())
			#print (data[i][3].lower() + " " + season.lower())
			#a = list(season.lower())
			#print (a)
			data[i][3] = str(data[i][3].lower())
			data[i][3] = data[i][3].strip()
			data[i][1] = str(data[i][1].lower())
			data[i][1] = data[i][1].strip()
			if(str(location.lower()) == data[i][1]  and season.lower() == data[i][3].lower()):
				try:
					Crop[data[i][4]]=1
					# Production.append(float(data[i][6])/float(data[i][5]))
					# Year.append(data[i][2])
				except:
					continue
		output1 =  str('Here is a list of possible crop which can be grown with there approximate production on your cultivated area will be shown if possible')
		for i in Crop:
			Production = []
			Year = []
			for j in range(1,len(data)):
				data[j][3] = str(data[j][3].lower())
				data[j][3] = data[j][3].strip()
				data[j][1] = str(data[j][1].lower())
				data[j][1] = data[j][1].strip()
				if(str(location.lower()) == data[j][1]  and season.lower() == data[j][3].lower() and i == data[j][4]):
					try:
						Production.append(float(data[j][6])/float(data[j][5]))
						Year.append(data[j][2])
					except:
						continue

			if(len(Year) == 0):
				output2 = str('No dataset found for your location or region please try after some days')
			else:
				X = []
				for j in range(len(Year)):
					X.append(int(Year[j]))
				[float(j) for j in Production]
				# print (Production)
				# print (X)
				try:
					[b0,b1] = simple_linear_regression(X,Production)
					current_year = now.year
					predicition = current_year*b1+b0
					if(float(predicition) == 0):
						continue
					output1 += str(i + " " + str(predicition) + " ")
					#print (i + " " +str(predicition))
				except:
					continue
	if(output2 == ""):
		return (output1)
	else:
		return (output2)

def response_encoder(response):

    ''' encodes message to the proper format '''

    message = {}
    message['bubbles'] = 1
    message['text'] = []

    if type(response) == str:
        message['text'].append('<div class="message new"><figure class="avatar"><img src="chathead.png" /></figure>' + response + '</div>')
    elif type(response) == dict:
        for key, value in response.items():
            message['text'].append('<div class="message new"><figure class="avatar"><img src="chathead.png" /></figure>' + value + '</div>')

        message['bubbles'] = len(response)

    print(message)

    return message
