#functions for fitting and plotting
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
from matplotlib.font_manager import FontProperties
import scipy.optimize as opt
import numpy as np

#fitting equations here
def kdfit(P, Kd, S, O):
	return S*(P/(P+Kd))+O

def quad(P, Kd, S, O, L): #in this form, L refers to the ligand held at constant concentration
	a = P+L+Kd
	return S*((a-(((a**2)-(4*P*L))**0.5))/(2*L))+O

#decided to make separate functions for each fitting equation also to make my life easier
def getkdfit(x, y, fiteq, p0, units):
	fits_x = []
	fits_y = []
	y_norm = []
	param_table = [["Kd ("+units+")"],["S"],["O"],["R^2"]]
	x = np.array(x) #making them arrays makes the math easier
	y = np.array(y)
	for i in range(len(y)):
		popt, _ = opt.curve_fit(fiteq, x, y[i], p0=p0)
		fits_x.append(np.geomspace(x[len(x)-1], x[0], 50))   
		fits_y.append(fiteq(fits_x[i], *popt))
		#use estimated parameters to normalize anisotropy to be fraction bound
		y_norm.append((y[i]-popt[2])/popt[1])
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
	return fits_x, fits_y, y_norm, param_table

def getquadfit(x, y, conc_L, fiteq, p0, units):
	fits_x = []
	fits_y = []
	y_norm = []
	param_table = [["Kd ("+units+")"],["S"],["O"],["R^2"]]
	x = np.array(x)
	y = np.array(y)
	for i in range(len(y)):
		#use a lambda function to fix L in the quad equation
		popt, _ = opt.curve_fit(lambda P, Kd, S, O: fiteq(P, Kd, S, O, conc_L), x, y[i], p0=p0)
		fits_x.append(np.geomspace(x[len(x)-1], x[0], 50))   
		fits_y.append(fiteq(fits_x[i], popt[0], popt[1], popt[2], conc_L))
		#use estimated parameters to normalize anisotropy to be fraction bound
		y_norm.append((y[i]-popt[2])/popt[1])
		#calculate R-squared
		residuals = (y[i] - fiteq(x, popt[0], popt[1], popt[2], conc_L))
		ss_res = np.sum(residuals**2)
		ss_tot = np.sum((y[i]-np.mean(y[i]))**2)
		r_sq = 1-(ss_res/ss_tot)
		#format parameters for table
		param_table[0].append(str(round(popt[0],2)))
		param_table[1].append(str(round(popt[1],4)))
		param_table[2].append(str(round(popt[2],4)))
		param_table[3].append(str(round(r_sq,4)))
	return fits_x, fits_y, y_norm, param_table

#general function for scatter plot with a log x scale with a table underneath
def logplot(x, y, labels, units, y_ax, fits_x, fits_y, param, 
	title, color, marker_size, marker, line_width, line_style, legend, svg, plotname, filepath):
	fig = plt.figure(figsize=(7.0,9.0), dpi=100) #forces figure size and shape 
	fig.subplots_adjust(left=0.125, right=0.95, bottom=0.05, top=0.9) #adjusts margins
	ax1 = plt.subplot2grid((6, 1), (0,0), rowspan=4) #subplot for scatter
	table = plt.subplot2grid((6, 1), (5,0)) #subplot for table
	#setup lists for table widths, labels, and colors
	#I have an initial list for each and add to it so that the first column has an empty first row with no color
	#labels and color are both lists specified in the config
	table_widths = [0.12]
	for i in range(len(y)):
		table_widths.append(0.12)
	table_labels = [' ']
	for a in labels:
		table_labels.append(a)
	table_color = ['w']
	for a in color:
		table_color.append(a)
	table = plt.table(cellText=param, loc="lower center", colLabels=table_labels,
		cellLoc="center", colWidths=table_widths, colColours=table_color)
	table.auto_set_font_size(False)
	table.set_fontsize(11)
	#for first column and first row, bold the font
	for (row,column), cell in table.get_celld().items():
		if (row==0) or (column==0):
			cell.set_text_props(fontproperties=FontProperties(weight='bold', size=11))
	table.scale(1.25,2) #scales column width and row heights
	plt.axis('off') #removes plot axes for the table
	ax1.set_title(title, fontsize=13)
	ax1.set_xscale('log')
	ax1.set_ylabel(y_ax, fontsize=13)
	ax1.set_xlabel("[Protein] ("+units+")", fontsize=13)
	#this part assumes that y is a list of lists. each inner list is one sample to plot
	legendicons = []
	for i in range(len(y)):
		ax1.scatter(x, y[i], s=20*marker_size, color=color[i], marker=marker, label=labels[i])
		ax1.plot(fits_x[i], fits_y[i], color=color[i], linewidth=line_width, linestyle=line_style)
		#this is to get legends with marker and line
		if legend == True:
			legendicons.append(mlines.Line2D([],[],color=color[i], marker=marker,
				linestyle=line_style, label=labels[i]))
	if legend == True:
		ax1.legend(legendicons, labels, fontsize=12, loc='upper left')
	#save as png for quick viewing, svg for further editing
	plt.savefig(filepath+plotname+'.png')
	if svg == True:
		plt.savefig(filepath+plotname+'.svg')

