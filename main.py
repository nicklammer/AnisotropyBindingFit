def run():
	import configparse
	import read
	import plot
	import importlib
	importlib.reload(configparse)
	raw_data = configparse.raw_data
	file_sheet = configparse.file_sheet
	a_or_p = configparse.a_or_p
	path_output = configparse.path_output
	plotname = configparse.plotname
	file_values= path_output+plotname+'_values.xlsx'
	concentrations = configparse.concentrations
	dilution_factors = configparse.dilution_factors
	titrations = configparse.titrations
	rc=configparse.rc
	wells = configparse.wells
	ligands=configparse.ligand_conc
	exclude = configparse.exclude
	units = configparse.units
	dupe = configparse.dupe
	labels = configparse.labels
	fiteq = configparse.fiteq
	p0 = configparse.p0
	L_pre = configparse.L_pre
	normalization = configparse.normalization
	perplot = configparse.perplot
	colors = configparse.colors
	marker_size = configparse.marker_size
	marker_style = configparse.markers
	line_width = configparse.line_width
	line_style = configparse.lines
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
	if raw_data == True:
		if a_or_p == 'anisotropy':
			y_title = "Anisotropy"
			#get parallel and perpendicular data from excel sheet
			parallel,perpendicular=read.excel_open_aniso(file_sheet,rc,wells)
			#calculate anisotropy and clean up lists to be lists of lists
			conc_all, yvalues, ligand_clean, labels_clean = read.format_aniso(parallel, perpendicular, concentrations, 
				dilution_factors, titrations, ligands, labels, dupe, exclude)
		elif a_or_p == 'polarization':
			y_title = "Polarization"
			#get polarization data from excel sheet
			polarization = read.excel_open_polar(file_sheet,rc,wells)
			#clean up lists to be lists of lists
			conc_all, yvalues, ligand_clean, labels_clean = read.format_polar(polarization, concentrations, 
				dilution_factors, titrations, ligands, labels, dupe, exclude)
		read.data_write(conc_all, yvalues, labels_clean, file_values)
	else:
		if a_or_p == 'anisotropy':
			y_title = "Anisotropy"
		elif a_or_p == 'polarization':
			y_title = "Polarization"
		conc_all, yvalues, labels_clean = read.data_read(file_sheet)
		ligand_clean = L_pre
		while len(yvalues) > len(labels_clean):
			if labels_clean[0] == '':
				labels_clean[0] = "No label"
			labels_clean.append("No label")

	#fit data to simplified binding isotherm
	if fiteq == "kdfit" or fiteq == "hill":
		p0=p0[0:3]
		plot.allplot(conc_all,yvalues,perplot,labels_clean,units,y_title,fiteq,p0,normalization,
			plottitle,colors,marker_size,marker_style,line_width,line_style,plot_title_size,
			x_title_size,y_title_size,x_tick_label_size,y_tick_label_size,x_tick_size,
			y_tick_size,legend,png,svg,plotname,path_output,showplot)
	#quadratic fitting
	elif fiteq == "quad":
		p0=p0[0:3]
		plot.quad_allplot(conc_all,yvalues,perplot,labels_clean,units,y_title,ligand_clean,fiteq,p0,
			normalization,plottitle,colors,marker_size,marker_style,line_width,line_style,
			plot_title_size,x_title_size,y_title_size,x_tick_label_size,y_tick_label_size,
			x_tick_size,y_tick_size,legend,png,svg,plotname,path_output,showplot)
	#multi-site fitting
	elif fiteq == "multi":
		plot.allplot(conc_all,yvalues,perplot,labels_clean,units,y_title,fiteq,p0,normalization,
			plottitle,colors,marker_size,marker_style,line_width,line_style,plot_title_size,
			x_title_size,y_title_size,x_tick_label_size,y_tick_label_size,x_tick_size,
			y_tick_size,legend,png,svg,plotname,path_output,showplot)
	print ("data is cool")

if __name__ == "__main__":
	run()