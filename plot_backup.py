import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import scipy.optimize as opt
import numpy as np

#implement a function that chooses which equation to fit to from the config (have Kd fit and quadratic)

def kdfit(P, Kd, S, O):
	return S*(P/(P+Kd))+O

def logplot(x, y, labels, units, fiteq, color, marker, line_style, plotname, filepath):
	fits_x = []
	fits_y = []
	param_table = [["Kd ("+units+")"],["S"],["O"],["R^2"]]

	p0 = [20.0, 0.1, 0.05]
	for i in range(len(y)):
		popt, pcov = opt.curve_fit(fiteq, x, y[i], p0=p0)
		fits_x.append(np.geomspace(x[len(x)-1], x[0], 50))   
		fits_y.append(fiteq(fits_x[i], *popt))
		#calculate R-squared
		residuals = y[i] - fiteq(x, *popt)
		ss_res = np.sum(residuals**2)
		ss_tot = np.sum((y[i]-np.mean(y[i]))**2)
		r_sq = 1-(ss_res/ss_tot)
		#format parameters for table
		param_table[0].append(str(round(popt[0],2)))
		param_table[1].append(str(round(popt[1],4)))
		param_table[2].append(str(round(popt[2],4)))
		param_table[3].append(str(round(r_sq,4)))

	fig = plt.figure(figsize=(9.375,9.375), dpi=100)
	fig.subplots_adjust(left=0.1, right=0.9)
	ax1 = plt.subplot2grid((6, 1), (0,0), rowspan=4)
	table_plot = plt.subplot2grid((6, 1), (5,0))
	table_widths = [0.12]
	for i in range(len(y)):
		table_widths.append(0.12)
	table_labels = [' ']
	for a in labels:
		table_labels.append(a)
	table_color = ['w']
	for a in color:
		table_color.append(a)
	table = plt.table(cellText=param_table, loc="upper center", colLabels=table_labels,
		cellLoc="center", colWidths=table_widths, colColours=table_color)
	table.auto_set_font_size(False)
	table.set_fontsize(11)
	for (row,column), cell in table.get_celld().items():
		if (row==0) or (column==0):
			cell.set_text_props(fontproperties=FontProperties(weight='bold', size=11))
	table.scale(1.25,2)
	plt.axis('off')
	ax1.set_xscale('log')
	#ax1.legend(loc='upper left')
	ax1.set_ylabel("Anisotropy")
	ax1.set_xlabel("[Protein] ("+units+")")

	for i in range(len(y)):
		ax1.plot(x, y[i], color[i]+marker, label='anisotropy')
		ax1.plot(fits_x[i], fits_y[i], color[i]+line_style, label="fit")
	
	plt.savefig(filepath+plotname+'.png')
	plt.savefig(filepath+plotname+'.svg')

def plotfour(data, labels, units, fiteq, color, marker, line_style, plotname, filepath):
	conc = []
	aniso = []
	holder = []
	for i in range(len(data[0])):
		conc.append(data[0][i][0])
	for i in range(len(data)):
		for n in range(len(data[i])):
			holder.append(data[i][n][1])
		aniso.append(holder)
		holder=[]
	
	plotcount=len(aniso)/4
	leftovers=len(aniso)%4
	masterindex = 0
	plotcounter = 1

	for n in range(plotcount):
		aniso_temp = []
		labels_temp = []
		for i in range(4):
			aniso_temp.append(aniso[masterindex])
			labels_temp.append(labels[masterindex])
			masterindex+=1
		logplot(conc, aniso_temp, labels_temp, units, fiteq, color, marker, 
			line_style, plotname+str(plotcounter), filepath)
		plotcounter+=1

	if leftovers>0:
		aniso_temp = []
		labels_temp = []
		for n in range(leftovers):
			aniso_temp.append(aniso[masterindex])
			labels_temp.append(labels[masterindex])
			masterindex+=1
		logplot(conc, aniso_temp, labels_temp, units, fiteq, color, marker, 
			line_style, plotname+str(plotcounter), filepath)