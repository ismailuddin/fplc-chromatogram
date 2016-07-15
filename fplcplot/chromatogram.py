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

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def importDataFromExcelFile(filename):
	"""
	Parses Excel .XLS (93-2003) file to extract
	curves for UV absorbance, conductivity,
	buffer B percentage, fractions. Each curve
	is extracted it with it's corresponding x-values
	being the volume (mL).
	
	## Arguments
	filename: String value of Excel file, including the
	extension.

	"""
	input_file = pd.read_excel("%s" % filename)
	uvTrace = input_file.iloc[2:,0:2].as_matrix()
	conductivityTrace = input_file.iloc[2:,4:6].as_matrix()
	percentageB = input_file.iloc[2:,6:8].fillna('0').as_matrix()
	fractions = input_file.iloc[2:,14:16].fillna('0')
	
	return uvTrace, conductivityTrace, percentageB, fractions

def convertBufferB(percentage, A, B):
	"""
	Convert the value of percentage buffer B
	to an absolute value of concentration.
	"""

	a = (100 - percentage) * A
	b = percentage * B
	return (a + b)/100.0

def plotTraces(file_list, title, output=True, f_format=".png", y_lower=0, y_upper=100, second_trace=False, buffer_A=10.0, buffer_B=400.0):
	"""
	Function for plotting parsed
	----------------------------------------------------------------
	Arg        	|	Description
	----------------------------------------------------------------
	file_list  	|	Python list with .XLS file names 
	----------------------------------------------------------------
	title 		|	Graph title
	----------------------------------------------------------------
	output 		|	Set by default to True, wherein the first 
				|	filename
				|	from file_list is used. Otherwise, specify
				|	filename for outputted file. 
	----------------------------------------------------------------
	f_format   	|	Default is '.png'. '.PDF' also supported.
	----------------------------------------------------------------
	y_lower		|	Lower limit for y-axis as integer
	----------------------------------------------------------------                    
	y_upper		|	Upper limit for y-axis as integer
	----------------------------------------------------------------                    
	second_trace|	Default is False. Set either to 'buffer_b' to
				|	plot buffer B percentage on second y-axis, or
				|	'conductivity' to plot conductivity trace on
				|	second y-axis.
	----------------------------------------------------------------
	"""
	
	sns.set_context("notebook", font_scale=1.5, rc={"lines.linewidth": 2.5})
	sns.set_style({"legend.frameon": True})
	
	fig = plt.figure(figsize=(12,6))
	ax1 = fig.add_subplot(111)
	ax1.set_xlabel("Volume (mL)")
	ax1.set_ylabel("Absorbance at 280 nm (a.u.)")
	ax1.set_title("%s" % title, y=1.1)
	
	
	ax1.set_ylim([y_lower, y_upper])

	j = 0

	for trace in file_list:
		title = trace[0:-4].title()
		uvTrace, conductivityTrace, percentageB, fractions = importDataFromExcelFile("%s" % trace)
		ax1.plot(uvTrace[0:,0], uvTrace[0:,1], label=title)
		ax1.yaxis.grid(alpha=0.5)
		ax1.xaxis.grid(False)
		ax1.legend()

		# Plotting fraction lanes using only first .XLS file
		if j == 0:
			ax2 = ax1.twiny()
			fraction_xticks = filter(lambda x: x != '0',fractions.iloc[0:,0].values.tolist())
			fraction_labels = filter(lambda x: x != '0',fractions.iloc[0:,1].values.tolist())
			a = [i.encode('ascii', 'ignore') for i in fraction_labels]
			b = ax1.get_xticks().tolist()
			ax2.set_xticks(b)
			ax2.set_xticks(fraction_xticks[::])
			ax2.set_xticklabels(a[::], rotation='vertical', fontsize=12)
			ax2.grid(alpha=0.5)
		
		# Plot buffer B absolute concentration as a second trace for first .XLS file
		if second_trace == 'buffer_b_abs':
			if j == 0:
				ax3 = ax1.twinx()
				bufferB_x = filter(lambda x: x != '0', percentageB[0:,0])
				bufferB = percentageB[0:len(bufferB_x),1]
				bufferB_abs = [convertBufferB(x, buffer_A, buffer_B) for x in bufferB]
				ax3.plot(bufferB_x, bufferB_abs, sns.xkcd_rgb["pale red"])
				ax3.set_ylabel("Buffer B (mM)")
				ax3.grid(False)


		# Plot buffer B percentage as a second trace for first .XLS file
		elif second_trace == 'buffer_b':
			if j == 0:
				ax3 = ax1.twinx()
				bufferB_x = filter(lambda x: x != '0', percentageB[0:,0])
				bufferB = percentageB[0:len(bufferB_x),1]
				ax3.plot(bufferB_x, bufferB, sns.xkcd_rgb["pale red"])
				ax3.set_ylabel("Buffer B (%)")
				ax3.grid(False)

		# Plot % conductivity trace as a second trace using the first .XLS file
		elif second_trace == 'conductivity':
			if j == 0:
				ax3 = ax1.twinx()
				cond_vol = conductivityTrace[0:,0]
				cond = conductivityTrace[0:,1]
				ax3.plot(cond_vol, cond, sns.xkcd_rgb["goldenrod"])
				ax3.set_ylabel("Conductivity (%)")
				ax3.grid(False)

		j += 1

	if output == True:
		plt.savefig("%s%s" % (file_list[0][:-4], f_format), dpi=300, bbox_inches='tight')
		print("%s%s outputted." % (file_list[0][:-4], f_format))
	elif output == False:
		pass
	else:
		plt.tight_layout()
		plt.savefig("%s%s" % (output, f_format), dpi=300, bbox_inches='tight')
		print("%s%s outputted." % (output, f_format))