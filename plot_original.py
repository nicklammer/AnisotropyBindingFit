import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import scipy.optimize as opt
import numpy as np

#implement a function that chooses which equation to fit to from the config (have Kd fit and quadratic)

def kdfit(P, Kd, S, O):
	return S*(P/(P+Kd))+O


def single(data, units, fiteq, color, marker, line_style, filepath):
	conc = []
	aniso = []
	for i in range(len(data)):
		conc.append(data[i][0])
		aniso.append(data[i][1])

	#getting a fit for the curve
	p0 = [20.0, 0.1, 0.05]
	popt, pcov = opt.curve_fit(fiteq, conc, aniso, p0=p0)
	print("Kd: "+str(popt[0]), "S: "+str(popt[1]), "O: "+str(popt[2]))
	fit_x = np.geomspace(conc[len(conc)-1], conc[0], 50)   
	fit_y = fiteq(fit_x, *popt)
	#calculate R-squared
	residuals = aniso - fiteq(conc, *popt)
	ss_res = np.sum(residuals**2)
	ss_tot = np.sum((aniso-np.mean(aniso))**2)
	r_sq = 1-(ss_res/ss_tot)
	print("R^2: "+str(r_sq))

	param_table = [["Kd ("+units+")",str(round(popt[0]))],
		["S",str(round(popt[1],4))],
		["O", str(round(popt[2], 4))], 
		["R^2", str(round(r_sq, 4))]]
	#plot everything
	fig = plt.figure()
	ax1 = plt.subplot2grid((1, 5), (0,0), colspan=3)
	table_plot = plt.subplot2grid((1,5), (0,4))
	table_widths = [0.5, 1.0]
	table = plt.table(cellText=param_table, loc="center", 
		cellLoc="center", colWidths=table_widths)
	table.auto_set_font_size(False)
	table.set_fontsize(11)
	table.scale(1.25,2)
	plt.axis('off')

	ax1.plot(conc, aniso, color+marker, label='anisotropy')
	ax1.plot(fit_x, fit_y, color+line_style, label="fit")
	ax1.set_xscale('log')
	#ax1.legend(loc='upper left')
	ax1.set_ylabel("Anisotropy")
	ax1.set_xlabel("[Protein] ("+units+")")

	plt.savefig(filepath+'test.png')
	plt.savefig(filepath+'test.svg')

def multiple(data, labels, units, fiteq, color, marker, line_style, filepath):
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

	#getting a fit for the curve
	fits_x = []
	fits_y = []
	param_table = [["Kd ("+units+")"],["S"],["O"],["R^2"]]

	p0 = [20.0, 0.1, 0.05]
	for i in range(len(aniso)):
		popt, pcov = opt.curve_fit(fiteq, conc, aniso[i], p0=p0)
		fits_x.append(np.geomspace(conc[len(conc)-1], conc[0], 50))   
		fits_y.append(fiteq(fits_x[i], *popt))
		#calculate R-squared
		residuals = aniso[i] - fiteq(conc, *popt)
		ss_res = np.sum(residuals**2)
		ss_tot = np.sum((aniso[i]-np.mean(aniso[i]))**2)
		r_sq = 1-(ss_res/ss_tot)
		#format parameters for table
		param_table[0].append(str(round(popt[0])))
		param_table[1].append(str(round(popt[1],4)))
		param_table[2].append(str(round(popt[2],4)))
		param_table[3].append(str(round(r_sq,4)))
	#print(param_table)
	#plot everything--------------------------------------
	#fig = plt.figure()
	fig = plt.figure(figsize=(9.375,9.375), dpi=100)
	#fig.subplots_adjust(hspace=0.3)
	fig.subplots_adjust(left=0.1, right=0.9)
	ax1 = plt.subplot2grid((6, 1), (0,0), rowspan=4)
	table_plot = plt.subplot2grid((6, 1), (5,0))
	table_widths = [0.12]
	for i in range(len(aniso)):
		table_widths.append(0.12)
	table_labels = [' ']
	for x in labels:
		table_labels.append(x)
	table_color = ['w']
	for x in color:
		table_color.append(x)
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

	for i in range(len(aniso)):
		ax1.plot(conc, aniso[i], color[i]+marker, label='anisotropy')
		ax1.plot(fits_x[i], fits_y[i], color[i]+line_style, label="fit")
	
	plt.savefig(filepath+'test.png')
	plt.savefig(filepath+'test.svg')

def multiple_test(data, labels, units, fiteq, color, marker, line_style, filepath):
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
	if len(aniso)%4>0:
		plotcount+=1
	print(plotcount)

	indexcounter = 0
	plotcounter = 1
	fourcounter = 0

	for n in range(plotcount):
		aniso_temp = []
		labels_temp = []
		while indexcounter<4:
			try:
				aniso_temp.append(aniso[indexcounter+fourcounter])
				labels_temp.append(labels[indexcounter+fourcounter])
				indexcounter+=1
			except:
				break

		fits_x = []
		fits_y = []
		param_table = [["Kd ("+units+")"],["S"],["O"],["R^2"]]

		p0 = [20.0, 0.1, 0.05]
		for i in range(len(aniso_temp)):
			popt, pcov = opt.curve_fit(fiteq, conc, aniso_temp[i], p0=p0)
			fits_x.append(np.geomspace(conc[len(conc)-1], conc[0], 50))   
			fits_y.append(fiteq(fits_x[i], *popt))
			#calculate R-squared
			residuals = aniso_temp[i] - fiteq(conc, *popt)
			ss_res = np.sum(residuals**2)
			ss_tot = np.sum((aniso_temp[i]-np.mean(aniso_temp[i]))**2)
			r_sq = 1-(ss_res/ss_tot)
			#format parameters for table
			param_table[0].append(str(round(popt[0])))
			param_table[1].append(str(round(popt[1],4)))
			param_table[2].append(str(round(popt[2],4)))
			param_table[3].append(str(round(r_sq,4)))

		fig = plt.figure(figsize=(9.375,9.375), dpi=100)
		fig.subplots_adjust(left=0.1, right=0.9)
		ax1 = plt.subplot2grid((6, 1), (0,0), rowspan=4)
		table_plot = plt.subplot2grid((6, 1), (5,0))
		table_widths = [0.12]
		for i in range(len(aniso_temp)):
			table_widths.append(0.12)
		table_labels = [' ']
		for x in labels_temp:
			table_labels.append(x)
		table_color = ['w']
		for x in color:
			table_color.append(x)
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

		for i in range(len(aniso_temp)):
			ax1.plot(conc, aniso_temp[i], color[i]+marker, label='anisotropy')
			ax1.plot(fits_x[i], fits_y[i], color[i]+line_style, label="fit")
		
		plt.savefig(filepath+'test_'+str(plotcounter)+'.png')
		plt.savefig(filepath+'test_'+str(plotcounter)+'.svg')

		fourcounter+=4
		plotcounter+=1
		indexcounter=0


