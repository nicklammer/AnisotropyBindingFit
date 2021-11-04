#functions for fitting and plotting
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
from matplotlib.font_manager import FontProperties
matplotlib.rcParams['font.sans-serif'] = "Arial"
matplotlib.rcParams['font.family'] = "sans-serif"
plt.rcParams['svg.fonttype'] = 'none'
#from scipy.stats import chisquare
import scipy.optimize as opt
import numpy as np

#fitting equations here
def kdfit(P, Kd, S, O):
	return S*(P/(P+Kd))+O

def quad(P, Kd, S, O, L): #in this form, L refers to the ligand held at constant concentration
	a = P+L+Kd
	return S*((a-(((a**2)-(4*P*L))**0.5))/(2*L))+O

#def hill(P, Kd, n, S, O):
#	return S*((P**n)/((P**n)+(Kd**n)))+O

def hill(P, Kd, n, m, S, O):
	#return S*((P**(n**m))/((P**(n**m))+(Kd**(n**m))))+O
	return	S*((P**(n)/((P**(n)+(Kd**(n))))))+O

def comp():#placeholder for competition fitting
	return "WIP"

def r_squared(y, residuals):
	ss_res = np.sum(residuals**2)
	ss_tot = np.sum((y-np.mean(y))**2)
	r_sq = 1-(ss_res/ss_tot)
	return r_sq

# def chi_squared(obs, exp):#calculate chi_squared (this probably doesn't need to be it's own thing)
# 	chi_sq = chisquare(obs, f_exp=exp) #returns (chi_sq, p-value)
# 	return chi_sq[0]
	
#decided to make separate functions for each fitting equation also to make my life easier
def getkdfit(x, y, fiteq, p0, units):
	fits_x = []
	fits_y = []
	y_norm = []
	#param_table = [["Kd ("+units+")"],["S"],["O"],["R^2"],["Chi^2"]]
	param_table = [["Kd ("+units+")"],["S"],["O"],["R^2"]]
	for i in range(len(y)):
		x[i] = np.array(x[i])
		y[i] = np.array(y[i])
		popt, _ = opt.curve_fit(kdfit, x[i], y[i], p0=p0, bounds=((0,0,0),(np.inf,np.inf,np.inf)))
		fits_x.append(np.geomspace(x[i][len(x[i])-1], x[i][0], 50))   
		fits_y.append(kdfit(fits_x[i], *popt))
		#use estimated parameters to normalize anisotropy to be fraction bound
		y_norm.append((y[i]-popt[2])/popt[1])
		#calculate R-squared
		residuals = y[i] - kdfit(x[i], *popt)
		r_sq = r_squared(y[i], residuals)
		#calculate chi-squared
		# y_expected = kdfit(x[i], *popt)
		# chi_sq = chi_squared(y[i],y_expected)
		#format parameters for table
		param_table[0].append(str(round(popt[0],2)))
		param_table[1].append(str(round(popt[1],4)))
		param_table[2].append(str(round(popt[2],4)))
		param_table[3].append(str(round(r_sq,4)))
		#param_table[4].append(str(round(chi_sq,4)))
	return fits_x, fits_y, y_norm, param_table

def getquadfit(x, y, ligand, fiteq, p0, units):
	fits_x = []
	fits_y = []
	y_norm = []
	#param_table = [["Kd ("+units+")"],["S"],["O"],["R^2"],["Chi^2"]]
	param_table = [["Kd ("+units+")"],["S"],["O"],["R^2"]]
	for i in range(len(y)):
		x[i] = np.array(x[i])
		y[i] = np.array(y[i])
		#use a lambda function to fix L in the quad equation
		popt, _ = opt.curve_fit(lambda P, Kd, S, O: quad(P, Kd, S, O, ligand[i]), 
			x[i], y[i], p0=p0, bounds=((0,0,0),(np.inf,np.inf,np.inf)))
		fits_x.append(np.geomspace(x[i][len(x[i])-1], x[i][0], 50))   
		fits_y.append(quad(fits_x[i], popt[0], popt[1], popt[2], ligand[i]))
		#use estimated parameters to normalize anisotropy to be fraction bound
		y_norm.append((y[i]-popt[2])/popt[1])
		#calculate R-squared
		residuals = (y[i] - quad(x[i], popt[0], popt[1], popt[2], ligand[i]))
		r_sq = r_squared(y[i], residuals)
		#calculate chi-squared
		# y_expected = quad(x[i], popt[0], popt[1], popt[2], ligand[i])
		# chi_sq = chi_squared(y[i],y_expected)
		#format parameters for table
		param_table[0].append(str(round(popt[0],2)))
		param_table[1].append(str(round(popt[1],4)))
		param_table[2].append(str(round(popt[2],4)))
		param_table[3].append(str(round(r_sq,4)))
		#param_table[4].append(str(round(chi_sq,4)))
	return fits_x, fits_y, y_norm, param_table

