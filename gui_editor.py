from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from matplotlib import markers
import gui_configparse
import read
import os
import main
from configparser import ConfigParser

class Editor:
	def __init__(self, parent):
		self.parent = parent
		#set up main window
		parent.title("FA plotting configuration")
		parent.grid_columnconfigure(1, weight=1)
		parent.grid_rowconfigure(1, weight=1)
		#set all the vars to be used
		self.raw_data = BooleanVar()
		self.sheet_path = StringVar()
		self.folder_path = StringVar()
		self.ap_choice = StringVar()
		self.duplicate = BooleanVar()
		self.normalization_value = BooleanVar()
		self.legend = BooleanVar()
		self.png = BooleanVar()
		self.svg = BooleanVar()
		self.showplot = BooleanVar()
		#load keys from gui_configparse
		self.colors_key = gui_configparse.colors_key_fordict
		self.marker_key = gui_configparse.marker_key
		self.line_key = gui_configparse.line_key
		#loading config files
		self.dir_path = os.path.dirname(os.path.realpath(__file__))
		self.config_path = os.path.join(self.dir_path, 'config.ini')
		self.parser = ConfigParser()
		self.parser.read(self.config_path)

		self.config_frame = Frame(root)
		self.config_frame.grid(row=0, column=0, columnspan=2, pady=3, sticky='nsew')
		self.config_frame.grid_columnconfigure(1, weight=1)
		self.config_label=Label(self.config_frame, text="Load config file").grid(row=0, padx=2, pady=3, sticky='nw')
		self.config_load_box_path = StringVar()
		self.config_load_box_path.set(self.config_path)
		self.config_load_box = Entry(self.config_frame, textvariable=self.config_load_box_path)
		self.config_load_box.grid(row=0, column=1, padx=3, pady=2, sticky='new')
		self.config_load_button = Button(self.config_frame, text="Browse", command=self.browse_config)
		self.config_load_button.grid(row=0, column=2, sticky='nw')

		self.nb = ttk.Notebook(root)
		self.nb.grid(row=1, column=0, columnspan=2, sticky='nsew')
		self.tab1 = Frame(self.nb)
		self.tab_data = Frame(self.nb)
		self.tab_fit = Frame(self.nb)
		self.tab_plot = Frame(self.nb)
		self.tab_style = Frame(self.nb)
		self.nb.add(self.tab1, text="Data")
		self.nb.add(self.tab_data, text="Data cont.")
		self.nb.add(self.tab_fit, text="Fit options")
		self.nb.add(self.tab_plot, text="Plot options")
		self.nb.add(self.tab_style, text="Style options")
		self.nb.enable_traversal()

		self.tab1.grid_columnconfigure(1, weight=1)

		#file information (Data tab)
		self.dataSheet_label=Label(self.tab1, text="Data sheet").grid(row=0, sticky='w', padx=10)
		self.data_box = Entry(self.tab1, textvariable=self.sheet_path)
		self.data_box.grid(row=0, column=1, sticky='ew')
		self.data_browse = Button(self.tab1, text="Browse", command=self.browse_sheet)
		self.data_browse.grid(row=0, column=2, sticky='w')

		self.raw_label=Label(self.tab1, text="Raw data or pre-formatted?").grid(row=1)
		self.raw = Radiobutton(self.tab1, text="Raw", variable=self.raw_data, value=True, command=self.raw_data_true)
		self.formatted = Radiobutton(self.tab1, text="Pre-formatted", variable=self.raw_data, value=False, command=self.raw_data_false)
		self.raw.grid(row=2)
		self.formatted.grid(row=2, column=1, sticky='w')

		self.aniso_label=Label(self.tab1, text="Anisotropy (parallel and perpendicular) or polarization?\n(Don't forget to set initial parameters)").grid(row=3, padx=3)
		self.aniso = Radiobutton(self.tab1, text="Anisotropy", variable=self.ap_choice, value='anisotropy')
		self.polar = Radiobutton(self.tab1, text="Polarization", variable=self.ap_choice, value='polarization')
		self.aniso.grid(row=4, pady=3)
		self.polar.grid(row=4, column=1, sticky='w')

		self.output_label=Label(self.tab1, text="Output folder").grid(row=5, sticky='w', padx=10)
		self.output_box = Entry(self.tab1, textvariable=self.folder_path)
		self.output_box.grid(row=5, column=1, sticky='ew')
		self.output_browse = Button(self.tab1, text="Browse", command=self.browse_dir)
		self.output_browse.grid(row=5, column=2, sticky='w')

		#Titration info (Data cont. tab)
		self.unit_label=Label(self.tab_data, text="Units:").grid(row=0,column=3)
		self.units_box = Entry(self.tab_data)
		self.units_box.grid(row=0, column=4, sticky='ew', pady=2)

		self.duplicate_check = Checkbutton(self.tab_data, text="Samples done in duplicate\n(enter samples one after the other)", 
			variable=self.duplicate, onvalue=True, offvalue=False)
		self.duplicate_check.grid(row=0,column=6,sticky='e')

		#actual data layout (Data cont. tab)
		self.dliution_label=Label(self.tab_data, text="Number of unique\nprotein dilutions").grid(row=0, column=0, padx=3, pady=5)
		self.unique_dilutions = Entry(self.tab_data, justify='center', width=7)
		self.unique_dilutions.grid(row=0, column=1)
		self.samplelabels_label=Label(self.tab_data, text="Sample labels", justify='center').grid(row=1, column=0)
		self.titration_label=Label(self.tab_data, text="Titration row\nor column", justify='center').grid(row=1, column=1)
		self.well_label=Label(self.tab_data, text="Titration wells", justify='center').grid(row=1, column=2)
		self.conc_label=Label(self.tab_data, text="Starting\nconcentration\n(at first well)", justify='center').grid(row=1, column=3)
		self.dilution_label=Label(self.tab_data, text="Dilution factor\n(1:2 is 2)", justify='center').grid(row=1, column=4)
		self.lconc_label=Label(self.tab_data, text="Ligand\nconcentration\n(each sample)", justify='center').grid(row=1, column=5)
		self.wells_label=Label(self.tab_data, text="Excluded\nwells", justify='center').grid(row=1, column=6)
		#check update_boxes function for how these boxes are organized
		self.label_boxes = []
		self.rc_boxes = []
		self.titration_boxes = []
		self.conc_boxes = []
		self.dilution_boxes = []
		self.ligand_boxes = []
		self.exclude_boxes = []
		self.updatebutton = Button(self.tab_data, text="Update boxes",
			command=self.update_boxes)
		self.updatebutton.grid(row=0, column=2, padx=5, pady=5)
		
		#Fit options
		self.fit_label=Label(self.tab_fit, text="Choose type of fit:").grid(row=0)
		self.fiteqs = ['simplified binding isotherm','quadratic','Hill','multi-site']
		self.fiteqs_id = ['kdfit','quad','hill','multi']
		self.fiteqs_dict = dict(zip(self.fiteqs_id,range(len(self.fiteqs))))
		#using a dropdown menu makes adding new fits waaay easier
		self.fit_menu = ttk.Combobox(self.tab_fit, values=self.fiteqs, width=25)
		self.fit_menu.grid(row=0, column=1, padx=3, pady=3)

		self.para_label=Label(self.tab_fit, text="Initial parameters:").grid(row=1, pady=2)
		self.kd_label=Label(self.tab_fit, text="Kd:").grid(row=2, pady=2)
		self.kd_box = Entry(self.tab_fit)
		self.kd_box.grid(row=2, column=1)
		self.s_label=Label(self.tab_fit, text="S:").grid(row=3, pady=2)
		self.s_box = Entry(self.tab_fit)
		self.s_box.grid(row=3, column=1)
		self.o_label=Label(self.tab_fit, text="O:").grid(row=4, pady=2)
		self.o_box = Entry(self.tab_fit)
		self.o_box.grid(row=4, column=1)
		self.multisite_label=Label(self.tab_fit, text="Multi-site binding only:").grid(row=5, pady=2)
		self.kd2_label=Label(self.tab_fit, text="Kd2:").grid(row=6, pady=2)
		self.kd2_box = Entry(self.tab_fit)
		self.kd2_box.grid(row=6, column=1)
		self.s2_label=Label(self.tab_fit, text="S2:").grid(row=7, pady=2)
		self.s2_box = Entry(self.tab_fit)
		self.s2_box.grid(row=7, column=1)
		self.lconc2_label=Label(self.tab_fit, text="Ligand concentrations in order\n(for pre-formatted data only):").grid(row=8, pady=2)
		self.L_box = Entry(self.tab_fit)
		self.L_box.grid(row=8, column=1)
		self.normalization_check = Checkbutton(self.tab_fit, text="Plot fraction bound normalization", 
			variable=self.normalization_value, onvalue=True, offvalue=False).grid(row=9)
		
		#Plot options
		self.plotoptions_label=Label(self.tab_plot, text="Plot options").grid(row=0, column=0, pady=4)
		self.samplesperplot_label=Label(self.tab_plot, text="Number of samples per plot:\n(Maximum of 6 or you can't read the table)").grid(row=1, column=0, pady=2)
		self.perplot_box = Entry(self.tab_plot)
		self.perplot_box.grid(row=1, column=1)

		self.legend_check = Checkbutton(self.tab_plot, text="Show legend", 
			variable=self.legend, onvalue=True, offvalue=False)
		self.legend_check.grid(row=2, column=0, columnspan=2)

		self.png_check = Checkbutton(self.tab_plot, text="Save .png files", 
			variable=self.png, onvalue=True, offvalue=False)
		self.png_check.grid(row=3, column=0, columnspan=2)

		self.svg_check = Checkbutton(self.tab_plot, text="Save .svg files", 
			variable=self.svg, onvalue=True, offvalue=False)
		self.svg_check.grid(row=4, column=0, columnspan=2)

		self.plottitle_label=Label(self.tab_plot, text="Plot title (for each plot):").grid(row=5, column=0)
		self.title_box = Entry(self.tab_plot)
		self.title_box.grid(row=5, column=1, pady=2)

		self.filename_label=Label(self.tab_plot, text="File name for the plots:").grid(row=6, column=0)
		self.plotname_box = Entry(self.tab_plot)
		self.plotname_box.grid(row=6, column=1, pady=2)

		self.show_check = Checkbutton(self.tab_plot, text="Show plots in a window", 
			variable=self.showplot, onvalue=True, offvalue=False)
		self.show_check.grid(row=7, column=0, columnspan=2)

		self.markerstyle_label=Label(self.tab_plot, text="Marker style and size:").grid(row=0, column=2)
		self.marker_size_box = Entry(self.tab_plot, justify='center', width=5)
		self.marker_size_box.grid(row=0, column=3, pady=1, sticky='w')

		self.linestyle_label=Label(self.tab_plot, text="Line width:").grid(row=1, column=2)
		self.line_width_box = Entry(self.tab_plot, justify='center', width=5)
		self.line_width_box.grid(row=1, column=3, pady=1, sticky='w')

		self.plottitlefontsize_label=Label(self.tab_plot, text="Plot title font size:").grid(row=2, column=2)
		self.plot_title_size_box = Entry(self.tab_plot, justify='center', width=5)
		self.plot_title_size_box.grid(row=2, column=3, pady=1, sticky='w')

		self.xaxistitlefontsize_label=Label(self.tab_plot, text="x-axis title font size:").grid(row=3, column=2)
		self.x_title_size_box = Entry(self.tab_plot, justify='center', width=5)
		self.x_title_size_box.grid(row=3, column=3, pady=1, sticky='w')

		self.yaxistitlefontsize_label=Label(self.tab_plot, text="y-axis title font size:").grid(row=4, column=2)
		self.y_title_size_box = Entry(self.tab_plot, justify='center', width=5)
		self.y_title_size_box.grid(row=4, column=3, pady=1, sticky='w')

		self.xtickfontsize_label=Label(self.tab_plot, text="x-tick font size:").grid(row=5, column=2)
		self.x_tick_label_size_box = Entry(self.tab_plot, justify='center', width=5)
		self.x_tick_label_size_box.grid(row=5, column=3, pady=1, sticky='w')

		self.ytickfontsize_label=Label(self.tab_plot, text="y-tick font size:").grid(row=6, column=2)
		self.y_tick_label_size_box = Entry(self.tab_plot, justify='center', width=5)
		self.y_tick_label_size_box.grid(row=6, column=3, pady=1, sticky='w')

		self.xticksize_label=Label(self.tab_plot, text="x-tick size:").grid(row=7, column=2)
		self.x_tick_size_box = Entry(self.tab_plot, justify='center', width=5)
		self.x_tick_size_box.grid(row=7, column=3, pady=1, sticky='w')

		self.yticksize_label=Label(self.tab_plot, text="y-tick size:").grid(row=8, column=2)
		self.y_tick_size_box = Entry(self.tab_plot, justify='center', width=5)
		self.y_tick_size_box.grid(row=8, column=3, pady=1, sticky='w')

		#Style options
		#bind tab changing to update the field in the style tab 
		#see update_style function below for how tab is organized
		self.nb.bind('<<NotebookTabChanged>>',self.tab_update)
		self.style_sample_label=Label(self.tab_style, text="Samples", justify='center').grid(row=0, column=0)
		self.color_label=Label(self.tab_style, text="Color", justify='center').grid(row=0, column=1)
		self.marker_label=Label(self.tab_style, text="Marker style", justify='center').grid(row=0, column=2)
		self.line_label=Label(self.tab_style, text="Line style", justify='center').grid(row=0, column=3)
		self.color_button=Button(self.tab_style, text="All", command=self.same_color)
		self.color_button.grid(row=1, column=1, sticky='n')
		self.marker_button=Button(self.tab_style, text="All", command=self.same_marker)
		self.marker_button.grid(row=1, column=2, sticky='n')
		self.line_button=Button(self.tab_style, text="All", command=self.same_line)
		self.line_button.grid(row=1, column=3, sticky='n')
		self.style_label = []
		self.color_boxes = []
		self.marker_boxes = []
		self.line_boxes = []

		#bottom buttons
		self.button_frame = Frame(parent)
		self.button_frame.grid(row=3, column=1)
		self.button_frame.grid_columnconfigure(0, weight=1)
		self.runbutton = Button(self.button_frame, text="Plot", command=self.run_main)
		self.runbutton.grid(row=3, column=0, padx=5, pady=5, sticky='w')
		self.savebutton = Button(self.button_frame, text="Save", command=self.save_everything)
		self.savebutton.grid(row=3, column=1, padx=5, pady=5, sticky='w')
		self.saveconfigbutton = Button(self.button_frame, text="Save as", command=self.save_config)
		self.saveconfigbutton.grid(row=3, column=2, padx=5, pady=5, sticky='w')
		self.exitbutton = Button(self.button_frame, text="Exit", command=self.exit_client)
		self.exitbutton.grid(row=3, column=3, padx=5, pady=5, sticky='e')
		
		self.fill_values()#fill in all the boxes
		self.default_disable()#start boxes disabled based on filled values
		self.default_enable()#start boxes enabled based on filled values

	#functions for buttons
	def exit_client(self):
		exit()
	def browse_config(self):
		#the first iteration of this gui used global variables all over the place
		#keeping them here as a reminder 
		#global config_load_box_path
		#global parser
		original = self.config_load_box_path.get()
		filename = filedialog.askopenfilename(title="Select config.ini to load", 
			filetypes=(("INI files","*.ini"),("All files", "*.*")))
		if filename == '':
			self.config_load_box_path.set(original)
		else:
			self.config_load_box_path.set(filename)
		print("Config changed to "+filename)
		self.parser.read(filename)
		self.fill_values()
		self.default_disable()
		self.default_enable()
	def browse_sheet(self):
		#global sheet_path
		original = self.sheet_path.get()
		filename = filedialog.askopenfilename(title="Select data sheet", 
			filetypes=(("Excel sheets","*.xlsx *.xls"),("All files", "*.*")))
		if filename == '':
			self.sheet_path.set(original)
		else:
			self.sheet_path.set(filename)
	def browse_dir(self):
		#global folder_path
		original = self.folder_path.get().strip('/')
		dirname = filedialog.askdirectory()
		if dirname == '':
			self.folder_path.set(original+'/')
		else:
			self.folder_path.set(dirname+'/')
	def raw_data_true(self):
		self.duplicate_check.config(state='normal')
		self.unique_dilutions.config(state='normal')
		self.updatebutton.config(state='normal')
		for i in range(int(self.unique_dilutions.get())):
			self.label_boxes[i].config(state='normal')
			self.rc_boxes[i].config(state='normal')
			self.titration_boxes[i].config(state='normal')
			self.conc_boxes[i].config(state='normal')
			self.dilution_boxes[i].config(state='normal')
			self.ligand_boxes[i].config(state='normal')
			self.exclude_boxes[i].config(state='normal')
		self.fill_style()
	def raw_data_false(self):
		self.duplicate_check.config(state='disabled')
		self.unique_dilutions.config(state='disabled')
		self.updatebutton.config(state='disabled')
		for i in range(int(self.unique_dilutions.get())):
			self.label_boxes[i].config(state='disabled')
			self.rc_boxes[i].config(state='disabled')
			self.titration_boxes[i].config(state='disabled')
			self.conc_boxes[i].config(state='disabled')
			self.dilution_boxes[i].config(state='disabled')
			self.ligand_boxes[i].config(state='disabled')
			self.exclude_boxes[i].config(state='disabled')
		self.fill_style()
	def same_color(self):
		color=self.color_boxes[0].get()
		for box in self.color_boxes:
			self.value_insert(box, color)
	def same_marker(self):
		marker=self.marker_boxes[0].get()
		for box in self.marker_boxes:
			self.value_insert(box, marker)
	def same_line(self):
		line=self.line_boxes[0].get()
		for box in self.line_boxes:
			self.value_insert(box, line)
	def update_boxes(self):
		#this is ugly but I'm leaving it for readability
		#this function is for updating how many samples you have and displaying new boxes
		boxes=["label","rc","titration","conc","dilution","ligand","exclude"]
		holder=dict(zip(boxes,[[] for _ in boxes]))#easier way to set up a bunch of empty lists
		#get entries from current boxes
		for i in range(len(self.label_boxes)):
			holder["label"].append(self.label_boxes[i].get())
			holder["rc"].append(self.rc_boxes[i].get())
			holder["titration"].append(self.titration_boxes[i].get())
			holder["conc"].append(self.conc_boxes[i].get())
			holder["dilution"].append(self.dilution_boxes[i].get())
			holder["ligand"].append(self.ligand_boxes[i].get())
			holder["exclude"].append(self.exclude_boxes[i].get())
			self.label_boxes[i].grid_forget()
			self.rc_boxes[i].grid_forget()
			self.titration_boxes[i].grid_forget()
			self.conc_boxes[i].grid_forget()
			self.dilution_boxes[i].grid_forget()
			self.ligand_boxes[i].grid_forget()
			self.exclude_boxes[i].grid_forget()
		#clear the box elements
		self.label_boxes = []
		self.rc_boxes = []
		self.titration_boxes = []
		self.conc_boxes = []
		self.dilution_boxes = []
		self.ligand_boxes = []
		self.exclude_boxes = []
		#append empty strings to display empty boxes when you add more
		while len(holder["label"]) < int(self.unique_dilutions.get()):
			holder["label"].append('')
			holder["rc"].append('')
			holder["titration"].append('')
			holder["conc"].append('')
			holder["dilution"].append('')
			holder["ligand"].append('')
			holder["exclude"].append('')
		#display boxes
		for n in range(int(self.unique_dilutions.get())):
			self.label_boxes.append(Entry(self.tab_data, justify='center', width=30))
			self.label_boxes[n].grid(row=n+2, column=0, pady=2)
			self.rc_boxes.append(Entry(self.tab_data, justify='center', width=10))
			self.rc_boxes[n].grid(row=n+2, column=1, pady=2)
			self.titration_boxes.append(Entry(self.tab_data, justify='center', width=7))
			self.titration_boxes[n].grid(row=n+2, column=2, pady=2)
			self.conc_boxes.append(Entry(self.tab_data, justify='center', width=8))
			self.conc_boxes[n].grid(row=n+2, column=3, pady=2)
			self.dilution_boxes.append(Entry(self.tab_data, justify='center', width=7))
			self.dilution_boxes[n].grid(row=n+2, column=4, pady=2)
			self.ligand_boxes.append(Entry(self.tab_data, justify='center', width=15))
			self.ligand_boxes[n].grid(row=n+2, column=5, pady=2)
			self.exclude_boxes.append(Entry(self.tab_data, justify='center', width=20))
			self.exclude_boxes[n].grid(row=n+2, column=6, pady=2, padx=8)
			self.label_boxes[n].insert('end', holder["label"][n])
			self.rc_boxes[n].insert('end', holder["rc"][n])
			self.titration_boxes[n].insert('end', holder["titration"][n])
			self.conc_boxes[n].insert('end', holder["conc"][n])
			self.dilution_boxes[n].insert('end', holder["dilution"][n])
			self.ligand_boxes[n].insert('end', holder["ligand"][n])
			self.exclude_boxes[n].insert('end', holder["exclude"][n])
	def tab_update(self,event):
		tab = event.widget.tab('current')['text']
		if tab == 'Style options':
			self.update_style()
			self.fill_style()
		else:
			pass
	def update_style(self):
		boxes=["label","color","marker","line"]
		holder=dict(zip(boxes,[[] for _ in boxes]))#easier way to set up a bunch of empty lists
		#get list of all sample labels
		if self.raw_data.get() == False:
			sheetpath=self.data_box.get()
			_,_,labels=read.data_read(sheetpath)
		else:
			labels_data = [x.get() for x in self.label_boxes]
			labels_temp = []
			for x in labels_data:
				labels_temp.append([n.strip() for n in x.split(',')])
			#I found this one liner to flatten a list of lists on stackoverflow
			labels=[x for xs in labels_temp for x in xs]
		#get entries from current boxes
		for i in range(len(self.style_label)):
			holder["label"].append(self.style_label[i].get())
			holder["color"].append(self.color_boxes[i].get())
			holder["marker"].append(self.marker_boxes[i].get())
			holder["line"].append(self.line_boxes[i].get())
			self.style_label[i].grid_forget()
			self.color_boxes[i].grid_forget()
			self.marker_boxes[i].grid_forget()
			self.line_boxes[i].grid_forget()
		#clear the box elements
		self.style_label = []
		self.color_boxes = []
		self.marker_boxes = []
		self.line_boxes = []
		#append empty strings to display empty boxes when you add more
		while len(holder["label"]) < len(labels):
			holder["label"].append('')
			holder["color"].append('')
			holder["marker"].append('')
			holder["line"].append('')
		#ensure no empty strings due to the data cont. tab having empty boxes
		if len(holder["label"]) > len(labels):
			for field in holder:
				holder[field] = holder[field][0:len(labels)]
		#display boxes
		for n in range(len(holder["label"])):
			self.style_label.append(Entry(self.tab_style, justify='center', width=15, state='normal'))
			self.style_label[n].grid(row=n+2,column=0,pady=2,padx=2)
			self.color_boxes.append(ttk.Combobox(self.tab_style, values=self.colors_key))
			self.color_boxes[n].grid(row=n+2, column=1, pady=2,padx=2)
			self.marker_boxes.append(ttk.Combobox(self.tab_style, values=self.marker_key))
			self.marker_boxes[n].grid(row=n+2, column=2, pady=2,padx=2)
			self.line_boxes.append(ttk.Combobox(self.tab_style, values=self.line_key))
			self.line_boxes[n].grid(row=n+2, column=3, pady=2,padx=2)
			self.style_label[n].insert('end', holder["label"][n])
			self.color_boxes[n].set(holder["color"][n])
			self.marker_boxes[n].set(holder["marker"][n])
			self.line_boxes[n].set(holder["line"][n])
	#function for setting all values after loading a config file
	def value_set(self, var, value):#for setting vars
		var.set(value)
	def value_insert(self, box, value):#for entry widgets
		box.delete(0, 'end')
		box.insert('end', value)
	def value_text_insert(self, box, value):#for text widgets
		box.delete('1.0', 'end')
		box.insert('end', value)
	def fill_values(self):
		self.value_set(self.raw_data, self.parser.getboolean('file options', 'raw data'))
		self.value_set(self.sheet_path, self.parser.get('file options', 'sheet file'))
		self.value_set(self.ap_choice, self.parser.get('file options', 'anisotropy or polarization'))
		self.value_set(self.folder_path, self.parser.get('file options', 'output folder'))
		self.value_insert(self.units_box, self.parser.get('sample layout', 'units'))
		self.value_insert(self.unique_dilutions, self.parser.get('sample layout', 'unique dilutions'))
		boxes=["label","rc","titration","conc","dilution","ligand","exclude"]
		holder=dict(zip(boxes,[[] for _ in boxes]))#easier way to set up a bunch of empty lists
		holder["label"] = [x.strip(':') for x in self.parser.get('sample layout', 'labels').split(': ')]
		holder["rc"] = [x.strip(':') for x in self.parser.get('sample layout', 'titration row or col').split(': ')]
		holder["titration"] = [x.strip() for x in self.parser.get('sample layout', 'titrations').split(',')]
		holder["conc"] = [x.strip() for x in self.parser.get('sample layout', 'concentrations').split(',')]
		holder["dilution"] = [x.strip() for x in self.parser.get('sample layout', 'dilution factors').split(',')]
		holder["ligand"] = self.parser.get('sample layout', 'ligand concentrations').split(': ')
		holder["exclude"] = self.parser.get('sample layout', 'excluded').split(': ')
		while len(holder["label"]) < int(self.unique_dilutions.get()):
			holder["label"].append('')
			holder["rc"].append('')
			holder["titration"].append('')
			holder["conc"].append('')
			holder["dilution"].append('')
			holder["ligand"].append('')
			holder["exclude"].append('')
		self.update_boxes()
		for n in range(int(self.unique_dilutions.get())):
			self.value_insert(self.label_boxes[n], holder["label"][n])
			self.value_insert(self.rc_boxes[n], holder["rc"][n])
			self.value_insert(self.titration_boxes[n], holder["titration"][n])
			self.value_insert(self.conc_boxes[n], holder["conc"][n])
			self.value_insert(self.dilution_boxes[n], holder["dilution"][n])
			self.value_insert(self.ligand_boxes[n], holder["ligand"][n])
			if holder["ligand"][n] == 'none':
				self.value_insert(self.ligand_boxes[n], '')
			else:
				self.value_insert(self.ligand_boxes[n], holder["ligand"][n])
			if holder["exclude"][n] == 'none':
				self.value_insert(self.exclude_boxes[n], '')
			else:
				self.value_insert(self.exclude_boxes[n], holder["exclude"][n])
		self.value_set(self.duplicate, self.parser.getboolean('sample layout', 'duplicates'))
		self.fit_menu.current(self.fiteqs_dict[self.parser.get('fit options', 'fiteq')])
		self.value_insert(self.kd_box, self.parser.getfloat('fit options', 'Kdi'))
		self.value_insert(self.s_box, self.parser.getfloat('fit options', 'Si'))
		self.value_insert(self.o_box, self.parser.getfloat('fit options', 'Oi'))
		self.value_insert(self.kd2_box, self.parser.getfloat('fit options', 'Kd2i'))
		self.value_insert(self.s2_box, self.parser.getfloat('fit options', 'S2i'))
		self.value_insert(self.L_box, self.parser.get('fit options', 'Ligand pre-formatted'))
		self.value_set(self.normalization_value, self.parser.getboolean('fit options', 'normalization'))
		self.value_insert(self.perplot_box, self.parser.getint('plot options', 'per plot'))
		self.value_insert(self.marker_size_box, self.parser.get('plot options', 'marker size'))
		self.value_insert(self.line_width_box, self.parser.get('plot options', 'line width'))
		self.value_insert(self.line_width_box, self.parser.get('plot options', 'line width'))
		self.value_insert(self.plot_title_size_box, self.parser.get('plot options', 'plot title size'))
		self.value_insert(self.x_title_size_box, self.parser.get('plot options', 'x title size'))
		self.value_insert(self.y_title_size_box, self.parser.get('plot options', 'y title size'))
		self.value_insert(self.x_tick_label_size_box, self.parser.get('plot options', 'x tick label size'))
		self.value_insert(self.y_tick_label_size_box, self.parser.get('plot options', 'y tick label size'))
		self.value_insert(self.x_tick_size_box, self.parser.get('plot options', 'x tick size'))
		self.value_insert(self.y_tick_size_box, self.parser.get('plot options', 'y tick size'))
		self.value_set(self.legend, self.parser.getboolean('plot options', 'legend'))
		self.value_set(self.png, self.parser.getboolean('plot options', 'png'))
		self.value_set(self.svg, self.parser.getboolean('plot options', 'svg'))
		self.value_insert(self.title_box, self.parser.get('plot options', 'plot title'))
		self.value_insert(self.plotname_box, self.parser.get('plot options', 'plot name'))
		self.value_set(self.showplot, self.parser.getboolean('plot options', 'show plot'))
		boxes=["label","color","marker","line"]
		holder=dict(zip(boxes,[[] for _ in boxes]))#easier way to set up a bunch of empty lists
		#get list of all sample labels
		if self.raw_data.get() == False:
			sheetpath=self.data_box.get()
			_,_,labels=read.data_read(sheetpath)
		else:
			labels_data = [x.strip(':') for x in self.parser.get('sample layout', 'labels').split(': ')]
			labels_temp = []
			for x in labels_data:
				labels_temp.append([n.strip() for n in x.split(',')])
			#I found this one liner to flatten a list of lists on stackoverflow
			labels=[x for xs in labels_temp for x in xs]
		holder["label"]=labels
		holder["color"] = [x.strip() for x in self.parser.get('plot options', 'colors').split(',')]
		holder["marker"] = [x.strip() for x in self.parser.get('plot options', 'marker style').split(',')]
		holder["line"] = [x.strip() for x in self.parser.get('plot options', 'line style').split(',')]
		self.update_style()
		for n in range(len(holder["label"])):
			self.value_insert(self.style_label[n], holder["label"][n])
			self.value_insert(self.color_boxes[n], holder["color"][n])
			self.value_insert(self.marker_boxes[n], holder["marker"][n])
			self.value_insert(self.line_boxes[n], holder["line"][n])
	def fill_style(self):
		#this makes sure the the style tab properly updates without erroring
		#there's probably a smarter way to condense these functions but I'll do that later
		boxes=["label","color","marker","line"]
		holder=dict(zip(boxes,[[] for _ in boxes]))#easier way to set up a bunch of empty lists
		#get list of all sample labels
		if self.raw_data.get() == False:
			sheetpath=self.data_box.get()
			_,_,labels=read.data_read(sheetpath)
		else:
			#labels_data = [x.strip(':') for x in self.parser.get('sample layout', 'labels').split(': ')]
			labels_data = [x.get() for x in self.label_boxes]
			labels_temp = []
			for x in labels_data:
				labels_temp.append([n.strip() for n in x.split(',')])
			#I found this one liner to flatten a list of lists on stackoverflow
			labels=[x for xs in labels_temp for x in xs]
		holder["label"]=labels
		#holder["color"] = [x.strip() for x in self.parser.get('plot options', 'colors').split(',')]
		#holder["marker"] = [x.strip() for x in self.parser.get('plot options', 'marker style').split(',')]
		#holder["line"] = [x.strip() for x in self.parser.get('plot options', 'line style').split(',')]
		for i in range(len(self.color_boxes)):
			holder["color"].append(self.color_boxes[i].get())
			holder["marker"].append(self.marker_boxes[i].get())
			holder["line"].append(self.line_boxes[i].get())
		self.update_style()
		for n in range(len(holder["label"])):
			self.value_insert(self.style_label[n], holder["label"][n])
			self.value_insert(self.color_boxes[n], holder["color"][n])
			self.value_insert(self.marker_boxes[n], holder["marker"][n])
			self.value_insert(self.line_boxes[n], holder["line"][n])
	def default_disable(self):
		if self.raw_data.get() == False:
			self.duplicate_check.config(state='disabled')
			self.unique_dilutions.config(state='disabled')
			self.updatebutton.config(state='disabled')
			for i in range(int(self.unique_dilutions.get())):
				self.label_boxes[i].config(state='disabled')
				self.rc_boxes[i].config(state='disabled')
				self.titration_boxes[i].config(state='disabled')
				self.conc_boxes[i].config(state='disabled')
				self.dilution_boxes[i].config(state='disabled')
				self.ligand_boxes[i].config(state='disabled')
				self.exclude_boxes[i].config(state='disabled')
	def default_enable(self):
		if self.raw_data.get() == True:
			self.duplicate_check.config(state='normal')
			self.unique_dilutions.config(state='normal')
			self.updatebutton.config(state='normal')
			for i in range(int(self.unique_dilutions.get())):
				self.label_boxes[i].config(state='normal')
				self.rc_boxes[i].config(state='normal')
				self.titration_boxes[i].config(state='normal')
				self.conc_boxes[i].config(state='normal')
				self.dilution_boxes[i].config(state='normal')
				self.ligand_boxes[i].config(state='normal')
				self.exclude_boxes[i].config(state='normal')
	
	#function for writing everything to the config.ini
	def config_set(self,section, option, value):
		self.parser.set(section, option, value)
	def config_write(self,file):
		configfile = open(file, 'w')
		self.parser.write(configfile)
	def save_everything(self):
		self.config_set('file options', 'raw data', str(self.raw_data.get()))
		self.config_set('file options', 'sheet file', self.data_box.get())
		self.config_set('file options', 'anisotropy or polarization', self.ap_choice.get())
		self.config_set('file options', 'output folder', self.output_box.get())
		boxes=["label","rc","titration","conc","dilution","ligand","exclude"]
		holder=dict(zip(boxes,[[] for _ in boxes]))#easier way to set up a bunch of empty lists
		for i in range(len(self.label_boxes)):
			holder["label"].append(self.label_boxes[i].get().replace('%','%%'))
			holder["rc"].append(self.rc_boxes[i].get())
			holder["titration"].append(self.titration_boxes[i].get())
			holder["conc"].append(self.conc_boxes[i].get())
			holder["dilution"].append(self.dilution_boxes[i].get())
			if self.ligand_boxes[i].get() == '':
				holder["ligand"].append('none')
			else:
				holder["ligand"].append(self.ligand_boxes[i].get())
			if self.exclude_boxes[i].get() == '':
				holder["exclude"].append('none')
			else:
				holder["exclude"].append(self.exclude_boxes[i].get())
		self.config_set('sample layout', 'unique dilutions', self.unique_dilutions.get())
		#possible to save config with empty strings for sample info, cut that out
		label_check=holder["label"]
		if label_check[-1] == '':
			for field in holder:
				holder[field].pop()
		self.config_set('sample layout', 'labels', ': '.join(holder["label"]))
		self.config_set('sample layout', 'titration row or col', ': '.join(holder["rc"]))
		self.config_set('sample layout', 'titrations', ', '.join(holder["titration"]))
		self.config_set('sample layout', 'concentrations', ', '.join(holder["conc"]))
		self.config_set('sample layout', 'dilution factors', ', '.join(holder["dilution"]))
		self.config_set('sample layout', 'ligand concentrations', ': '.join(holder["ligand"]))
		self.config_set('sample layout', 'excluded', ': '.join(holder["exclude"]))
		self.config_set('sample layout', 'units', self.units_box.get())
		self.config_set('sample layout', 'duplicates', str(self.duplicate.get()))
		self.config_set('fit options', 'fiteq', self.fiteqs_id[self.fit_menu.current()])
		self.config_set('fit options', 'Kdi', self.kd_box.get())
		self.config_set('fit options', 'Si', self.s_box.get())
		self.config_set('fit options', 'Oi', self.o_box.get())
		self.config_set('fit options', 'Kd2i', self.kd2_box.get())
		self.config_set('fit options', 'S2i', self.s2_box.get())
		self.config_set('fit options', 'Ligand pre-formatted', self.L_box.get())
		self.config_set('fit options', 'normalization', str(self.normalization_value.get()))
		self.config_set('plot options', 'per plot', self.perplot_box.get())
		self.config_set('plot options', 'marker size', self.marker_size_box.get())
		self.config_set('plot options', 'line width', self.line_width_box.get())
		self.config_set('plot options', 'plot title size', self.plot_title_size_box.get())
		self.config_set('plot options', 'x title size', self.x_title_size_box.get())
		self.config_set('plot options', 'y title size', self.y_title_size_box.get())
		self.config_set('plot options', 'x tick label size', self.x_tick_label_size_box.get())
		self.config_set('plot options', 'y tick label size', self.y_tick_label_size_box.get())
		self.config_set('plot options', 'x tick size', self.x_tick_size_box.get())
		self.config_set('plot options', 'y tick size', self.y_tick_size_box.get())
		self.config_set('plot options', 'legend', str(self.legend.get()))
		self.config_set('plot options', 'png', str(self.png.get()))
		self.config_set('plot options', 'svg', str(self.svg.get()))
		self.config_set('plot options', 'plot title', self.title_box.get().replace('%', '%%'))
		self.config_set('plot options', 'plot name', self.plotname_box.get().replace('%', '%%'))
		self.config_set('plot options', 'show plot', str(self.showplot.get()))
		boxes=["label","color","marker","line"]
		holder=dict(zip(boxes,[[] for _ in boxes]))#easier way to set up a bunch of empty lists
		for i in range(len(self.color_boxes)):
			holder["color"].append(self.color_boxes[i].get())
			holder["marker"].append(self.marker_boxes[i].get())
			holder["line"].append(self.line_boxes[i].get())
		if label_check[-1] == '':
			for field in holder:
				holder[field].pop()
		self.config_set('plot options', 'colors', ', '.join(holder["color"]))
		self.config_set('plot options', 'marker style', ', '.join(holder["marker"]))
		self.config_set('plot options', 'line style', ', '.join(holder["line"]))
		self.config_write(self.config_path)
		self.config_write(self.config_load_box_path.get())
		print("config saved")
	def save_config(self):
		savedir = filedialog.asksaveasfilename(title="Save config as", defaultextension='.ini',
			filetypes=((".ini files","*.ini"),("All files", "*.*")))
		if savedir != '':
			self.save_everything()
			self.config_write(savedir)
		else:
			pass
	def run_main(self):
		self.save_everything()
		main.run()

if __name__ == '__main__':
	root = Tk()
	editorGui = Editor(root)
	root.mainloop()