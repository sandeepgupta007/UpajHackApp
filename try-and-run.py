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
from sklearn import datasets,linear_model
import tkinter as tk
import tkinter.font as tkFont
try:
    import ttk as ttk
    import ScrolledText
except ImportError:
    import tkinter.ttk as ttk
    import tkinter.scrolledtext as ScrolledText
from pprint import pprint



conversation = watson_developer_cloud.ConversationV1(
    username='e91c46f8-af25-4f34-8fef-2770b88a7ae6',
    password='kHshOoKQggLE',
    version='2018-03-08'
)

def get_response(chat):

    ''' Calls the Watson API for responses'''

    workspace_id = 'b1d807f3-080c-4b9a-bdee-dead8ed75a1b'
    response = conversation.message(workspace_id=workspace_id, input={'text': chat})
    return response

def resp(chat):

    intents = []
    entities = []

    response = get_response(chat)
    pprint(response)

    for intent in response['intents']:
        intents.append(intent['intent'])

    for entity in response['entities']:
        entities.append(entity)

    msg_type(intents, entities, response)


def msg_type(intents, entities, response):

    if 'greetings' in intents:
        return greeting(response)

    if 'weather' in intents:
        return weather(entities)

    if 'crop_forecasting' in intents:
        return crop_forecasting()

    if 'cost' in intents:
        return cost(response)

    if 'pesticide' in intents:
        return pesticide(chat)

    if 'goodbyes' in intents:
        return bye()

def greeting(response):

    ''' returns greetings messages'''

    for text in response['output']['text']:
        print(text)


def weather(entities):

    location = entities[0]['value']
    location_id = location_suggestions(location)

    weather_data = pywapi.get_weather_from_weather_com(location_id)
    pprint(weather_data)


def location_suggestions(location):

    ''' facilitates search of location '''

    data = pywapi.get_location_ids(location)
    if len(data) is 1:
        for loc_id, location in data.items():
            return loc_id
    else:
        print ('There are number quite a few location with similar set of name, please be specific')
        for loc_id, location in data.items():
            print(location)


def cost(response):
    return 0

resp("weather jabalpur")