def gethillfit(x, y, fiteq, p0, units):
	fits_x = []
	fits_y = []
	y_norm = []
	p0_n = [p0[0], 1.0, 1.0, p0[1], p0[2]]
	#param_table = [["Kd ("+units+")"],["n"],["S"],["O"],["R^2"]]
	param_table = [["Kd ("+units+")"],["n"],["m"],["S"],["O"],["R^2"]]
	for i in range(len(y)):
		x[i] = np.array(x[i])
		y[i] = np.array(y[i])
		#popt, _ = opt.curve_fit(hill, x[i], y[i], p0=p0_n, bounds=((0,0,0,0),(np.inf,np.inf,np.inf,np.inf)))
		popt, _ = opt.curve_fit(hill, x[i], y[i], p0=p0_n, bounds=((0,0,0,0,0),(np.inf,np.inf,np.inf,np.inf,np.inf)))
		fits_x.append(np.geomspace(x[i][len(x[i])-1], x[i][0], 50))   
		fits_y.append(hill(fits_x[i], *popt))
		#use estimated parameters to normalize anisotropy to be fraction bound
		y_norm.append((y[i]-popt[3])/popt[2])
		#calculate R-squared
		residuals = y[i] - hill(x[i], *popt)
		r_sq = r_squared(y[i], residuals)
		#format parameters for table
		param_table[0].append(str(round(popt[0],2)))
		param_table[1].append(str(round(popt[1],2)))
		param_table[2].append(str(round(popt[2],4)))
		param_table[3].append(str(round(popt[3],4)))
		param_table[4].append(str(round(popt[4],4)))
		#param_table[4].append(str(round(r_sq,4)))
		param_table[5].append(str(round(r_sq,4)))
	return fits_x, fits_y, y_norm, param_table

#general function for scatter plot with a log x scale with a table underneath
def logplot(x, y, labels, units, y_ax, fits_x, fits_y, param, 
	title, color, marker_size, marker, line_width, line_style, 
	plot_title_size, x_title_size, y_title_size, x_tick_label_size,
	y_tick_label_size, x_tick_size, y_tick_size, legend, png, svg, 
	plotname, filepath, showplot):
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
			cell.set_text_props(fontproperties=FontProperties(weight='bold', size=12))
	table.scale(1.25,2) #scales column width and row heights
	plt.axis('off') #removes plot axes for the table
	ax1.set_xscale('log')
	#labels, font sizes, and tick sizes
	ax1.set_title(title, fontsize=plot_title_size)
	ax1.set_ylabel(y_ax, fontsize=x_title_size)
	ax1.set_xlabel("[Protein] ("+units+")", fontsize=y_title_size)
	ax1.tick_params(axis='x', which='major', labelsize=x_tick_label_size)
	ax1.tick_params(axis='y', which='major', labelsize=y_tick_label_size)
	ax1.tick_params(axis='x', which='major', length=x_tick_size)
	ax1.tick_params(axis='x', which='minor', length=x_tick_size/2)
	ax1.tick_params(axis='y', which='major', length=y_tick_size)

	#fix the dumb margins here
	x_upper = max([series[0] for series in x])
	x_lower = min([series[-1] for series in x])
	ax1.set_xlim(x_lower/2, x_upper*2)
	#this part assumes that y is a list of lists. each inner list is one sample to plot
	legendicons = []
	for i in range(len(y)):
		ax1.scatter(x[i], y[i], s=20*marker_size, color=color[i], marker=marker, label=labels[i])
		ax1.plot(fits_x[i], fits_y[i], color=color[i], linewidth=line_width, linestyle=line_style)
		#this is to get legends with marker and line
		if legend == True:
			legendicons.append(mlines.Line2D([],[],color=color[i], marker=marker,
				linestyle=line_style, label=labels[i]))
	if legend == True:
		ax1.legend(legendicons, labels, fontsize=13, loc='upper left')
	#save as png for quick viewing, svg for further editing
	if png == True:
		plt.savefig(filepath+plotname+'.png')
	if svg == True:
		plt.savefig(filepath+plotname+'.svg')
	#show plot(s) in pop-up window
	if showplot == True:
		plt.show()

