from Tkinter import *
from ttk import *
import tkFileDialog
import configparse
import os
from ConfigParser import SafeConfigParser

#import style keys from plot_style.ini through configparse
colors_key = configparse.colors_key_fordict
marker_key = configparse.marker_key
line_key = configparse.line_key

root = Tk()
#functions for buttons
def exit_client():
	exit()
def browse_config():
	global config_load_box_path
	global parser
	filename = tkFileDialog.askopenfilename(title="Select config.ini to load", 
		filetypes=(("INI files","*.ini"),("All files", "*.*")))
	config_load_box_path.set(filename)
	print("Config changed to "+filename)
	parser.read(filename)
	fill_values()
	default_disable()
	default_enable()
def browse_sheet():
	global sheet_path
	filename = tkFileDialog.askopenfilename(title="Select data sheet", 
		filetypes=(("Excel sheets","*.xlsx *.xls"),("All files", "*.*")))
	sheet_path.set(filename)
def browse_dir():
	global folder_path
	dirname = tkFileDialog.askdirectory()
	folder_path.set(dirname+'/')
def raw_data_true():
	row.config(state='enabled')
	column.config(state='enabled')
	titrations_box.config(state='enabled')
	max_conc_box.config(state='enabled')
	dilution_box.config(state='enabled')
	duplicate_check.config(state='enabled')
def raw_data_false():
	row.config(state='disabled')
	column.config(state='disabled')
	titrations_box.config(state='disabled')
	max_conc_box.config(state='disabled')
	dilution_box.config(state='disabled')
	duplicate_check.config(state='disabled')
def addcolor(event):
	color_box.insert('end', color_dd.get()+', ')

#set all the vars to be used
raw_data = BooleanVar()
sheet_path = StringVar()
folder_path = StringVar()
rc_choice = BooleanVar()
duplicate = BooleanVar()
fiteq_value = StringVar()
normalization_value = BooleanVar()
legend = BooleanVar()
png = BooleanVar()
svg = BooleanVar()
showplot = BooleanVar()


root.title("FA plotting configuration")

root.grid_columnconfigure(1, weight=1)
root.grid_rowconfigure(1, weight=1)

#loading config files
dir_path = os.path.dirname(os.path.realpath(__file__))
config_path = os.path.join(dir_path, 'config.ini')
parser = SafeConfigParser()
parser.read(config_path)

config_frame = Frame(root)
config_frame.grid(row=0, column=0, columnspan=2, pady=3, sticky='nsew')
config_frame.grid_columnconfigure(1, weight=1)
Label(config_frame, text="Load config file").grid(row=0, padx=2, pady=3, sticky='nw')
config_load_box_path = StringVar()
config_load_box_path.set(config_path)
config_load_box = Entry(config_frame, textvariable=config_load_box_path)
config_load_box.grid(row=0, column=1, padx=3, pady=2, sticky='new')
config_load_button = Button(config_frame, text="Browse", command=browse_config)
config_load_button.grid(row=0, column=2, sticky='nw')


nb = Notebook(root)
nb.grid(row=1, column=0, columnspan=2, sticky='nsew')
tab1 = Frame(nb)
tab_data = Frame(nb)
tab2 = Frame(nb)
nb.add(tab1, text="Data")
nb.add(tab_data, text="Data cont.")
nb.add(tab2, text="Plot and fit")
nb.enable_traversal()

tab1.grid_columnconfigure(1, weight=1)

#file path entries
Label(tab1, text="Data sheet").grid(row=0, sticky='w', padx=10)
data_box = Entry(tab1, textvariable=sheet_path)
data_box.grid(row=0, column=1, sticky='ew')
data_browse = Button(tab1, text="Browse", command=browse_sheet)
data_browse.grid(row=0, column=2, sticky='w')

Label(tab1, text="Raw data or pre-formatted?").grid(row=1)
raw = Radiobutton(tab1, text="Raw", variable=raw_data, value=True, command=raw_data_true)
formatted = Radiobutton(tab1, text="Pre-formatted", variable=raw_data, value=False, command=raw_data_false)
raw.grid(row=2)
formatted.grid(row=2, column=1, sticky='w')

Label(tab1, text="Output folder").grid(row=3, sticky='w', padx=10)
output_box = Entry(tab1, textvariable=folder_path)
output_box.grid(row=3, column=1, sticky='ew')
output_browse = Button(tab1, text="Browse", command=browse_dir)
output_browse.grid(row=3, column=2, sticky='w')

#Titration info
Label(tab1, text="Titrations done per row or column?").grid(row=4)
row = Radiobutton(tab1, text="Row", variable=rc_choice, value=True)
column = Radiobutton(tab1, text="Column", variable=rc_choice, value=False)
row.grid(row=5)
column.grid(row=5, column=1, sticky='w')

