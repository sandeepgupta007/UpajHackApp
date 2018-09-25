from django.shortcuts import render, HttpResponse


import sys
import json
import watson_developer_cloud
import pywapi
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
from math import sqrt
from random import seed
from random import randrange
from csv import reader
from datetime import datetime
import time
from sklearn import datasets,linear_model
import os.path

from sklearn.linear_model import LinearRegression

from django.contrib.staticfiles.templatetags.staticfiles import static
# Create your views here.

conversation = watson_developer_cloud.ConversationV1(
    username='e91c46f8-af25-4f34-8fef-2770b88a7ae6',
    password='kHshOoKQggLE',
    version='2018-03-08'
)

workspace_id = 'b1d807f3-080c-4b9a-bdee-dead8ed75a1b'



def load_csv(filename):
    dataset = list()
    # file_path = static(filename)
    file_path = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(file_path, 'static', filename)
    with open(file_path, 'r') as file:
        csv_reader = reader(file)
        for row in csv_reader:
            if not row:
                continue
            dataset.append(row)
    return dataset

# Calculate the mean value of a list of numbers
def mean(values):
	return sum(values) / float(len(values))

# Calculate covariance between x and y
def covariance(x, mean_x, y, mean_y):
	covar = 0.0
	for i in range(len(x)):
		covar += (x[i] - mean_x) * (y[i] - mean_y)
	return covar

# Calculate the variance of a list of numbers
def variance(values, mean):
	return sum([(x-mean)**2 for x in values])

# Calculate coefficients
def coefficients(X,Y):
	x = X
	y = Y
	x_mean, y_mean = mean(X), mean(Y)
	b1 = covariance(X, x_mean, Y, y_mean) / variance(X, x_mean)
	b0 = y_mean - b1 * x_mean
	return [b0, b1]

# Simple linear regression algorithm
def simple_linear_regression(X,Y):
	b0, b1 = coefficients(X,Y)
	return [b0,b1]

location = 'Jabalpur'
cultivated_area = 5
current_crop = -1
irrigation_facilities = -1
season = 'whole year'
value = True


def home(request):
    return render(request, 'bot/index.html')


def probable_location(location_ID):
    count = 0
    loc_id = ""
    for possible_location in location_ID:
        count = count + 1
        loc_id = possible_location
    
    if(count <= 1.0):
        return loc_id
    else:
        print('There are quite a few location with similar set of name, please be specific')
        for possible_location in location_ID:
            print(location_ID[possible_location])
            loc_id = "-1"
        return loc_id


def pesticides(chat):
    output = ""
    response = conversation.message(workspace_id = workspace_id, input={'text':chat})

    val = str(-1)
    for i in response['entities']:
        if(i['entity'] != [] and i['entity'] == 'disease'):
            val = i['value']
            break
    if(val == str(-1)):
        return output
    
    data = []
    data = load_csv('pesticides.csv')
    pest = str(-1)
    for i in  range(1, len(data)):
        if(data[i][0].lower() == val.lower()):
            pest = data[i][1].lower()
            break
    
    if(pest != str(-1)):
        output = str('It is advisable to use ' + data[i][1] + ' for '+ data[i][0]+ ' disease')
    else:
        output = str('It is advisable to use ' + 'Boron Hexa Choloride or ' + 'DDT ' + ' for this type of disease ' + data[i][0])

    return output


def bye():
    return str("Hope to see you again..!!")


def msp(crop):
    output = ""
    print(crop)
    data = []
    data = load_csv('crops.csv')
    msp_cost = -1
    now = datetime.now().year
    print(len(data))
    for i in range(1, len(data)):
        if(data[i][0].lower() == crop.lower()):
            msp_cost = i
            break
    

    if(msp_cost == -1):
        output = str('No data found for the crop, please try after some other crop')
    else:
        Year = []
        Price = []
        j = 1
        while(j < len(data[msp_cost])):
            Year.append(data[0][j])
            Price.append(data[msp_cost][j])
            j = j + 2
        
        X = []
        for j in Price:
            X.append(float(j))
        
        Y = []
        for j in Year:
            Y.append(int(j))
        
        # print(Y)
        # print(X)
        
        try:
            b0, b1 = simple_linear_regression(Y, X)
            # print(b0)
            # print(b1)
            current_year = datetime.now().year
            # current_year = 2018
            # print(current_year)
            prediction = current_year * b1 + b0
            if(prediction <= 0):
                print(' * ')
                output = str('Sorry! no prediction avialable')
            else:
                output = str('Minimum selling price of '+ crop+ ' ' +str(prediction))
        except:
            output = str('Sorry! no prediction avialable')
    return output




