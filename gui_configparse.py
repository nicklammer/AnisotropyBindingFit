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

#make the color dictionary, pull values for colors saved to the config as keys
colors_key=[x.strip() for x in parser.get('plot options', 'colors').split(',')]
colors_key_temp_fordict = parsestyle.get('colors', 'colors_key')
colors_value_temp_fordict = parsestyle.get('colors', 'colors_value')
colors_key_fordict = colors_key_temp_fordict.split(', ')
colors_value_fordict = colors_value_temp_fordict.split(', ')
colors_dict = dict(zip(colors_key_fordict, colors_value_fordict))

colors = []
for key in colors_key:
	colors.append(colors_dict[key])

#marker style dictionary
marker_chosen = parser.get('plot options', 'marker style')
marker_key_temp = parsestyle.get('marker', 'marker_key')
marker_value_temp = parsestyle.get('marker', 'marker_value')
marker_key = marker_key_temp.split(', ')
marker_value = marker_value_temp.split(', ')
marker_dict = dict(zip(marker_key, marker_value))
marker = marker_dict[marker_chosen]

#line style dictionary
line_chosen = parser.get('plot options', 'line style')
line_key_temp = parsestyle.get('line', 'line_key')
line_value_temp = parsestyle.get('line', 'line_value')
line_key = line_key_temp.split(', ')
line_value = line_value_temp.split(', ')
line_dict = dict(zip(line_key, line_value))
line_style = line_dict[line_chosen]