Label(tab1, text="Units:").grid(row=13)
units_box = Entry(tab1)
units_box.grid(row=13, column=1, sticky='w', pady=2)

Label(tab1, text="Sample labels\n(Enter names in order separated by a comma and space)").grid(row=17)
label_box = Text(tab1, height=2, width=40, borderwidth=2)
label_box.grid(row=17, column=1, sticky='w', pady=5)
duplicate_check = Checkbutton(tab1, text="Samples done in duplicate", 
	variable=duplicate, onvalue=True, offvalue=False)
duplicate_check.grid(row=18)

#actual data layout
Label(tab_data, text="Number of unique\nprotein dilutions").grid(row=0, column=0, padx=3, pady=5)
unique_dilutions = Entry(tab_data, justify='center')
unique_dilutions.grid(row=0, column=1)
Label(tab_data, text="Starting\nconcentration", justify='center').grid(row=1, column=0)
Label(tab_data, text="Dilution factor\n(1:2 is 2)", justify='center').grid(row=1, column=1)
Label(tab_data, text="# of titrations", justify='center').grid(row=1, column=2)
Label(tab_data, text="Starting row/column", justify='center').grid(row=1, column=3)
Label(tab_data, text="Sample numbers", justify='center').grid(row=1, column=4)
conc_boxes = []
dilution_boxes = []
titration_boxes = []
sample_boxes = []
def update_boxes():
	#this is ugly, but it works
	global unique_dilutions
	global conc_boxes
	global dilution_boxes
	global titration_boxes
	global sample_boxes
	holder1 = []
	holder2 = []
	holder3 = []
	holder5 = []
	for i in range(len(conc_boxes)):
		holder1.append(conc_boxes[i].get())
		holder2.append(dilution_boxes[i].get())
		holder3.append(titration_boxes[i].get())
		holder5.append(sample_boxes[i].get())
		conc_boxes[i].grid_forget()
		dilution_boxes[i].grid_forget()
		titration_boxes[i].grid_forget()
		sample_boxes[i].grid_forget()
	conc_boxes = []
	dilution_boxes = []
	titration_boxes = []
	sample_boxes = []
	while len(holder1) < int(unique_dilutions.get()):
		holder1.append('')
		holder2.append('')
		holder3.append('')
		holder5.append('')
	for n in range(int(unique_dilutions.get())):
		conc_boxes.append(Entry(tab_data, justify='center', width=8))
		conc_boxes[n].grid(row=n+2, column=0, pady=2)
		dilution_boxes.append(Entry(tab_data, justify='center', width=7))
		dilution_boxes[n].grid(row=n+2, column=1, pady=2)
		titration_boxes.append(Entry(tab_data, justify='center', width=7))
		titration_boxes[n].grid(row=n+2, column=2, pady=2)
		sample_boxes.append(Entry(tab_data, justify='center'))
		sample_boxes[n].grid(row=n+2, column=4, pady=2)
		conc_boxes[n].insert('end', holder1[n])
		dilution_boxes[n].insert('end', holder2[n])
		titration_boxes[n].insert('end', holder3[n])
		sample_boxes[n].insert('end', holder5[n])
updatebutton = Button(tab_data, text="Update boxes", command=update_boxes)
updatebutton.grid(row=0, column=2, padx=5, pady=5)

#Plotting and fitting options
Label(tab2, text="Choose type of fit:").grid(row=0)
kdfit = Radiobutton(tab2, text="Simple Kd Fit", variable=fiteq_value, value="kdfit")
quad = Radiobutton(tab2, text="Quadratic", variable=fiteq_value, value="quad")
kdfit.grid(row=1, sticky='w')
quad.grid(row=2, sticky='w')

Label(tab2, text="Concentration of ligand (quad fit):").grid(row=3)
conc_L_box = Entry(tab2)
conc_L_box.grid(row=3, column=1)

Label(tab2, text="Initial parameters:").grid(row=4, pady=2)
Label(tab2, text="Kd:").grid(row=5, pady=2)
kd_box = Entry(tab2)
kd_box.grid(row=5, column=1)
Label(tab2, text="S:").grid(row=6, pady=2)
s_box = Entry(tab2)
s_box.grid(row=6, column=1)
Label(tab2, text="O:").grid(row=7, pady=2)
o_box = Entry(tab2)
o_box.grid(row=7, column=1)
normalization_check = Checkbutton(tab2, text="Plot fraction bound normalization", 
	variable=normalization_value, onvalue=True, offvalue=False).grid(row=8)

