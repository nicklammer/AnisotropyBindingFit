#config parser for FA plotting
from configparser import ConfigParser
import os

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

#file options
raw_data = parser.getboolean('file options', 'raw data')
file_sheet = parser.get('file options', 'sheet file')
a_or_p = parser.get('file options', 'anisotropy or polarization')
path_output = parser.get('file options', 'output folder')
#sample layout
rows = parser.getboolean('sample layout', 'rows')
concentrations = parser.get('sample layout', 'concentrations').split(', ')
concentrations = [float(n) for n in concentrations]
dilution_factors = parser.get('sample layout', 'dilution factors').split(', ')
dilution_factors = [float(n) for n in dilution_factors]
titrations = parser.get('sample layout', 'titrations').split(', ')
titrations = [int(n) for n in titrations]
#make sample and exclude lists usable
samples_temp = parser.get('sample layout', 'samples').split(': ')
samples_split = []
samples = []
for x in samples_temp:
	samples_split.append(x.split(', '))
for x in samples_split:
	if x == ['none'] or x == ['']:
		raise Exception('Must have sample numbers (check gui/config)')
	else:
		samples.append([int(n) for n in x])
exclude_temp = parser.get('sample layout', 'excluded').split(': ')
exclude_split = []
exclude = []
for x in exclude_temp:
	exclude_split.append(x.split(', '))
for x in exclude_split:
	if x == ['none'] or x == ['']:
		exclude.append([None])
	else:
		exclude.append([int(n) for n in x])
units = parser.get('sample layout', 'units')
dupe = parser.getboolean('sample layout', 'duplicates')
labels_temp = parser.get('sample layout', 'labels')
labels = labels_temp.split(', ')
#fit options
fiteq = parser.get('fit options', 'fiteq')
conc_L = parser.getfloat('fit options', 'ligand concentration')
Kdi = parser.getfloat('fit options', 'Kdi')
Si = parser.getfloat('fit options', 'Si')
Oi = parser.getfloat('fit options', 'Oi')
p0 = [Kdi, Si, Oi]
normalization = parser.getboolean('fit options', 'normalization')
#plot options
perplot = parser.getint('plot options', 'per plot')
#strip is a work around for the gui editor. I can't get it to work there
colors_key_temp = parser.get('plot options', 'colors').strip(", ")
colors_key = colors_key_temp.split(', ')
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
