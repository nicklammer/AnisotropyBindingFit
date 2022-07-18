#config parser for FA plotting
from configparser import ConfigParser
import os
import string

parsestyle = ConfigParser()
dir_path = os.path.dirname(os.path.realpath(__file__))
style_path = os.path.join(dir_path, 'plot_style.ini')
parsestyle.read(style_path)

#pull color keys
colors_key_temp_fordict = parsestyle.get('colors', 'colors_key')
colors_key_fordict = colors_key_temp_fordict.split(', ')

#marker style dictionary
marker_key_temp = parsestyle.get('marker', 'marker_key')
marker_key = marker_key_temp.split(', ')

#line style dictionary
line_key_temp = parsestyle.get('line', 'line_key')
line_key = line_key_temp.split(', ')