Label(tab2, text="Plot options").grid(row=0, column=2, pady=4)
Label(tab2, text="Number of samples per plot:\n(Maximum of 6 or you can't read the table)").grid(row=1, column=2, pady=2)
perplot_box = Entry(tab2)
perplot_box.grid(row=1, column=3)

Label(tab2, text="Colors for samples (in plotted order)").grid(row=3, column=2)
color_dd = Combobox(tab2, values=colors_key)
color_dd.grid(row=3, column=3, pady=3)
color_dd.bind("<<ComboboxSelected>>", addcolor)
color_box = Text(tab2, height=2, width=40, borderwidth=2)
color_box.grid(row=4, column=2, columnspan=2, padx=20, pady=3)

Label(tab2, text="Marker style:").grid(row=5, column=2)
marker_dd = Combobox(tab2, values=marker_key)
marker_dd.grid(row=5, column=3, pady=2)

Label(tab2, text="Marker size:").grid(row=6, column=2)
marker_size_box = Entry(tab2)
marker_size_box.grid(row=6, column=3, pady=2)

Label(tab2, text="Line style:").grid(row=7, column=2)
line_dd = Combobox(tab2, values=line_key)
line_dd.grid(row=7, column=3, pady=2)

Label(tab2, text="Line width:").grid(row=8, column=2)
line_width_box = Entry(tab2)
line_width_box.grid(row=8, column=3, pady=2)

legend_check = Checkbutton(tab2, text="Show legend", 
	variable=legend, onvalue=True, offvalue=False)
legend_check.grid(row=9, column=2, columnspan=2)

png_check = Checkbutton(tab2, text="Save .png files", 
	variable=png, onvalue=True, offvalue=False)
png_check.grid(row=10, column=2, columnspan=2)

svg_check = Checkbutton(tab2, text="Save .svg files", 
	variable=svg, onvalue=True, offvalue=False)
svg_check.grid(row=11, column=2, columnspan=2)

Label(tab2, text="Plot title (for each plot):").grid(row=12, column=2)
title_box = Entry(tab2)
title_box.grid(row=12, column=3, pady=2)

Label(tab2, text="File name for the plots:").grid(row=13, column=2)
plotname_box = Entry(tab2)
plotname_box.grid(row=13, column=3, pady=2)

show_check = Checkbutton(tab2, text="Show plots in a window", 
	variable=showplot, onvalue=True, offvalue=False)
show_check.grid(row=14, column=2, columnspan=2)

#function for setting all values after loading a config file
def value_set(thing, value):#for setting vars
	thing.set(value)
def value_insert(box, value):#for entry widgets
	box.delete(0, 'end')
	box.insert('end', value)
def value_text_insert(box, value):#for text widgets
	box.delete('1.0', 'end')
	box.insert('end', value)
def fill_values():
	value_set(raw_data, parser.getboolean('file options', 'raw data'))
	value_set(sheet_path, parser.get('file options', 'sheet file'))
	value_set(folder_path, parser.get('file options', 'output folder'))
	value_set(rc_choice, parser.getboolean('sample layout', 'rows'))
	value_insert(units_box, parser.get('sample layout', 'units'))
	value_text_insert(label_box, parser.get('sample layout', 'labels'))
	value_insert(unique_dilutions, parser.get('sample layout', 'unique dilutions'))
	holder1 = parser.get('sample layout', 'concentrations').split(', ')
	holder2 = parser.get('sample layout', 'dilution factors').split(', ')
	holder3 = parser.get('sample layout', 'titrations').split(', ')
	holder5 = parser.get('sample layout', 'samples').split(': ')
	while len(holder1) < int(unique_dilutions.get()):
		holder1.append('')
	while len(holder2) < int(unique_dilutions.get()):
		holder2.append('')
	while len(holder3) < int(unique_dilutions.get()):
		holder3.append('')
	while len(holder5) < int(unique_dilutions.get()):
		holder5.append('')
	update_boxes()
	for n in range(int(unique_dilutions.get())):
		value_insert(conc_boxes[n], holder1[n])
		value_insert(dilution_boxes[n], holder2[n])
		value_insert(titration_boxes[n], holder3[n])
		value_insert(sample_boxes[n], holder5[n])
	value_set(duplicate, parser.getboolean('sample layout', 'duplicates'))
	value_set(fiteq_value, parser.get('fit options', 'fiteq'))
	value_insert(conc_L_box, parser.getfloat('fit options', 'ligand concentration'))
	value_insert(kd_box, parser.getfloat('fit options', 'Kdi'))
	value_insert(s_box, parser.getfloat('fit options', 'Si'))
	value_insert(o_box, parser.getfloat('fit options', 'Oi'))
	value_set(normalization_value, parser.getboolean('fit options', 'normalization'))
	value_insert(perplot_box, parser.getint('plot options', 'per plot'))
	value_text_insert(color_box, parser.get('plot options', 'colors').strip(", "))
	value_insert(marker_dd, parser.get('plot options', 'marker style'))
	value_insert(marker_size_box, parser.get('plot options', 'marker size'))
	value_insert(line_dd, parser.get('plot options', 'line style'))
	value_insert(line_width_box, parser.get('plot options', 'line width'))
	value_set(legend, parser.getboolean('plot options', 'legend'))
	value_set(png, parser.getboolean('plot options', 'png'))
	value_set(svg, parser.getboolean('plot options', 'svg'))
	value_insert(title_box, parser.get('plot options', 'plot title'))
	value_insert(plotname_box, parser.get('plot options', 'plot name'))
	value_set(showplot, parser.getboolean('plot options', 'show plot'))

