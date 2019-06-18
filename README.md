# AnisotropyBindingFit
Scripts for fitting raw fluorescence anisotropy data for binding experiments

Currently only reads a specific format for the raw data (microplate view, parallel and perpendicular intensities separated)

To use:
	Edit config to specify filepaths, plate information, plot customization, etc. There are notes in the config for more detailed info. 
	Run main. 
	If everything works, it should pop out an excel sheet with the protein concentrations and corresponding anisotropy values and log plots using those values

The read script can be edited to use different data formats as long as it goes to the plotting script in the correct format:
	List where each entry is a list of x, y pairs that corresponds to one sample. Example: [[(x1.1, y1.1),(x1.2, y1.2)], [(x2.1, y2.1), (x2.2, y2.2)]] for samples 1 and 2.

