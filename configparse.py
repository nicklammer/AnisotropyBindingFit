#config parser for FA plotting
from configparser import ConfigParser
import os
import string

parser = ConfigParser()
parsestyle = ConfigParser()
dir_path = os.path.dirname(os.path.realpath(__file__))
config_path = os.path.join(dir_path, 'config.ini')
style_path = os.path.join(dir_path, 'plot_style.ini')
parser.read(config_path)
parsestyle.read(style_path)

def config_write(file):
	configfile = open(file, 'w')
	parser.write(configfile)
#create dict for letter denoted wells for later
letters=dict(zip((string.ascii_uppercase)[0:16],range(0,16)))

#file options
raw_data = parser.getboolean('file options', 'raw data')
file_sheet = parser.get('file options', 'sheet file')
a_or_p = parser.get('file options', 'anisotropy or polarization')
path_output = parser.get('file options', 'output folder')
#sample layout
labels_temp = parser.get('sample layout', 'labels').split(': ')
labels = []
for x in labels_temp:
	labels.append([n.strip() for n in x.split(',')])

rc_temp = parser.get('sample layout', 'titration row or col').split(': ')
rc = []
for x in rc_temp:
	rc.append([n.strip() for n in x.split(',')])
#get number of titrations from well range
wells_temp = parser.get('sample layout', 'titrations').split(',')
wells = []
for x in wells_temp:
	wells.append([n.strip() for n in x.split('-')])
#change letter wells to index numbers
for i in range(len(wells)):
	for n in range(len(wells[i])):
		if wells[i][n].isalpha()==True:
			wells[i][n] = int(letters[wells[i][n]])
		elif wells[i][n].isdigit()==True:
			wells[i][n] = int(wells[i][n])-1 #convert to zero index
titrations = [int(x[1])-int(x[0])+1 for x in wells]
concentrations = [float(x.strip()) for x in parser.get('sample layout', 'concentrations').split(',')]
dilution_factors = [float(x.strip()) for x in parser.get('sample layout', 'dilution factors').split(',')]

#make ligands concentration and exclude lists usable
ligand_conc_temp = parser.get('sample layout', 'ligand concentrations').split(': ')
ligand_conc_split = []
ligand_conc = []
for x in ligand_conc_temp:
	ligand_conc_split.append([n.strip() for n in x.split(',')])
for x in ligand_conc_split:
	if x == ['none'] or x == ['']:
		ligand_conc.append([float(0)])
	else:
		ligand_conc.append([float(n) for n in x])
exclude_temp = parser.get('sample layout', 'excluded').split(': ')
exclude_split = []
exclude = []
for x in exclude_temp:
	exclude_split.append([n.strip() for n in x.split(',')])
for x in exclude_split:
	if x == ['none'] or x == ['']:
		exclude.append([None])
	else:
		exclude.append(x)
#change letter wells to index number
for i in range(len(exclude)):
	if exclude[i] != [None]:
		for n in range(len(exclude[i])):
			if exclude[i][n].isalpha()==True:
				exclude[i][n] = int(letters[exclude[i][n]]) - int(wells[i][0])
			elif exclude[i][n].isdigit()==True:
				exclude[i][n] = (int(exclude[i][n])-1) - int(wells[i][0])

units = parser.get('sample layout', 'units')
dupe = parser.getboolean('sample layout', 'duplicates')
#fit options
fiteq = parser.get('fit options', 'fiteq')
Kdi = parser.getfloat('fit options', 'Kdi')
Si = parser.getfloat('fit options', 'Si')
Oi = parser.getfloat('fit options', 'Oi')
p0 = [Kdi, Si, Oi]
L_pre_temp = parser.get('fit options', 'ligand pre-formatted').split(', ')
L_pre = [float(x) for x in L_pre_temp]
normalization = parser.getboolean('fit options', 'normalization')
#plot options
perplot = parser.getint('plot options', 'per plot')
colors_key=[x.strip() for x in parser.get('plot options', 'colors').split(',')]
marker_chosen = parser.get('plot options', 'marker style')
marker_size = parser.getfloat('plot options', 'marker size')
line_chosen = parser.get('plot options', 'line style')
line_width = parser.getfloat('plot options', 'line width')
plot_title_size = parser.getfloat('plot options', 'plot title size')
x_title_size = parser.getfloat('plot options', 'x title size')
y_title_size = parser.getfloat('plot options', 'y title size')
x_tick_label_size = parser.getfloat('plot options', 'x tick label size')
y_tick_label_size = parser.getfloat('plot options', 'y tick label size')
x_tick_size = parser.getfloat('plot options', 'x tick size')
y_tick_size = parser.getfloat('plot options', 'y tick size')
legend = parser.getboolean('plot options', 'legend')
png = parser.getboolean('plot options', 'png')
svg = parser.getboolean('plot options', 'svg')
plottitle = parser.get('plot options', 'plot title')
plotname = parser.get('plot options', 'plot name')
showplot = parser.getboolean('plot options', 'show plot')

#make the color dictionary, pull values for colors saved to the config as keys
colors_key_temp_fordict = parsestyle.get('colors', 'colors_key')
colors_value_temp_fordict = parsestyle.get('colors', 'colors_value')
colors_key_fordict = colors_key_temp_fordict.split(', ')
colors_value_fordict = colors_value_temp_fordict.split(', ')
colors_dict = dict(zip(colors_key_fordict, colors_value_fordict))

colors = []
for key in colors_key:
	colors.append(colors_dict[key])

#marker style dictionary
marker_key_temp = parsestyle.get('marker', 'marker_key')
marker_value_temp = parsestyle.get('marker', 'marker_value')
marker_key = marker_key_temp.split(', ')
marker_value = marker_value_temp.split(', ')
marker_dict = dict(zip(marker_key, marker_value))
marker = marker_dict[marker_chosen]

#line style dictionary
line_key_temp = parsestyle.get('line', 'line_key')
line_value_temp = parsestyle.get('line', 'line_value')
line_key = line_key_temp.split(', ')
line_value = line_value_temp.split(', ')
line_dict = dict(zip(line_key, line_value))
line_style = line_dict[line_chosen]