#plot a single sample
def singleplot(data, sample, labels, units, fiteq, p0, normalization, title,
	color, marker_size, marker, line_width, line_style, legend, svg, plotname, filepath):
	conc = []
	aniso = [[]] #as above, the logplot function takes a list of lists
	labels_temp = [labels[0]]
	#split up data into a list of concentrations and a list of anisotropy values
	for i in range(len(data[0])):
		conc.append(data[0][i][0])
	for i in range(len(data[0])):
		aniso[0].append(data[0][i][1])
	p0_norm = [20.0, 1.0, 0.0]
	fits_x, fits_y, y_norm, param = getkdfit(conc, aniso, fiteq, p0, units)
	#plot data as anisotropy
	logplot(conc, aniso, labels_temp, units, 'Anisotropy', fits_x, fits_y,
		param, title, color, marker_size, marker, line_width, line_style, legend, svg, plotname, filepath)
	#plot data as fraction bound
	if normalization == 1:
		normfits_x, normfits_y, _, normparam = getkdfit(conc, y_norm, fiteq, p0_norm, units)
		logplot(conc, y_norm, labels_temp, units, 'Fraction Bound', normfits_x, normfits_y,
			normparam, title+' (Normalized)', color, marker_size, marker,
			line_width, line_style, legend, svg, plotname+'_normalized', filepath)

def multiplot(data, perplot, labels, units, fiteq, p0, normalization, title,
	color, marker_size, marker, line_width, line_style, legend, svg, plotname, filepath):
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
	#the rest of this is to figure out how many plots to make based on the perplot in the config
	#plotcount gives the numer of plots minus one. leftovers gives the last one
	plotcount=len(aniso)/perplot
	leftovers=len(aniso)%perplot
	#masterindex counts up per sample plotted. plotcounter counts the plots so I can number the files.
	masterindex = 0
	plotcounter = 1
	p0_norm = [20.0, 1.0, 0.0]
	for n in range(plotcount):#for each full plot to be made (no leftover plot)
		aniso_temp = []
		labels_temp = []
		for i in range(perplot):#for each sample per plot, append lists with anisotropy and label of the sample based on masterindex
			aniso_temp.append(aniso[masterindex])
			labels_temp.append(labels[masterindex])
			masterindex+=1
		#fit and plot using the condensed sample list
		fits_x, fits_y, y_norm, param = getkdfit(conc, aniso_temp, fiteq, p0, units)
		logplot(conc, aniso_temp, labels_temp, units, 'Anisotropy', fits_x, fits_y,
			param, title, color, marker_size, marker, line_width, line_style, legend, svg, plotname+str(plotcounter), filepath)
		if normalization == 1:
			normfits_x, normfits_y, _, normparam = getkdfit(conc, y_norm, fiteq, p0_norm, units)
			logplot(conc, y_norm, labels_temp, units, 'Fraction Bound', normfits_x, normfits_y,
				normparam, title+' (Normalized)', color, marker_size, marker, line_width,
				line_style, legend, svg, plotname+str(plotcounter)+'_normalized', filepath)
		plotcounter+=1
	#deal with the rest of the samples if there are any leftovers. code is same as above.
	if leftovers>0:
		aniso_temp = []
		labels_temp = []
		for n in range(leftovers):
			aniso_temp.append(aniso[masterindex])
			labels_temp.append(labels[masterindex])
			masterindex+=1
		fits_x, fits_y, y_norm, param = getkdfit(conc, aniso_temp, fiteq, p0, units)
		logplot(conc, aniso_temp, labels_temp, units, 'Anisotropy', fits_x, fits_y,
			param, title, color, marker_size, marker, line_width, line_style, legend, svg, plotname+str(plotcounter), filepath)
		if normalization == 1:
			normfits_x, normfits_y, _, normparam = getkdfit(conc, y_norm, fiteq, p0_norm, units)
			logplot(conc, y_norm, labels_temp, units, 'Fraction Bound', normfits_x, normfits_y,
				normparam, title+' (Normalized)', color, marker_size, marker, line_width,
				line_style, legend, svg, plotname+str(plotcounter)+'_normalized', filepath)
