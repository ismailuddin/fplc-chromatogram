# UNICORN 5.0/6.0 FPLC chromatogram curves plotter
# Copyright (C) 2016, Ismail Uddin
# www.github.com/ismailuddin/
# www.scienceexposure.com
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

from Tkinter import *
from ttk import *
import tkFileDialog
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os
from fplcplot.chromatogram import plotTraces

class App:

	def __init__(self, master):
		self.master = master
		frame = Frame(master)
		frame.pack(pady=5, padx=5)
		self.filename = ''

		self.fileSelectLabel = Label(frame, text='Select Excel file with data' )
		self.fileSelectLabel.grid(row=0, padx=5, pady=5, columnspan=2)

		self.openFileBtn = Button(frame, text="Open file", command=self.loadFile)
		self.openFileBtn.grid(row=1, padx=5, pady=5, columnspan=2)

		self.titleLabel= Label(frame, text="Title for graph:")
		self.titleLabel.grid(row=2, padx=5, pady=5, columnspan=2)

		self.title = StringVar()
		self.titleEntry = Entry(frame, font=(15), textvariable=self.title)
		self.titleEntry.grid(row=3, padx=5, pady=5, columnspan=2)

		self.yLimitsLabel= Label(frame, text="Y-limits")
		self.yLimitsLabel.grid(row=4, padx=5, pady=5, columnspan=2)

		self.yLower = StringVar()
		self.yLowerEntry = Entry(frame, font=(15), textvariable=self.yLower)
		self.yLowerEntry.grid(row=5, column=0, padx=5, pady=5)

		self.yUpper = StringVar()
		self.yUpperEntry = Entry(frame, font=(15), textvariable=self.yUpper)
		self.yUpperEntry.grid(row=5, column=1, padx=5, pady=5)

		self.filenameExportLabel = Label(frame, text="Filename for export:")
		self.filenameExportLabel.grid(row=6, padx=5, pady=5, columnspan=2)

		self.filenameExport = StringVar()
		self.filenameExportEntry = Entry(frame, font=(15), textvariable=self.filenameExport)
		self.filenameExportEntry.grid(row=7, padx=5, pady=5, columnspan=2)

		self.fileFormatLabel = Label(frame, text="File format:")
		self.fileFormatLabel.grid(row=8, padx=5, pady=5, column=0)

		self.secondTraceLabel = Label(frame, text="Second trace:")
		self.secondTraceLabel.grid(row=8, padx=5, pady=5, column=1)

		self.fileFormat = StringVar()
		self.fileFormat.set(".png")

		self.fileFormatSelect = OptionMenu(frame, self.fileFormat, ".png", ".pdf")
		self.fileFormatSelect.grid(row=9, column=0, padx=5, pady=5)

		self.secondTrace = StringVar()
		self.secondTrace.set("None")

		secondTraceSelect = OptionMenu(frame, self.secondTrace, "None", "buffer_b", "conductivity")
		secondTraceSelect.grid(row=9, column=1, padx=5, pady=5)

		self.plotBtn = Button(frame, text="Plot data", command=self.plot)
		self.plotBtn.grid(row=10, padx=5, pady=5, columnspan=2)

		label = Label(frame, text="(C) 2016, Ismail Uddin \n www.github.com/ismailuddin/")
		label.grid(row=11, padx=5, pady=5, columnspan=2)

	def loadFile(self):
		extensions = [('Excel file', '.xls')]
		self.filenamePath = tkFileDialog.askopenfilename(filetypes=extensions, title='Choose your data file')
		print("%s file selected." % os.path.normcase(self.filenamePath))
		self.filename = os.path.normcase(self.filenamePath).split("\\")[-1]
		print self.filename
		
		
	def plot(self):
		plotTraces([self.filename], self.title.get(), output=self.filenameExport.get(), f_format=self.fileFormat.get(), y_lower=int(self.yLower.get()), y_upper=int(self.yUpper.get()), second_trace=self.secondTrace.get())
		plt.show()


root = Tk()
root.wm_title('UNICORN 6 - AKTA Chromatogram plotter')
app = App(root)
root.geometry("500x415+20+20")
root.mainloop()
