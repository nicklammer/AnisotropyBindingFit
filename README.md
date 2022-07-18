# AnisotropyBindingFit
### Scripts for fitting raw fluorescence anisotropy data for binding experiments.

https://github.com/nicklammer/AnisotropyBindingFit

I updated this to be used with python 3.7.

#### Requirements:
	-pandas and openpyxl for working with spreadsheets
	-scipy, numpy, and matplotlib for fitting and plotting.

#### Use
	Currently only reads a specific format for the raw data (microplate view, parallel and perpendicular intensities separated or polarization values).
	Also reads a pre-formatted data sheet as well. This can be anisotropy or fraction bound:
		-Must be an excel sheet and data should be in the first sheet. 
		-Data need to be in the following format: first row as a header (no data), rest data. Each sample should be 2 columns with concentration on the left and anisotropy/fraction bound on the right (x, y). 

##### To use:
	-Run the gui editor with python3. You can also edit the config.ini directly in a text editor. If you do this, use %% instead of % in names/labels to avoid interpolation errors. I recommend using the editor.
	-If you want to keep a config to reuse, use the 'Save As' button. Then you can load it next time you use the gui.
	-Click the 'Plot' button or run main. 
	-If everything works, it should pop out an excel sheet with the protein concentrations and corresponding anisotropy values and log plots using those values
	-If something didn't work right, read below.
	-If nothing in here helps, reach out.

##### Things to keep in mind so the scripts work:
	-If you want to change the plotting order, either rearrange the raw data sheet to put them next to each other or rearrange the sheet that the script gives you with calculated anisotropies.
	-Duplicates need to have their data side-by-side (sample 1 = A, B; not A, C, for example). If they were not read that way, then you can rearrange the sheet to fix this.
	-Maintain comma-space (", ") separation between multiple entries (samples, labels, colors, etc.).
	-If values are missing, then the script will error. For example, you give 4 samples, but only 2 labels.
	-Normalization does not currently plot well for samples that do not bind.
	-If you are not using a value, do not delete it. Just leave it alone and it will be ignored.

#### Errors, other info

##### Common errors and possible reasons:
	-If you get a "list index out of range" it's likely that a field does not have enough values or has too many. Check that your samples, labels, colors, etc. match up in terms of size.
	-If you can't open the gui, it's possible that fields in your config do not have their values separated properly. In most cases, they need to be separated by a comma and a space (", "). In the case of samples, each sample set is separated by colon and space (": ") and the samples themselves by comma-space. To fix the issue, you will have to open the config.ini in a text editor and fix the problem values. I recommend saving a backup config.ini so you can overwrite the error-causing one.

##### Function of each script:
	-gui_editor.py manages the interface for editing the config.ini file. Takes the current values and fills them in, then saves over the existing file with the present values. Also enables plotting.
	-configparse.py parses the config.ini for use by other scripts.
	-gui_configparse.py parses config.ini for the gui. This is separate to reduce gui errors.
	-read.py handles the Excel files. Contains functions that extract the parallel and perpendicular intensities, remove empty values, average duplicates if necessary, calculate concentrations, sort everything into lists in order of the samples, write to a new Excel file, and read a pre-formatted Excel file.
	-plot.py contains the fitting equations, general log plotting function, and functions for sorting data into the right number of plots.
	-main.py imports from configparse.py, cleans up some variables, and sends data to other scripts.

	The read script can be edited to use different data formats as long as it goes to the plotting script in the correct format:
		-A list of the concentrations for each sample (x-values) and a list of the anisotropies for each sample (y-values). Each list should be a list of lists, with each interior list being a sample.
		-x and y lists need to both be ordered by sample so they match up.