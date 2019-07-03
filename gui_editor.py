from Tkinter import *
from ttk import *
import tkFileDialog
import configparse
import os
from ConfigParser import SafeConfigParser

#import the current config
file_raw = configparse.file_raw
path_output = configparse.path_output
rows = configparse.rows
titrations = configparse.titrations
start_col = configparse.start_col
start_row = configparse.start_row
concentration = configparse.concentration
dilution_factor = configparse.dilution_factor
units = configparse.units
dupe = configparse.dupe
single = configparse.single
sample = configparse.sample_temp
labels = configparse.labels
fiteq = configparse.fiteq
conc_L = configparse.conc_L
p0 = configparse.p0
normalization = configparse.normalization
perplot = configparse.perplot
color_single = configparse.color_single_key
color_multiple = configparse.color_multiple_key_temp
marker = configparse.marker_chosen
line_style = configparse.line_chosen
plottitle = configparse.plottitle
plotname = configparse.plotname
colors_key = configparse.colors_key
marker_key = configparse.marker_key
line_key = configparse.line_key

root = Tk()
def exit_client():
	exit()
def browse_sheet():
	global sheet_path
	filename = tkFileDialog.askopenfilename(title="Select data sheet", filetypes=(("Excel sheets","*.xlsx *.xls"),("All files", "*.*")))
	sheet_path.set(filename)
def browse_dir():
	global folder_path
	dirname = tkFileDialog.askdirectory()
	folder_path.set(dirname+'/')
def rc_rows():
	start_col_box.config(state='enabled')
	start_row_box.config(state='disabled')
def rc_cols():
	start_col_box.config(state='disabled')
	start_row_box.config(state='enabled')
def sample_single():
	sample_box.config(state='enabled')
	color_single_dd.config(state='enabled')
	perplot_box.config(state='disabled')
	color_multiple_dd.config(state='disabled')
	color_multiple_box.config(state='disabled')
def sample_multiple():
	sample_box.config(state='enabled')
	color_single_dd.config(state='disabled')
	perplot_box.config(state='enabled')
	color_multiple_dd.config(state='enabled')
	color_multiple_box.config(state='normal')
def sample_all():
	sample_box.config(state='disabled')
	color_single_dd.config(state='disabled')
	perplot_box.config(state='enabled')
	color_multiple_dd.config(state='enabled')
	color_multiple_box.config(state='normal')
def addcolor(event):
	color_multiple_box.insert('end', color_multiple_dd.get()+', ')

root.title("FA plotting configuration")
root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(0, weight=1)
nb = Notebook(root)
nb.grid(row=0, column=0, columnspan=2, sticky='nsew')
tab1 = Frame(nb)
tab2 = Frame(nb)
nb.add(tab1, text="Data layout")
nb.add(tab2, text="Plot and fit")
nb.enable_traversal()

tab1.grid_columnconfigure(1, weight=1)

#file path entries
Label(tab1, text="Data sheet").grid(row=0, sticky='w', padx=10)
sheet_path = StringVar()
sheet_path.set(file_raw)
data_box = Entry(tab1, textvariable=sheet_path)
data_box.grid(row=0, column=1, sticky='ew')
data_browse = Button(tab1, text="Browse", command=browse_sheet)
data_browse.grid(row=0, column=2, sticky='w')

Label(tab1, text="Output folder").grid(row=1, sticky='w', padx=10)
folder_path = StringVar()
folder_path.set(path_output)
output_box = Entry(tab1, textvariable=folder_path)
output_box.grid(row=1, column=1, sticky='ew')
output_browse = Button(tab1, text="Browse", command=browse_dir)
output_browse.grid(row=1, column=2, sticky='w')
#Titration info
Label(tab1, text="Titrations done per row or column?").grid(row=3)
rc_choice = BooleanVar()
rc_choice.set(rows)
row = Radiobutton(tab1, text="Row", variable=rc_choice, value=True, command=rc_rows)
column = Radiobutton(tab1, text="Column", variable=rc_choice, value=False, command=rc_cols)
row.grid(row=4)
column.grid(row=4, column=1, sticky='w')

Label(tab1, text="Number of titrations and starting column or row:").grid(row=5)
Label(tab1, text="Titrations:").grid(row=6)
titrations_box = Entry(tab1)
titrations_box.grid(row=6, column=1, sticky='w', pady=2)
titrations_box.insert('end', titrations)
Label(tab1, text="Starting column:").grid(row=7)
start_col_box = Entry(tab1)
start_col_box.grid(row=7, column=1, sticky='w', pady=2)
start_col_box.insert('end', start_col)
if rows == False:
	start_col_box.config(state='disabled')
