#!/usr/bin/python3

# Created by Balraj 29/11/2016

# External libraries
import pandas as pd

# My libraries
import continents

# setting pandas configs
pd.options.mode.chained_assignment = None  # default='warn'

# Print task 2 for CMD
def printTask2(pdData, doc_id):
    print('Here are views by country for the given document')
    pdData = getFilteredTask2(pdData, doc_id)
    countryCount = pdData.groupby('visitor_country')['visitor_country'].count()
    print('Visits grouped by country:')
    print(countryCount)
    continentCount = getFilteredTask2ByContinent(pdData,doc_id)
    print('Countries by continent')
    print(continentCount)
    
def getFilteredTask2(pdData, doc_id):
    return pdData.loc[pdData['subject_doc_id'] == doc_id]

def getFilteredTask2ByContinent(pdData, doc_id):
    pdData = getFilteredTask2(pdData, doc_id)
    for index, row in pdData.iterrows():
        # Get the continent using continent module
        cont = continents.continentName(continents.countryToContinent(row['visitor_country']))
        pdData.loc[index,'visitor_country'] = cont
    return pdData.groupby('visitor_country')['visitor_country'].count()

# Print task 3 for CMD
def printTask3(pdData, verbose):
    print('Here are views from browsers : ')
    if not verbose:
        print(pdData.groupby('visitor_useragent')['visitor_useragent'].count())
    else:
        pdData = pdData['visitor_useragent'].str.replace('Mozilla.+','Mozilla')
        pdData = pdData.reset_index()
        pdData = pdData['visitor_useragent'].str.replace('Opera.+','Opera')
        pdData = pdData.reset_index()
        pdData = pdData['visitor_useragent'].str.replace('Dalvik.+','Dalvik')
        pdData = pdData.reset_index()
        pdData = pdData['visitor_useragent'].str.replace('UCWEB.+','UCWEB')
        pdData = pdData.reset_index()
        print(pdData.groupby('visitor_useragent').count())

# Print task 4 for CMD
def printTask4(pdData):
    print('The TOP 10 Reader profiles are : ')
    print(getTask4DataFrame(pdData))

# Task 4 function
def getTask4DataFrame(pdData):
    return pdData.sort_values(by='event_readtime',ascending=0)[['visitor_uuid','event_readtime']].head(10)
    
# Print task 5 for CMD
def printTask5(pdData,doc_id,visitor_id):
    # Get the docs of the reader
    docs = getDocsOfUser(pdData,visitor_id)
    relativeUsers = []
    print('Docs of user '+visitor_id+':')
    for docK,docV in docs:
        print(docK)
        tempUsers = getUsersOfDoc(pdData,docK)
        print('Readers of doc '+docK+':')
        for tempUserK,tempUserV in tempUsers:
            add = True
            print(tempUserK)
            for relativeUser in relativeUsers:
                if tempUserK == relativeUser:
                    add = False
                    pass
            if add and tempUserK != visitor_id:
                relativeUsers.append(tempUserK)
    print(relativeUsers)
    relativeDocs = []
    for relativeUser in relativeUsers:
        tempDocs = getDocsOfUser(pdData,relativeUser)
        print('Docs of reader '+relativeUser+':')
        for tempDocK,tempDocV in tempDocs:
            add = True
            print(tempDocK)
            for relativeDoc in relativeDocs:
                if tempDocK == relativeDoc:
                    add = False
                    pass
            if add and doc_id != tempDocK:
                relativeDocs.append(tempDocK)
    print(relativeDocs)

# Task 5, part a : Returns Documents for a given user
def getDocsOfUser(pdData,user_id):
    pdData = pdData.loc[pdData['visitor_uuid'] == user_id]
    return pdData.groupby('subject_doc_id')['subject_doc_id']

# Task 5, part b : Returns Users for a given document
def getUsersOfDoc(pdData,doc_id):
    pdData = pdData.loc[pdData['subject_doc_id'] == doc_id]
    return pdData.groupby('visitor_uuid')['visitor_uuid']