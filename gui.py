#!/usr/bin/python3

# Created by Balraj 30/11/2016

# System libraries
import tkinter as tk
import sys

# External libraries
import pandas as pd
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import numpy as np

# My libraries
import analytics

class Application(tk.Frame):
    data = {}
    def __init__(self, pdData, master=None):
        super().__init__(master)
        master.minsize(500,550)
        self.pack()
        self.create_widgets(pdData)

    def create_widgets(self, pdData):
        # Assign the data
        self.pdData = pdData
        # setup The main label and pack it
        self.descLabel = tk.Label(self,text='Coursework 2: Python App for Analytics by Balraj',pady=5)
        self.descLabel.pack(side='top')
        # Create task widgets
        self.createTask2Widgets(pdData)
        self.createTask3Widgets(pdData)
        self.createTask4Widgets(pdData)
        self.createTask5Widgets(pdData)

    def createTask2Widgets(self,pdData):
        # setup Task 2 Frame and child frames
        self.task2Frame = tk.LabelFrame(self, text='Task 2: Views by country', padx=5, pady=5)
        self.t1inputFrame = tk.Frame(self.task2Frame,pady=2)
        self.buttonFrame = tk.Frame(self.task2Frame,pady=2)
        # setup Task 2 Doc ID label and pack it
        self.docIdEntryLabel = tk.Label(self.t1inputFrame, text='Document UUID')
        self.docIdEntryLabel.pack(side='left')
        # Task 2 Doc ID entry and pack it
        self.docIdEntry = tk.Entry(self.t1inputFrame)
        self.docIdEntry.pack(side='left')
        # Task 2 Doc ID submit button and pack it
        self.docIdEntrySubmit = tk.Button(self.buttonFrame, text='Group by country', command=self.drawTask2Hist)
        self.docIdEntrySubmit.pack(side='right')
        self.docIdEntrySubmitSecondary = tk.Button(self.buttonFrame, text='Group by Continent', command=self.drawTask2Hist)
        self.docIdEntrySubmitSecondary.pack(side='right')
        # Pack Task 2 frame and child frames
        self.t1inputFrame.pack()
        self.buttonFrame.pack()
        self.task2Frame.pack(padx=5,pady=5)
    
    def createTask3Widgets(self,pdData):
        # setup Task 3 Frame
        self.task3Frame = tk.LabelFrame(self, text='Task 3: Views by browser', padx=5, pady=5)
        # TODO: Add Graph for task 3
        self.task3ViewBtn = tk.Button(self.task3Frame, text='View graph', command=self.drawTask3Hist)
        self.task3ViewBtn.pack()
        # Pack Task 3 Frame
        self.task3Frame.pack(padx=5,pady=5)
    
    def createTask4Widgets(self,pdData):
        # Setup task 4 frame
        self.task4Frame = tk.LabelFrame(self,text='Task 4: Top 10 Reader profiles', padx=5, pady=5)
        # setup a listbox to display top 10 users and their time
        self.topTenListBox = tk.Listbox(self.task4Frame, width=40)
        self.topTenListBox.insert('end', 'Visitor UUID : Time (ms)')
        # Setup the data to display
        task4data = analytics.getTask4DataFrame(pdData)
        topTenVisitorList = task4data['visitor_uuid'].tolist()
        topTenVisitorTime = task4data['event_readtime'].tolist()
        # insert the data in the list box
        for i,item in enumerate(topTenVisitorList):
            itemString = str(i+1)+'. '+str(topTenVisitorList[i])+' : '+str(topTenVisitorTime[i])
            self.topTenListBox.insert('end', itemString)
        # Pack task 4 frame
        self.topTenListBox.pack()
        self.task4Frame.pack(padx=5,pady=5)
    
    def createTask5Widgets(self,pdData):
        # Setup task 5 Frame and child frames
        self.task5Frame = tk.LabelFrame(self,text='Task 5: Also likes functionality')
        self.task5UserInputFrame = tk.Frame(self.task5Frame)
        self.task5DocInputFrame = tk.Frame(self.task5Frame)
        self.task5OptionsFrame = tk.Frame(self.task5Frame)
        self.task5SubmitFrame = tk.Frame(self.task5Frame)
        # Add label and inputs for task5 user input frame
        self.task5UserEntryLabel = tk.Label(self.task5UserInputFrame, text='User UUID: ')
        self.task5UserEntry = tk.Entry(self.task5UserInputFrame)
        self.task5UserEntryLabel.pack(side='left')
        self.task5UserEntry.pack()
        # Add label and inputs for task5 doc input frame
        self.task5DocEntryLabel = tk.Label(self.task5DocInputFrame, text='Doc UUID: ')
        self.task5DocEntry = tk.Entry(self.task5DocInputFrame)
        self.task5DocEntryLabel.pack(side='left')
        self.task5DocEntry.pack()
        # Add options for task5Frame
        self.task5OptionsLabel = tk.Label(self.task5OptionsFrame, text='Select sort option: ')
        self.task5OptionsLabel.pack(side='left')
        OPTIONS = [
            "Sort by Part D",
            "Sort by Part E",
            "Sort by Part F"
        ]
        self.optionVar = tk.StringVar()
        self.optionVar.set(OPTIONS[0])
        self.task5Options = tk.OptionMenu(self.task5OptionsFrame, self.optionVar,*OPTIONS)
        self.task5Options.pack()
        # Button frame
        self.task5SubmitBtn = tk.Button(self.task5SubmitFrame, text='View top 10 list')
        self.task5SubmitBtn.pack()
        # Pack task5 frames
        self.task5UserInputFrame.pack()
        self.task5DocInputFrame.pack()
        self.task5OptionsFrame.pack()
        self.task5SubmitFrame.pack()
        self.task5Frame.pack(padx=5,pady=5)

    def drawTask2Hist(self):
        if self.docIdEntry.get() == '':
            self.displayPopup('Error','Please enter a document UUID')
            plt.barh([1,2,3], [22,33,77], align='center', alpha=0.4)
            plt.show()
        else:
            self.fig = Figure(figsize=(5,4), dpi=100)
            task2data = analytics.getFilteredTask2(self.pdData, self.docIdEntry.get())
            countries = task2data.groupby('visitor_country')['visitor_country']
            counts = task2data.groupby('visitor_country')['visitor_country'].count()
            print(counts)
            print(countries)
            self.p = counts.hist()
            self.p.set_xlabel('Country', fontsize = 15)
            self.p.set_ylabel('Views', fontsize = 15)
        # #self.a = self.fig.add_subplot(111)
        # #self.a.plot()
            self.canvas = FigureCanvasTkAgg(self.p, self.task2GraphFrame)
            self.canvas.show()
            self.canvas.get_tk_widget().pack()

    def drawTask3Hist(self):
        plt.barh([1,2,3], [22,33,77], align='center', alpha=0.4)
        plt.show()

    def displayPopup(self,title,message):
        self.top = tk.Toplevel()
        self.top.wm_geometry('300x150')
        self.top.title(title)
        self.msg = tk.Message(self.top, text=message)
        self.msg.pack()
        self.button = tk.Button(self.top, text="Dismiss", command=self.top.destroy)
        self.button.pack()