Label(tab1, text="Starting row:").grid(row=8)
start_row_box = Entry(tab1)
start_row_box.grid(row=8, column=1, sticky='w', pady=2)
start_row_box.insert('end', start_row)
if rows == True:
	start_row_box.config(state='disabled')

Label(tab1, text="Maximum protein concentration, dilution factor, and units:").grid(row=9)
Label(tab1, text="Max concentration:").grid(row=10)
max_conc_box = Entry(tab1)
max_conc_box.grid(row=10, column=1, sticky='w', pady=2)
max_conc_box.insert('end', concentration)
Label(tab1, text="Dilution factor (if 1:2 dilutions, would enter 2):").grid(row=11)
dilution_box = Entry(tab1)
dilution_box.grid(row=11, column=1, sticky='w', pady=2)
dilution_box.insert('end', dilution_factor)
Label(tab1, text="Units:").grid(row=12)
units_box = Entry(tab1)
units_box.grid(row=12, column=1, sticky='w', pady=2)
units_box.insert('end', units)

Label(tab1, text="Single sample or multiple?").grid(row=13)
sample_number_choice = IntVar()
sample_number_choice.set(single)
single_button = Radiobutton(tab1, text="Single", variable=sample_number_choice, value=0, command=sample_single)
multiple_button = Radiobutton(tab1, text="Multiple", variable=sample_number_choice, value=1, command=sample_multiple)
all_button = Radiobutton(tab1, text="All", variable=sample_number_choice, value=2, command=sample_all)
single_button.grid(row=14)
multiple_button.grid(row=14, column=1, sticky='w')
all_button.grid(row=14, column=1)
Label(tab1, text="If single or multiple, which sample(s)?\n(Number of the sample(s) in order)").grid(row=15)
sample_box = Entry(tab1)
sample_box.grid(row=15, column=1, sticky='w', pady=2)
sample_box.insert('end', sample)
if single == 2:
	sample_box.config(state='disabled')

Label(tab1, text="Sample labels\n(Enter names in order separated by a comma and space)").grid(row=16)
label_box = Text(tab1, height=2, width=40, borderwidth=2)
label_box.grid(row=16, column=1, sticky='w', pady=5)
label_box.insert('end', ", ".join(labels))
duplicate = BooleanVar()
duplicate.set(dupe)
duplicate_check = Checkbutton(tab1, text="Samples done in duplicate", 
	variable=duplicate, onvalue=True, offvalue=False)
duplicate_check.grid(row=17)

#Plotting and fitting options
Label(tab2, text="Choose type of fit:").grid(row=0)
fiteq_value = StringVar()
fiteq_value.set(fiteq)
kdfit = Radiobutton(tab2, text="Simple Kd Fit", variable=fiteq_value, value="kdfit")
quad = Radiobutton(tab2, text="Quadratic", variable=fiteq_value, value="quad")
kdfit.grid(row=1, sticky='w')
quad.grid(row=2, sticky='w')

Label(tab2, text="Concentration of ligand (quad fit):").grid(row=3)
conc_L_box = Entry(tab2)
conc_L_box.grid(row=3, column=1)
conc_L_box.insert('end', conc_L)

Label(tab2, text="Initial parameters:").grid(row=4, pady=2)
Label(tab2, text="Kd:").grid(row=5, pady=2)
kd_box = Entry(tab2)
kd_box.grid(row=5, column=1)
kd_box.insert('end', p0[0])
Label(tab2, text="S:").grid(row=6, pady=2)
s_box = Entry(tab2)
s_box.grid(row=6, column=1)
s_box.insert('end', p0[1])
Label(tab2, text="O:").grid(row=7, pady=2)
o_box = Entry(tab2)
o_box.grid(row=7, column=1)
o_box.insert('end', p0[2])
normalization_value = BooleanVar()
normalization_value.set(normalization)
normalization_check = Checkbutton(tab2, text="Plot fraction bound normalization", 
	variable=normalization_value, onvalue=True, offvalue=False).grid(row=8)

Label(tab2, text="Plot options").grid(row=0, column=2, pady=4)
Label(tab2, text="Number of samples per plot").grid(row=1, column=2, pady=2)
perplot_box = Entry(tab2)
perplot_box.grid(row=1, column=3)
perplot_box.insert('end', perplot)
if single == 0:
	perplot_box.config(state='disabled')