def multiple_test2(data, labels, units, fiteq, color, marker, line_style, filepath):
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
	fourcounter = 0

	for n in range(plotcount):
		aniso_temp = []
		labels_temp = []
		for i in range(4):
			aniso_temp.append(aniso[masterindex])
			labels_temp.append(labels[masterindex])
			masterindex+=1

		fits_x = []
		fits_y = []
		param_table = [["Kd ("+units+")"],["S"],["O"],["R^2"]]

		p0 = [20.0, 0.1, 0.05]
		for i in range(len(aniso_temp)):
			popt, pcov = opt.curve_fit(fiteq, conc, aniso_temp[i], p0=p0)
			fits_x.append(np.geomspace(conc[len(conc)-1], conc[0], 50))   
			fits_y.append(fiteq(fits_x[i], *popt))
			#calculate R-squared
			residuals = aniso_temp[i] - fiteq(conc, *popt)
			ss_res = np.sum(residuals**2)
			ss_tot = np.sum((aniso_temp[i]-np.mean(aniso_temp[i]))**2)
			r_sq = 1-(ss_res/ss_tot)
			#format parameters for table
			param_table[0].append(str(round(popt[0])))
			param_table[1].append(str(round(popt[1],4)))
			param_table[2].append(str(round(popt[2],4)))
			param_table[3].append(str(round(r_sq,4)))

		fig = plt.figure(figsize=(9.375,9.375), dpi=100)
		fig.subplots_adjust(left=0.1, right=0.9)
		ax1 = plt.subplot2grid((6, 1), (0,0), rowspan=4)
		table_plot = plt.subplot2grid((6, 1), (5,0))
		table_widths = [0.12]
		for i in range(len(aniso_temp)):
			table_widths.append(0.12)
		table_labels = [' ']
		for x in labels_temp:
			table_labels.append(x)
		table_color = ['w']
		for x in color:
			table_color.append(x)
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

		for i in range(len(aniso_temp)):
			ax1.plot(conc, aniso_temp[i], color[i]+marker, label='anisotropy')
			ax1.plot(fits_x[i], fits_y[i], color[i]+line_style, label="fit")
		
		plt.savefig(filepath+'test_'+str(plotcounter)+'.png')
		plt.savefig(filepath+'test_'+str(plotcounter)+'.svg')

		fourcounter+=4
		plotcounter+=1

	aniso_temp = []
	labels_temp = []
	for n in range(leftovers):
		aniso_temp.append(aniso[masterindex])
		labels_temp.append(labels[masterindex])
		masterindex+=1

	fits_x = []
	fits_y = []
	param_table = [["Kd ("+units+")"],["S"],["O"],["R^2"]]

	p0 = [20.0, 0.1, 0.05]
	for i in range(len(aniso_temp)):
		popt, pcov = opt.curve_fit(fiteq, conc, aniso_temp[i], p0=p0)
		fits_x.append(np.geomspace(conc[len(conc)-1], conc[0], 50))   
		fits_y.append(fiteq(fits_x[i], *popt))
		#calculate R-squared
		residuals = aniso_temp[i] - fiteq(conc, *popt)
		ss_res = np.sum(residuals**2)
		ss_tot = np.sum((aniso_temp[i]-np.mean(aniso_temp[i]))**2)
		r_sq = 1-(ss_res/ss_tot)
		#format parameters for table
		param_table[0].append(str(round(popt[0])))
		param_table[1].append(str(round(popt[1],4)))
		param_table[2].append(str(round(popt[2],4)))
		param_table[3].append(str(round(r_sq,4)))

	fig = plt.figure(figsize=(9.375,9.375), dpi=100)
	fig.subplots_adjust(left=0.1, right=0.9)
	ax1 = plt.subplot2grid((6, 1), (0,0), rowspan=4)
	table_plot = plt.subplot2grid((6, 1), (5,0))
	table_widths = [0.12]
	for i in range(len(aniso_temp)):
		table_widths.append(0.12)
	table_labels = [' ']
	for x in labels_temp:
		table_labels.append(x)
	table_color = ['w']
	for x in color:
		table_color.append(x)
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

	for i in range(len(aniso_temp)):
		ax1.plot(conc, aniso_temp[i], color[i]+marker, label='anisotropy')
		ax1.plot(fits_x[i], fits_y[i], color[i]+line_style, label="fit")
	
	plt.savefig(filepath+'test_'+str(plotcounter)+'.png')
	plt.savefig(filepath+'test_'+str(plotcounter)+'.svg')
