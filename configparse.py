#config parser for FA plotting
from ConfigParser import SafeConfigParser
import os

parser = SafeConfigParser()
parsestyle = SafeConfigParser()
dir_path = os.path.dirname(os.path.realpath(__file__))
config_path = os.path.join(dir_path, 'config.ini')
style_path = os.path.join(dir_path, 'plot_style.ini')
parser.read(config_path)
parsestyle.read(style_path)

#file options
raw_data = parser.getboolean('file options', 'raw data')
file_sheet = parser.get('file options', 'sheet file')
path_output = parser.get('file options', 'output folder')
#sample layout
rows = parser.getboolean('sample layout', 'rows')
titrations = parser.getint('sample layout', 'titrations')
start_col = parser.getint('sample layout', 'starting column') 
start_row = parser.getint('sample layout', 'starting row')
concentration = parser.getfloat('sample layout', 'max concentration')
dilution_factor = parser.getfloat('sample layout', 'dilution factor')
units = parser.get('sample layout', 'units')
dupe = parser.getboolean('sample layout', 'duplicates')
single = parser.getint('sample layout', 'single')
sample_temp = parser.get('sample layout', 'sample')
sample = [int(x) for x in sample_temp.split(', ')]
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
color_single_key = parser.get('plot options', 'color single')
#strip is a work around for the gui editor. I can't get it to work there
color_multiple_key_temp = parser.get('plot options', 'color multiple').strip(", ")
color_multiple_key = color_multiple_key_temp.split(', ')
marker_chosen = parser.get('plot options', 'marker style')
marker_size = parser.getfloat('plot options', 'marker size')
line_chosen = parser.get('plot options', 'line style')
line_width = parser.getfloat('plot options', 'line width')
legend = parser.getboolean('plot options', 'legend')
svg = parser.getboolean('plot options', 'svg')
plottitle = parser.get('plot options', 'plot title')
plotname = parser.get('plot options', 'plot name')

#make the color dictionary, pull values for colors saved to the config as keys
colors_key_temp = parsestyle.get('colors', 'colors_key')
colors_value_temp = parsestyle.get('colors', 'colors_value')
colors_key = colors_key_temp.split(', ')
colors_value = colors_value_temp.split(', ')
colors_dict = dict(zip(colors_key, colors_value))

color_single = colors_dict[color_single_key]
color_multiple = []
for key in color_multiple_key:
	color_multiple.append(colors_dict[key])

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