def default_disable():
	if raw_data.get() == False:
		row.config(state='disabled')
		column.config(state='disabled')
		titrations_box.config(state='disabled')
		max_conc_box.config(state='disabled')
		dilution_box.config(state='disabled')
		duplicate_check.config(state='disabled')
def default_enable():
	if raw_data.get() == True:
		duplicate_check.config(state='enabled')

fill_values()#fill in all the boxes
default_disable()#start boxes disabled based on filled values

#function for writing everything to the config.ini
def config_set(section, option, value):
	parser.set(section, option, value)
def config_write(file):
	configfile = open(file, 'w')
	parser.write(configfile)
def save_everything():
	config_set('file options', 'raw data', str(raw_data.get()))
	config_set('file options', 'sheet file', data_box.get())
	config_set('file options', 'output folder', output_box.get())
	config_set('sample layout', 'rows', str(rc_choice.get()))
	holder1 = []
	holder2 = []
	holder3 = []
	holder5 = []
	for i in range(len(conc_boxes)):
		holder1.append(conc_boxes[i].get())
		holder2.append(dilution_boxes[i].get())
		holder3.append(titration_boxes[i].get())
		holder5.append(sample_boxes[i].get())
	config_set('sample layout', 'unique dilutions', unique_dilutions.get())
	config_set('sample layout', 'concentrations', ', '.join(holder1))
	config_set('sample layout', 'dilution factors', ', '.join(holder2))
	config_set('sample layout', 'titrations', ', '.join(holder3))
	config_set('sample layout', 'samples', ': '.join(holder5))
	config_set('sample layout', 'units', units_box.get())
	config_set('sample layout', 'duplicates', str(duplicate.get()))
	config_set('sample layout', 'labels', label_box.get('1.0', 'end').replace('%','%%').strip('\n'))
	config_set('fit options', 'fiteq', fiteq_value.get())
	config_set('fit options', 'ligand concentration', conc_L_box.get())
	config_set('fit options', 'Kdi', kd_box.get())
	config_set('fit options', 'Si', s_box.get())
	config_set('fit options', 'Oi', o_box.get())
	config_set('fit options', 'normalization', str(normalization_value.get()))
	config_set('plot options', 'per plot', perplot_box.get())
	config_set('plot options', 'colors', color_box.get('1.0', 'end').strip('\n'))
	config_set('plot options', 'marker style', marker_dd.get())
	config_set('plot options', 'marker size', marker_size_box.get())
	config_set('plot options', 'line style', line_dd.get())
	config_set('plot options', 'line width', line_width_box.get())
	config_set('plot options', 'legend', str(legend.get()))
	config_set('plot options', 'png', str(png.get()))
	config_set('plot options', 'svg', str(svg.get()))
	config_set('plot options', 'plot title', title_box.get().replace('%', '%%'))
	config_set('plot options', 'plot name', plotname_box.get().replace('%', '%%'))
	config_set('plot options', 'show plot', str(showplot.get()))

	config_write(config_path)
	config_write(config_load_box_path.get())
	print("Saved")
def save_config():
	savedir = tkFileDialog.asksaveasfilename(title="Save config as", defaultextension='.ini',
		filetypes=((".ini files","*.ini"),("All files", "*.*")))
	save_everything()
	config_write(savedir)

button_frame = Frame(root)
button_frame.grid(row=3, column=1)
button_frame.grid_columnconfigure(0, weight=1)
savebutton = Button(button_frame, text="Save", command=save_everything)
savebutton.grid(row=3, column=0, padx=5, pady=5, sticky='w')
saveconfigbutton = Button(button_frame, text="Save as", command=save_config)
saveconfigbutton.grid(row=3, column=1, padx=5, pady=5, sticky='w')
exitbutton = Button(button_frame, text="Exit", command=exit_client)
exitbutton.grid(row=3, column=2, padx=5, pady=5, sticky='e')

root.mainloop()
