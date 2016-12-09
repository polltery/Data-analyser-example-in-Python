#!/usr/bin/python3

# Created by Balraj 29/11/2016

# System libraries
import json
from pprint import pprint
# External libraries 
import requests

# Loading JSON data via HTTP
def loadFromURL(url, printData=False):
    resp = requests.get(url=url, params=None)
    data = json.loads(resp.text)
    if printData:
        pprint(data)
    return data

# Loading JSON data locally
def loadFromFile(path='data.txt', printData=False, lineDelimited=True):
    data = []
    if lineDelimited:
        with open(path) as data_file:
            for line in data_file:
                data.append(json.loads(line))
    else:
        with open(path) as data_file:
            data = json.load(data_file)
    if printData:
        pprint(data)
    return data