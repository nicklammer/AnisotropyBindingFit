import config
import read
import plot

def run():
	file_raw = config.file_raw
	file_formatted = config.file_formatted
	rows = config.rows
	titrations = config.titrations
	start_col = config.start_col
	start_row = config.start_row
	concentration = config.concentration_start
	dilution_factor = config.dilution_factor
	units = config.units
	dupe = config.duplicates
	labels = config.labels
	fiteq = config.fiteq
	conc_L = float(config.conc_L)
	single = config.single
	sample = config.sample
	perplot = config.perplot
	color_single = config.color_single
	color_multiple = config.color_multiple
	marker = config.marker
	line_style = config.line_style
	plotname = config.plotname
	path_plot = config.path_plot
	normalization = config.normalization

	#pick between a row layout or columns 
	if rows == 0:
		FA = read.excel_open_colsamples(file_raw, titrations, start_row)
	elif rows == 1:
		FA = read.excel_open_rowsamples(file_raw, titrations, start_col)

	#read data excel file, calculate anisotropy, and output in a formatted excel sheet
	formatted = read.format(concentration, dilution_factor, dupe, FA)
	read.data_write(formatted, labels, file_formatted)
	#fit data to simplified binding isotherm
	if fiteq == "kdfit":
		if single == 0:
			plot.singleplot(formatted,sample,labels,units,plot.kdfit,normalization,
				color_multiple,marker,line_style,plotname,path_plot)
		elif single == 1:
			plot.multiplot(formatted,perplot,labels,units,plot.kdfit,normalization,
				color_multiple,marker,line_style,plotname,path_plot)

	elif fiteq == "quad":
		if single == 0:
			plot.quad_singleplot(formatted,sample,labels,units,conc_L,plot.quad,normalization,
				color_multiple,marker,line_style,plotname,path_plot)
		elif single == 1:
			plot.quad_multiplot(formatted,perplot,labels,units,conc_L,plot.quad,normalization,
				color_multiple,marker,line_style,plotname,path_plot)

	print ("data is cool")

if __name__ == "__main__":
	run()