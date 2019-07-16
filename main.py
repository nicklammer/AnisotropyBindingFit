import configparse
import read
import plot

def run():
	raw_data = configparse.raw_data
	file_sheet = configparse.file_sheet
	path_output = configparse.path_output
	plotname = configparse.plotname
	file_anisotropy= path_output+plotname+'_anisotropy.xls'
	rows = configparse.rows
	concentrations = configparse.concentrations
	dilution_factors = configparse.dilution_factors
	titrations = configparse.titrations
	samples_temp = configparse.samples
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
	legend = configparse.legend
	png = configparse.png
	svg = configparse.svg
	plottitle = configparse.plottitle
	showplot = configparse.showplot
	#make sample list usable
	samples_split = []
	samples = []
	for x in samples_temp:
		samples_split.append(x.split(', '))
	for x in samples_split:
		samples.append([int(n) for n in x])

	if raw_data == True:
		#pick between a row layout or columns 
		if rows == False:
			parallel, perpendicular = read.excel_open_colsamples(file_sheet)
		else:
			parallel, perpendicular = read.excel_open_rowsamples(file_sheet)
		#calculate anisotropy and output in a formatted excel sheet
		conc_all, anisos = read.format(parallel, perpendicular, concentrations, dilution_factors, titrations, samples, dupe)
		while len(anisos) > len(labels):
				labels.append("No label")
		read.data_write(conc_all, anisos, labels, file_anisotropy)

	else:
		conc_all, anisos = read.data_read(file_sheet)

	#fit data to simplified binding isotherm
	if fiteq == "kdfit":
		plot.allplot(conc_all,anisos,perplot,labels,units,plot.kdfit,p0,normalization,
			plottitle,colors,marker_size,marker,line_width,line_style,legend,
			png,svg,plotname,path_output,showplot)
	#quadratic fitting
	elif fiteq == "quad":
		plot.quad_allplot(conc_all,anisos,perplot,labels,units,conc_L,plot.quad,p0,normalization,
			plottitle,colors,marker_size,marker,line_width,line_style,legend,
			png,svg,plotname,path_output,showplot)

	print ("data is cool")

if __name__ == "__main__":
	run()