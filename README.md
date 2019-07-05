# AnisotropyBindingFit
Scripts for fitting raw fluorescence anisotropy data for binding experiments.

I wrote this for python 2.7.16. In python 3 they replaced basestring with str (see read.py). If you use python 3, just change every instance of basestring into str. All prints were written to work on 3. The gui (Tkinter) may be different for 3 as well.

Requires xlrd, xlwt, and xlutils for using excel spreadsheets; scipy, numpy, and matplotlib for fitting and plotting.

Currently only reads a specific format for the raw data (microplate view, parallel and perpendicular intensities separated)

To use:
	Edit config.ini with a text editor. Use %% instead of % in names/labels to avoid interpolation errors.
	Can also run the gui editor if you don't want to edit the text file. If you want to keep a config to reuse, use the save as button. Then you can load it next time you use the gui.
	Run main. 
	If everything works, it should pop out an excel sheet with the protein concentrations and corresponding anisotropy values and log plots using those values

The read script can be edited to use different data formats as long as it goes to the plotting script in the correct format:
	List where each entry is a list of x, y pairs that corresponds to one sample. x is concentration, y is anisotropy or fraction bound if you're using a different method. Example: [[(x1.1, y1.1),(x1.2, y1.2)], [(x2.1, y2.1), (x2.2, y2.2)]] for samples 1 and 2.

Quadratic fitting may not work properly. The fits seem fine, but I get a runtime warning, something about dividing by zero. I would just avoid it for now.