def cost(chat):
    output = ""
    response = conversation.message(workspace_id = workspace_id, input={'text':chat})
    print(response)
    crop_data = str(-1)
    if(response['entities'] != []):
        for i in response['entities']:
            for j in i:
                if(j == 'entity' and i[j] == 'crops'):
                    crop_data = i['value']
        
        output = msp(crop_data)
    else:
        output = str('Can you be more specific, for which crop you need cost')
    return output


def weather_intent(chat):
    output1 = ""
    output2 = ""

    response = conversation.message(workspace_id=workspace_id, input={'text':chat})
    if(location != -1):
        location_ID = pywapi.get_location_ids(location)
        loc_id = probable_location(location_ID)
        if(loc_id != str(-1)):
            try:
                now = 'current_conditions'
                if(response['entities'] != []):
                    for i in response['entities']:
                        for j in i:
                            if(j == 'entity' and i[j] == 'location'):
                                location_ID = pywapi.get_location_ids(i['values'])
                                loc_id = probable_location(location_ID)
                                if(loc_id == -1):
                                    return 0
                            if(j == 'entity' and i[j] == 'time'):
                                now = i['value']
                    Weather_details = pywapi.get_weather_from_weather_com(loc_id)

                    if(now == 'current_conditions'):
                        output1 = str('It is '+ Weather_details[now]['text']+' and '+Weather_details[now]['wind']['speed'] + 'Km/hr now in '+ Weather_details[now]['station'])
                    else:
                        overcast = 0
                        for i in Weather_details:
                            if(i == 'forecasts'):
                                for j in  Weather_details[i]:
                                    for k in j:
                                        if(k == 'day_of_week' and j[k].lower() == now):
                                            output1 = str('It is '+ j['day']['text'] + ' on ' + now)
                                        if(j['day']['text'] == 'overcast' or j['day']['text'] == 'storm'):
                                            overcast += 1
                        if(overcast <= 1):
                            output2 = str('No need to worry, there are no overcast for this week')
                        else:
                            output2 = str('There are quite a few chances for overcast, please be patient and calm')
                else:
                    Weather_details = pywapi.get_weather_from_weather_com(loc_id)
                    output1 = str('It is '+Weather_details[now]['text']+' and '+Weather_details[now]['wind']['speed'] + 'Km/hr windspeed now in '+ Weather_details[now]['station'])
            except:
                output1 = str('Server seems busy, cannot display weather information. till then have cup of tea')
    return(output1 + output2)



def greeting(chat):
    response = conversation.message(workspace_id = workspace_id, input={
        'text':chat
    })

    for i in response['output']:
        if(i == 'text'):
            return str(response['output']['text'][0])



def msg_type(chat, intent, values, entities, text):
    if(intent == 'greetings'):
        return greeting(chat)
    elif(intent == 'weather'):
        return weather_intent(chat)
    # elif(intent == 'crop_forecasting'):
    #     return crop_forecasting()
    elif(intent == 'cost'):
        return cost(chat)
    elif(intent == 'googbyes'):
        return bye()
    elif(intent == 'pesticide'):
        return pesticides(chat)


def resp(chat):
    print(chat)
    response = conversation.message(workspace_id=workspace_id, input={'text': chat})
    print(response)
    for i in response:
        if(str(i) == 'entities'):
            for j in response[i]:
                for k in j:
                    if(k == 'entity' and j[k] == 'location'):
                        location = j['value']
                        print(location)
                        # return HttpResponse("Message is sent")

    intent = []
    values = []
    text = []
    entities = []
    for i in response:
        if(str(i) == 'intents'):
            for j in response[i]:
                for k in j:
                    if(k == 'intent'):
                        intent.append(j[k])

    for intents in intent: 
        return msg_type(chat, intents, values, entities, text)
    return str(intent)


    return HttpResponse('Message sent')

def get_response(request):
    query = request.POST['query']
    print(query)
    # self.query.delete(0)

    response = resp(query)
    print(response)
    return HttpResponse("updated")