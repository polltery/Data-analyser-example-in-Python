#!/usr/bin/python3

# Created by Balraj 29/11/2016

# System libraries
import sys, argparse
# External libraries
import pandas as pd
import tkinter as tk
# My libraries
import jsonLoader, analytics, gui

# For Parsing arguments when using as a command line interface
parser = argparse.ArgumentParser(description='Coursework 2 Application for analytics of issuu datasets. To use with GUI, do not provide any arguments.')

# setting up CMD arguments
parser.add_argument('-task_id', metavar='t', help='The ID of the task (2,3,4 or 5) as given in the PDF', type=int)
parser.add_argument('-user_uuid',metavar='u', help='visitor_uuid from dataset (required for task_id 5)')
parser.add_argument('-doc_uuid',metavar='d', help='subject_doc_uuid from dataset (required for task_id 2 and 5)')

# Parse all the arguments
args = parser.parse_args()

# Main code for CMD mode
def cmdMode():
    if args.task_id == 5 and not args.user_uuid and not args.doc_uuid:
        print('please provide user_uuid and doc_uuid \nuse --help to know more')
        return
    # The task to be performed provided with dataframe and task id
    printTask(getPDDataFromJSON(),args.task_id)

# For CMD, Do validations for input and print task using analytics
def printTask(pdData,task_id):
    if task_id == 2:
        if not args.doc_uuid:
            print('please provide doc_uuid\nuse --help to know more')
            return
        else:
            analytics.printTask2(pdData, args.doc_uuid)
    elif task_id == 3:
        analytics.printTask3(pdData, True)
    elif task_id == 4:
        analytics.printTask4(pdData)
    elif task_id == 5:
        if not args.user_uuid and not args.doc_uuid:
            print('please provide user_uuid and doc_uuid \nuse --help to know more')
            return
        else:
            analytics.printTask5(pdData,args.doc_uuid,args.user_uuid)

# Getting the Pandas data frame from JSON
def getPDDataFromJSON(path='data.txt'):
     # Reading data from a file using jsonLoader
    data = jsonLoader.loadFromFile(path, False, True)
    # Creating a data frame for pandas library
    return pd.DataFrame(data, columns=['ts','visitor_uuid','visitor_username','visitor_source','visitor_device','visitor_useragent','visitor_ip','visitor_country','visitor_referrer','env_type','env_doc_id','env_adid','event_type','event_readtime','subject_type','env_type','subject_doc_id','subject_page','cause'])

# Main code for GUI mode
def guiMode():
    # setup tk for gui
    root = tk.Tk()
    interface = gui.Application(master=root, pdData=getPDDataFromJSON())
    interface.mainloop()

# check args length, if 0, then start in GUI mode
if len(sys.argv) > 1:
    cmdMode()
else:
    guiMode()