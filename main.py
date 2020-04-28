import configparse
import read
import plot

def run():
	raw_data = configparse.raw_data
	file_sheet = configparse.file_sheet
	a_or_p = configparse.a_or_p
	path_output = configparse.path_output
	plotname = configparse.plotname
	file_values= path_output+plotname+'_values.xls'
	rows = configparse.rows
	concentrations = configparse.concentrations
	dilution_factors = configparse.dilution_factors
	titrations = configparse.titrations
	samples = configparse.samples
	exclude = configparse.exclude
	units = configparse.units
	dupe = configparse.dupe
	labels = configparse.labels
	fiteq = configparse.fiteq
	conc_L = configparse.conc_L
	p0 = configparse.p0
	normalization = configparse.normalization
	perplot = configparse.perplot
	colors = configparse.colors
	marker_size = configparse.marker_size
	marker = configparse.marker
	line_width = configparse.line_width
	line_style = configparse.line_style
	plot_title_size = configparse.plot_title_size
	x_title_size = configparse.x_title_size
	y_title_size = configparse.y_title_size
	x_tick_label_size = configparse.x_tick_label_size
	y_tick_label_size = configparse.y_tick_label_size
	x_tick_size = configparse.x_tick_size
	y_tick_size = configparse.y_tick_size
	legend = configparse.legend
	png = configparse.png
	svg = configparse.svg
	plottitle = configparse.plottitle
	showplot = configparse.showplot

	for x in samples:
		if x == ['none'] or x == ['']:
			raise Exception('Must have sample numbers (check gui/config)')

	if raw_data == True:
		if a_or_p == 'anisotropy':
			y_title = "Anisotropy"
			#pick between a row layout or columns 
			if rows == False:
				parallel, perpendicular = read.excel_open_colsamples(file_sheet)
			else:
				parallel, perpendicular = read.excel_open_rowsamples(file_sheet)
			#calculate anisotropy and output to a formatted excel sheet
			conc_all, yvalues = read.format(parallel, perpendicular, concentrations, 
				dilution_factors, titrations, samples, dupe, exclude)
		elif a_or_p == 'polarization':
			y_title = "Polarization"
			#pick between a row layout or columns 
			if rows == False:
				polarization = read.polarization_colsamples(file_sheet)
			else:
				polarization = read.polarization_rowsamples(file_sheet)
			#output polarization to a formatted excel sheet
			conc_all, yvalues = read.polarization_format(polarization, concentrations, 
				dilution_factors, titrations, samples, dupe, exclude)
		while len(yvalues) > len(labels):
				if labels[0] == '':
					labels[0] = "No label"
				labels.append("No label")
		read.data_write(conc_all, yvalues, labels, file_values)
	else:
		if a_or_p == 'anisotropy':
			y_title = "Anisotropy"
		elif a_or_p == 'polarization':
			y_title = "Polarization"
		conc_all, yvalues, labels = read.data_read(file_sheet)
		while len(yvalues) > len(labels):
			if labels[0] == '':
				labels[0] = "No label"
			labels.append("No label")

	#fit data to simplified binding isotherm
	if fiteq == "kdfit":
		plot.allplot(conc_all,yvalues,perplot,labels,units,y_title,plot.kdfit,p0,normalization,
			plottitle,colors,marker_size,marker,line_width,line_style,plot_title_size,
			x_title_size,y_title_size,x_tick_label_size,y_tick_label_size,x_tick_size,
			y_tick_size,legend,png,svg,plotname,path_output,showplot)
	#quadratic fitting
	elif fiteq == "quad":
		plot.quad_allplot(conc_all,yvalues,perplot,labels,units,y_title,conc_L,plot.quad,p0,
			normalization,plottitle,colors,marker_size,marker,line_width,line_style,
			plot_title_size,x_title_size,y_title_size,x_tick_label_size,y_tick_label_size,
			x_tick_size,y_tick_size,legend,png,svg,plotname,path_output,showplot)

	print ("data is cool")

if __name__ == "__main__":
	run()