Label(tab2, text="Color for single sample").grid(row=2, column=2)
color_single_dd = Combobox(tab2, values=colors_key)
color_single_dd.grid(row=2, column=3)
color_single_dd.insert('end', color_single)
if single in (1, 2):
	color_single_dd.config(state='disabled')

Label(tab2, text="Colors for multiple samples").grid(row=3, column=2)
color_multiple_dd = Combobox(tab2, values=colors_key)
color_multiple_dd.grid(row=3, column=3)
color_multiple_dd.bind("<<ComboboxSelected>>", addcolor)
color_multiple_box = Text(tab2, height=2, width=40, borderwidth=2)
color_multiple_box.grid(row=4, column=2, columnspan=2, padx=20, pady=3)
color_multiple_box.insert('end', color_multiple)
if single == 0:
	color_multiple_dd.config(state='disabled')
	color_multiple_box.config(state='disabled')

Label(tab2, text="Marker style:").grid(row=5, column=2)
marker_dd = Combobox(tab2, values=marker_key)
marker_dd.grid(row=5, column=3)
marker_dd.insert('end', marker)
Label(tab2, text="Line style:").grid(row=6, column=2)
line_dd = Combobox(tab2, values=line_key)
line_dd.grid(row=6, column=3)
line_dd.insert('end', line_style)

Label(tab2, text="Plot title (for each plot):").grid(row=7, column=2)
title_box = Entry(tab2)
title_box.grid(row=7, column=3)
title_box.insert('end', plottitle)

Label(tab2, text="File name for the plots:").grid(row=8, column=2)
plotname_box = Entry(tab2)
plotname_box.grid(row=8, column=3)
plotname_box.insert('end', plotname)

#function for writing everything to the config.ini
dir_path = os.path.dirname(os.path.realpath(__file__))
config_path = os.path.join(dir_path, 'config.ini')
parser = SafeConfigParser()
parser.read(config_path)
def config_set(section, option, value):
	parser.set(section, option, value)
def config_write(file):
	configfile = open(file, 'w')
	parser.write(configfile)
def save_everything():
	config_set('file options', 'file raw', data_box.get())
	config_set('file options', 'output folder', output_box.get())
	config_set('sample layout', 'rows', str(rc_choice.get()))
	config_set('sample layout', 'titrations', titrations_box.get())
	config_set('sample layout', 'starting column', start_col_box.get())
	config_set('sample layout', 'starting row', start_row_box.get())
	config_set('sample layout', 'max concentration', max_conc_box.get())
	config_set('sample layout', 'dilution factor', dilution_box.get())
	config_set('sample layout', 'units', units_box.get())
	config_set('sample layout', 'duplicates', str(duplicate.get()))
	config_set('sample layout', 'single', str(sample_number_choice.get()))
	config_set('sample layout', 'sample', sample_box.get())
	config_set('sample layout', 'labels', label_box.get('1.0', 'end').replace('%','%%'))
	config_set('fit options', 'fiteq', fiteq_value.get())
	config_set('fit options', 'ligand concentration', conc_L_box.get())
	config_set('fit options', 'Kdi', kd_box.get())
	config_set('fit options', 'Si', s_box.get())
	config_set('fit options', 'Oi', o_box.get())
	config_set('fit options', 'normalization', str(normalization_value.get()))
	config_set('plot options', 'per plot', perplot_box.get())
	config_set('plot options', 'color single', color_single_dd.get())
	config_set('plot options', 'color multiple', color_multiple_box.get('1.0', 'end'))
	config_set('plot options', 'marker style', marker_dd.get())
	config_set('plot options', 'line style', line_dd.get())
	config_set('plot options', 'plot title', title_box.get().replace('%', '%%'))
	config_set('plot options', 'plot name', plotname_box.get().replace('%', '%%'))

	config_write(config_path)
	print("Saved")
# def save_and_plot():
# 	save_everything()


savebutton = Button(root, text="Save", command=save_everything)
savebutton.grid(row=1, column=0, padx=5, pady=5, sticky='e')
# saveandplotbutton = Button(root, text="Save and plot", command=save_and_plot)
# saveandplotbutton.grid(row=1, column=1, padx=5, pady=5, sticky='e')
exitbutton = Button(root, text="Exit", command=exit_client)
exitbutton.grid(row=1, column=2, padx=5, pady=5, sticky='w')

root.mainloop()
