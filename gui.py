#!/usr/bin/python3

# Created by Balraj 30/11/2016

# System libraries
import tkinter as tk

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
        master.minsize(500,500)
        self.pack()
        self.create_widgets(pdData)

    def create_widgets(self, pdData):
        self.pdData = pdData
        # setup The main label and pack it
        self.descLabel = tk.Label(self,text='Coursework 2: Python App for Analytics by Balraj',pady=5)
        self.descLabel.pack(side='top')
        # setup Task 2 Frame
        self.task2Frame = tk.LabelFrame(self, text='Task 2: Views by country', padx=5, pady=5)
        # setup Task 2 Doc ID label and pack it
        self.docIdEntryLabel = tk.Label(self.task2Frame, text='Document UUID')
        self.docIdEntryLabel.pack(side='left')
        # Task 2 Doc ID entry and pack it
        self.docIdEntry = tk.Entry(self.task2Frame)
        self.docIdEntry.pack(side='left')
        # Task 2 Doc ID submit button and pack it
        self.docIdEntrySubmit = tk.Button(self.task2Frame, text='Submit', command=self.drawTask2Hist)
        self.docIdEntrySubmit.pack(side='right')
        self.task2GraphFrame = tk.Frame(self)
        # Pack Task 2 frame
        self.task2Frame.pack(padx=5,pady=5)
        # Pack task 2 frame again to insert the graph
        self.task2Frame.pack()
        self.task2GraphFrame.pack()
        # setup Task 3 Frame
        self.task3Frame = tk.LabelFrame(self, text='Task 3: Views by browser', padx=5, pady=5)
        # TODO: Add Graph for task 3
        self.graphLabel = tk.Label(self.task3Frame, text='GRAPH 3 GOES HERE')
        self.graphLabel.pack()
        # Pack Task 3 Frame
        self.task3Frame.pack(padx=5,pady=5)
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

    def drawTask2Hist(self):
        if self.docIdEntry.get() == '':
            self.displayPopup('Error','Please enter a document UUID')
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
    #     self.hi_there = tk.Button(self)
    #     self.hi_there["text"] = "Hello World\n(click me)"
    #     self.hi_there["command"] = self.say_hi
    #     self.hi_there.pack(side="top")
    #     self.quit = tk.Button(self, text="QUIT", fg="red",
    #                           command=root.destroy)
    #     f = Figure(figsize=(5,4), dpi=100)
    #     canvas = FigureCanvasTkAgg(f, master=root)
    #     canvas.get_tk_widget().grid(row=1, column=3, rowspan=6)
    #     self.quit.pack(side="bottom")
    #     p = f.gca()
    #     p.hist([0,0,0], [0,0,0])
    #     p.set_xlabel('Median Value', fontsize = 15)
    #     p.set_ylabel('Frequency', fontsize = 15)
    #     canvas.show()

    # def say_hi(self):
    #     print("hi there, everyone!")

    def displayPopup(self,title,message):
        self.top = tk.Toplevel()
        self.top.wm_geometry('300x300')
        self.top.title(title)
        self.msg = tk.Message(self.top, text=message)
        self.msg.pack()
        self.button = tk.Button(self.top, text="Dismiss", command=self.top.destroy)
        self.button.pack()