def allplot(conc, anisos, perplot, labels, units, y_title, fiteq, p0, normalization, title,
	color, marker_size, marker, line_width, line_style, plot_title_size, x_title_size, 
	y_title_size, x_tick_label_size, y_tick_label_size, x_tick_size, y_tick_size, 
	legend, png, svg, plotname, filepath, showplot):
	#this is to figure out how many plots to make based on the perplot in the config
	#plotcount gives the numer of plots minus one. leftovers gives the last one
	plotcount=int(len(anisos)/perplot)
	leftovers=int(len(anisos)%perplot)
	#masterindex counts up per sample plotted. plotcounter counts the plots so I can number the files.
	masterindex = 0
	plotcounter = 1
	p0_norm = [p0[0], 1.0, 0.0]
	for n in range(plotcount):#for each full plot to be made (no leftover plot)
		conc_temp = []
		anisos_temp = []
		labels_temp = []
		for i in range(perplot):#for each sample per plot, append lists with anisotropy and label of the sample based on masterindex
			conc_temp.append(conc[masterindex])
			anisos_temp.append(anisos[masterindex])
			labels_temp.append(labels[masterindex])
			masterindex+=1
		#fit and plot using the condensed sample list
		if fiteq == "kdfit":
			fits_x, fits_y, y_norm, param = getkdfit(conc_temp, anisos_temp, fiteq, p0, units)
		elif fiteq == "hill":
			fits_x, fits_y, y_norm, param = gethillfit(conc_temp, anisos_temp, fiteq, p0, units)
		logplot(conc_temp, anisos_temp, labels_temp, units, y_title, fits_x, fits_y,
			param, title, color, marker_size, marker, line_width, line_style, plot_title_size, 
			x_title_size, y_title_size, x_tick_label_size, y_tick_label_size, x_tick_size, 
			y_tick_size, legend, png, svg, plotname+str(plotcounter), filepath, showplot)
		if normalization == 1:
			if fiteq == "kdfit":
				normfits_x, normfits_y, _, normparam = getkdfit(conc_temp, y_norm, fiteq, p0_norm, units)
			elif fiteq == "hill":
				normfits_x, normfits_y, _, normparam = gethillfit(conc_temp, y_norm, fiteq, p0_norm, units)
			logplot(conc_temp, y_norm, labels_temp, units, 'Fraction Bound', normfits_x, normfits_y,
				normparam, title+' (Normalized)', color, marker_size, marker, line_width,
				line_style,plot_title_size, x_title_size, y_title_size, x_tick_label_size,
				y_tick_label_size, x_tick_size, y_tick_size, legend, png, svg, 
				plotname+str(plotcounter)+'_normalized', filepath, showplot)
		plotcounter+=1
	#deal with the rest of the samples if there are any leftovers. code is same as above.
	if leftovers>0:
		conc_temp = []
		anisos_temp = []
		labels_temp = []
		for n in range(leftovers):
			conc_temp.append(conc[masterindex])
			anisos_temp.append(anisos[masterindex])
			labels_temp.append(labels[masterindex])
			masterindex+=1
		if fiteq == "kdfit":
			fits_x, fits_y, y_norm, param = getkdfit(conc_temp, anisos_temp, fiteq, p0, units)
		elif fiteq == "hill":
			fits_x, fits_y, y_norm, param = gethillfit(conc_temp, anisos_temp, fiteq, p0, units)
		logplot(conc_temp, anisos_temp, labels_temp, units, y_title, fits_x, fits_y,
			param, title, color, marker_size, marker, line_width, line_style, 
			plot_title_size, x_title_size, y_title_size, x_tick_label_size,
			y_tick_label_size, x_tick_size, y_tick_size,legend, png, svg, 
			plotname+str(plotcounter), filepath, showplot)
		if normalization == 1:
			if fiteq == "kdfit":
				normfits_x, normfits_y, _, normparam = getkdfit(conc_temp, y_norm, fiteq, p0_norm, units)
			elif fiteq == "hill":
				normfits_x, normfits_y, _, normparam = gethillfit(conc_temp, y_norm, fiteq, p0_norm, units)
			logplot(conc_temp, y_norm, labels_temp, units, 'Fraction Bound', normfits_x, normfits_y,
				normparam, title+' (Normalized)', color, marker_size, marker, line_width,
				line_style, plot_title_size, x_title_size, y_title_size, x_tick_label_size,
				y_tick_label_size, x_tick_size, y_tick_size, legend, png, svg, 
				plotname+str(plotcounter)+'_normalized', filepath, showplot)


