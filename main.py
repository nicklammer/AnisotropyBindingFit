import configparse
import read
import plot

def run():
	file_raw = configparse.file_raw
	path_output = configparse.path_output
	file_anisotropy= path_output+'anisotropy.xls'
	rows = configparse.rows
	titrations = configparse.titrations
	start_col = configparse.start_col
	start_row = configparse.start_row
	concentration = configparse.concentration
	dilution_factor = configparse.dilution_factor
	units = configparse.units
	dupe = configparse.dupe
	single = configparse.single
	sample = configparse.sample
	labels = configparse.labels
	fiteq = configparse.fiteq
	conc_L = configparse.conc_L
	p0 = configparse.p0
	normalization = configparse.normalization
	perplot = configparse.perplot
	color_single = [configparse.color_single]
	color_multiple = configparse.color_multiple
	marker = configparse.marker
	line_style = configparse.line_style
	plotname = configparse.plotname

	if single in (0, 1):
		sample = [x-1 for x in sample]
	#pick between a row layout or columns 
	if rows == False:
		FA = read.excel_open_colsamples(file_raw, titrations, start_row)
	else:
		FA = read.excel_open_rowsamples(file_raw, titrations, start_col)

	#read data excel file, calculate anisotropy, and output in a formatted excel sheet
	formatted = read.format(concentration, dilution_factor, single, sample, dupe, FA)
	while len(formatted) > len(labels):
			labels.append("No label")
	read.data_write(formatted, labels, file_anisotropy)
	#fit data to simplified binding isotherm
	if fiteq == "kdfit":
		if single == 0:
			plot.singleplot(formatted,sample[0],labels,units,plot.kdfit,p0,normalization,
				color_single,marker,line_style,plotname,path_output)
		else:
			plot.multiplot(formatted,perplot,labels,units,plot.kdfit,p0,normalization,
				color_multiple,marker,line_style,plotname,path_output)
	#quadratic fitting
	elif fiteq == "quad":
		if single == 0:
			plot.quad_singleplot(formatted,sample,labels,units,conc_L,plot.quad,p0,normalization,
				color_multiple,marker,line_style,plotname,path_output)
		else:
			plot.quad_multiplot(formatted,perplot,labels,units,conc_L,plot.quad,p0,normalization,
				color_multiple,marker,line_style,plotname,path_output)

	print ("data is cool")

if __name__ == "__main__":
	run()