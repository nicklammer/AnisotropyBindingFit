#config for fluorescence anisotropy anaylsis script

#file paths for the raw data (microplate layout) and the paths for the output excel sheet and plots
file_raw = "../FA_data/test4.xlsx"
file_formatted = "../FA_data/anisotropy.xls"
path_plot = "../FA_data/"

#sample layout info
#are titrations done per row or column? 1 for rows, 0 for columns
rows = 1
#how many titrations are there?
titrations = 20
#column or row that titrations start on (start_col if your samples were done by row)
start_col = 1
start_row = 1


#starting 1X concentration for protein and the dilution factor
#this script assumes each titration between samples are the same concentration. if not, try using the single plotting for each
concentration_start = 40000
dilution_factor = 2
units = "nM"

#if you have duplicates, value is 1. If not, value is 0
duplicates = 1

#plot a single sample or multiple. 0 for single, 1 for multiple
single = 0

#if single, which sample? express as a number starting from 0 based on the order on the plate
sample = 2

#labels for data in order of rows (A-P)
labels = ["cGR DNA","R1K2 DNA","K2K5 DNA","R1K2K5 DNA",
	"cGR RNA","R1K2 RNA","K2K5 RNA","R1K2K5 RNA",
	]

#equation for fit. kdfit or quad for now
fiteq = "kdfit"

#plot options
perplot = 4
color_single = 'black'
color_multiple = ['blue','green','turquoise','red','magenta','orange', 'yellowgreen', 'xkcd:lavender']
#find a table with color names here matplotlib.org/users/colors.html
marker = 'o'
line_style = '--'
plotname = 'boop_'

#do you also want normalized fraction bound plots? (0 for no, 1 for yes)
normalization = 1