#it was easier for me to just define separate functions for a quadratic fit
def quad_singleplot(data, sample, labels, units, conc_L, fiteq, p0, normalization, 
	title, color, marker_size, marker, line_width, line_style, legend, svg, plotname, filepath):
	conc = []
	aniso = [[]] #as above, the logplot function takes a list of lists
	labels_temp = [labels[0]]
	#split up data into a list of concentrations and a list of anisotropy values
	for i in range(len(data[0])):
		conc.append(data[0][i][0])
	for i in range(len(data[0])):
		aniso[0].append(data[0][i][1])
	fits_x, fits_y, y_norm, param = getquadfit(conc, aniso, conc_L, fiteq, p0, units)
	#plot data as anisotropy
	logplot(conc, aniso, labels_temp, units, 'Anisotropy', fits_x, fits_y,
		param, title, color, marker_size, marker, line_width, line_style, legend, svg, plotname, filepath)
	#plot data as fraction bound
	p0_norm = [20.0, 1.0, 0.0]
	if normalization == 1:
		normfits_x, normfits_y, _, normparam = getquadfit(conc, y_norm, conc_L, fiteq, p0_norm, units)
		logplot(conc, y_norm, labels_temp, units, 'Fraction Bound', normfits_x, normfits_y,
			normparam, title+' (Normalized)', color, marker_size, marker,
			line_width, line_style, legend, svg, plotname+'_normalized', filepath)

def quad_multiplot(data, perplot, labels, units, conc_L, fiteq, p0, normalization, 
	title, color, marker_size, marker, line_width, line_style, legend, svg, plotname, filepath):
	#fix sqrt with normalization
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
	#the rest of this is to figure out how many plots to make based on the perplot in the config
	#plotcount gives the numer of plots minus one. leftovers gives the last one
	plotcount=len(aniso)/perplot
	leftovers=len(aniso)%perplot
	#masterindex counts up per sample plotted. plotcounter counts the plots so I can number the files.
	masterindex = 0
	plotcounter = 1
	p0_norm = [20.0, 1.0, 0.0]
	for n in range(plotcount):#for each full plot to be made (no leftover plot)
		aniso_temp = []
		labels_temp = []
		for i in range(perplot):#for each sample per plot, append lists with anisotropy and label of the sample based on masterindex
			aniso_temp.append(aniso[masterindex])
			labels_temp.append(labels[masterindex])
			masterindex+=1
		#fit and plot using the condensed sample list
		fits_x, fits_y, y_norm, param = getquadfit(conc, aniso_temp, conc_L, fiteq, p0, units)
		logplot(conc, aniso_temp, labels_temp, units, 'Anisotropy', fits_x, fits_y,
			param, title, color, marker_size, marker, line_width, line_style, legend, svg, plotname+str(plotcounter), filepath)
		if normalization == 1:
			normfits_x, normfits_y, _, normparam = getquadfit(conc, y_norm, conc_L, fiteq, p0_norm, units)
			logplot(conc, y_norm, labels_temp, units, 'Fraction Bound', normfits_x, normfits_y,
				normparam, title+' (Normalized)', color, marker_size, marker, line_width,
				line_style, legend, svg, plotname+str(plotcounter)+'_normalized', filepath)
		plotcounter+=1
	#deal with the rest of the samples if there are any leftovers. code is same as above.
	if leftovers>0:
		aniso_temp = []
		labels_temp = []
		for n in range(leftovers):
			aniso_temp.append(aniso[masterindex])
			labels_temp.append(labels[masterindex])
			masterindex+=1
		fits_x, fits_y, y_norm, param = getquadfit(conc, aniso_temp, conc_L, fiteq, p0, units)
		logplot(conc, aniso_temp, labels_temp, units, 'Anisotropy', fits_x, fits_y,
			param, title, color, marker_size, marker, line_width, line_style, legend, svg, plotname+str(plotcounter), filepath)
		if normalization == 1:
			normfits_x, normfits_y, _, normparam = getquadfit(conc, y_norm, conc_L, fiteq, p0_norm, units)
			logplot(conc, y_norm, labels_temp, units, 'Fraction Bound', normfits_x, normfits_y,
				normparam, title+' (Normalized)', color, marker_size, marker, line_width,
				line_style, legend, svg, plotname+str(plotcounter)+'_normalized', filepath)