def quad_allplot(conc, anisos, perplot, labels, units, y_title, ligands, fiteq, p0, normalization, 
	title, color, marker_size, marker, line_width, line_style, plot_title_size, x_title_size, 
	y_title_size, x_tick_label_size, y_tick_label_size, x_tick_size, y_tick_size, 
	legend, png, svg, plotname, filepath, showplot):
	#need to fix sqrt with normalization

	#the rest of this is to figure out how many plots to make based on the perplot in the config
	#plotcount gives the numer of plots minus one. leftovers gives the last one
	plotcount=int(len(anisos)/perplot)
	leftovers=int(len(anisos)%perplot)
	#masterindex counts up per sample plotted. plotcounter counts the plots so I can number the files.
	masterindex = 0
	plotcounter = 1
	p0_norm = [p0[0], 1.0, 0.0]
	for n in range(plotcount):#for each full plot to be made (no leftover plot)
		conc_temp = []
		anisos_temp = []
		ligands_temp = []
		labels_temp = []
		for i in range(perplot):#for each sample per plot, append lists with anisotropy and label of the sample based on masterindex
			conc_temp.append(conc[masterindex])
			anisos_temp.append(anisos[masterindex])
			ligands_temp.append(ligands[masterindex])
			labels_temp.append(labels[masterindex])
			masterindex+=1
		#fit and plot using the condensed sample list
		fits_x, fits_y, y_norm, param = getquadfit(conc_temp, anisos_temp, ligands_temp, fiteq, p0, units)
		logplot(conc_temp, anisos_temp, labels_temp, units, y_title, fits_x, fits_y,
			param, title, color, marker_size, marker, line_width, line_style, plot_title_size, 
			x_title_size, y_title_size, x_tick_label_size, y_tick_label_size, x_tick_size, y_tick_size, 
			legend, png, svg, plotname+str(plotcounter), filepath, showplot)
		if normalization == 1:
			normfits_x, normfits_y, _, normparam = getquadfit(conc_temp, y_norm, ligands_temp, fiteq, p0_norm, units)
			logplot(conc_temp, y_norm, labels_temp, units, 'Fraction Bound', normfits_x, normfits_y,
				normparam, title+' (Normalized)', color, marker_size, marker, line_width,
				line_style, plot_title_size, x_title_size, y_title_size, x_tick_label_size,
				y_tick_label_size, x_tick_size, y_tick_size,legend, png, svg, 
				plotname+str(plotcounter)+'_normalized', filepath, showplot)
		plotcounter+=1
	#deal with the rest of the samples if there are any leftovers. code is same as above.
	if leftovers>0:
		conc_temp = []
		anisos_temp = []
		ligands_temp = []
		labels_temp = []
		for n in range(leftovers):
			conc_temp.append(conc[masterindex])
			anisos_temp.append(anisos[masterindex])
			ligands_temp.append(ligands[masterindex])
			labels_temp.append(labels[masterindex])
			masterindex+=1
		fits_x, fits_y, y_norm, param = getquadfit(conc_temp, anisos_temp, ligands_temp, fiteq, p0, units)
		logplot(conc_temp, anisos_temp, labels_temp, units, y_title, fits_x, fits_y,
			param, title, color, marker_size, marker, line_width, line_style, 
			plot_title_size, x_title_size, y_title_size, x_tick_label_size,
			y_tick_label_size, x_tick_size, y_tick_size, legend, png, svg, 
			plotname+str(plotcounter), filepath, showplot)
		if normalization == 1:
			normfits_x, normfits_y, _, normparam = getquadfit(conc_temp, y_norm, ligands_temp, fiteq, p0_norm, units)
			logplot(conc_temp, y_norm, labels_temp, units, 'Fraction Bound', normfits_x, normfits_y,
				normparam, title+' (Normalized)', color, marker_size, marker, line_width,
				line_style, plot_title_size, x_title_size, y_title_size, x_tick_label_size,
				y_tick_label_size, x_tick_size, y_tick_size, legend, png, svg, 
				plotname+str(plotcounter)+'_normalized', filepath, showplot)