#script that can read FP plate excel sheet, calculate anisotropy, and reorganize data to line up with protein concentrations
#this works for data formatted in a 384-well format from a clariostar instrument. Rows A-P, columns 1-24
import xlrd
import xlwt
from xlutils.copy import copy

#function for getting data for samples done per row
def excel_open_rowsamples(file_raw):
	holder = []
	parallel = []
	perpendicular = []
	#open raw data, first sheet
	wb = xlrd.open_workbook(file_raw)
	sheet_raw = wb.sheet_by_index(0)
	#scan rows for the parallel data by looking for the heading for it
	#then look through the rows for data. If there's data, add it to a holder list, then append
	for row in range(sheet_raw.nrows):
		#if str(sheet_raw.cell_value(row,1)) == "1. Raw Data (parallel)":
		if "parallel" in str(sheet_raw.cell_value(row,1)):
			for r in range(2,18):
				for c in range (1,25): #this makes it so you only get the number of titrations you want
					if isinstance(sheet_raw.cell_value(row+r,c), str) == False and sheet_raw.cell_value(row+r,c) > 0:
						holder.append(sheet_raw.cell_value(row+r,c))
				parallel.append(holder)
				holder = []
	#same as above, but with perpendicular data
		#elif str(sheet_raw.cell_value(row,1)) == "2. Raw Data (perpendicular)":
		elif "perpendicular" in str(sheet_raw.cell_value(row,1)):
			for r in range(2,18):
				for c in range (1,25):
					if isinstance(sheet_raw.cell_value(row+r,c), str) == False and sheet_raw.cell_value(row+r,c) > 0:
						holder.append(sheet_raw.cell_value(row+r,c))
				perpendicular.append(holder)
				holder = []
	parallel = [x for x in parallel if x!=[]]
	perpendicular = [x for x in perpendicular if x!=[]]
	return parallel, perpendicular

#function for getting data for samples done per column
def excel_open_colsamples(file_raw):
	holder = []
	parallel = []
	perpendicular = []
	#open raw data, first sheet
	wb = xlrd.open_workbook(file_raw)
	sheet_raw = wb.sheet_by_index(0)
	#this is convoluted-looking because I couldn't think of a better way at the time
	#scan column and rows for parallel and perpendicular data
	for col in range(sheet_raw.ncols):
		for row in range(sheet_raw.nrows):
			#if str(sheet_raw.cell_value(row,col)) == "1. Raw Data (parallel)":
			if "parallel" in str(sheet_raw.cell_value(row,col)):
				for c in range (24):
					for r in range(2,18):
						if isinstance(sheet_raw.cell_value(row+r, col+c), str) == False and sheet_raw.cell_value(row+r, col+c) > 0:
							holder.append(sheet_raw.cell_value(row+r,col+c))
					parallel.append(holder)
					holder = []
			#elif str(sheet_raw.cell_value(row,col)) == "2. Raw Data (perpendicular)":
			elif "perpendicular" in str(sheet_raw.cell_value(row,col)):
				for c in range (24):
					for r in range(2,18):
						if isinstance(sheet_raw.cell_value(row+r, col+c), str) == False and sheet_raw.cell_value(row+r, col+c) > 0:
							holder.append(sheet_raw.cell_value(row+r,col+c))
					perpendicular.append(holder)
					holder = []	
	parallel = [x for x in parallel if x!=[]]
	perpendicular = [x for x in perpendicular if x!=[]]

	return parallel, perpendicular

def polarization_rowsamples(file_raw):
	holder = []
	polar = []
	#open raw data, first sheet
	wb = xlrd.open_workbook(file_raw)
	sheet_raw = wb.sheet_by_index(0)
	#scan rows for the polarization data by looking for the heading for it
	#then look through the rows for data. If there's data, add it to a holder list, then append
	for row in range(sheet_raw.nrows):
		if str(sheet_raw.cell_value(row,1)).find('Polarization') == 0:#this is different than above because 'polarization' can show up multiple times in the same column
			for r in range(2,18):
				for c in range (1,25): #this makes it so you only get the number of titrations you want
					if isinstance(sheet_raw.cell_value(row+r,c), str) == False and sheet_raw.cell_value(row+r,c) > 0:
						holder.append(sheet_raw.cell_value(row+r,c))
				polar.append(holder)
				holder = []

	polar = [x for x in polar if x!=[]]
	return polar

def polarization_colsamples(file_raw):
	holder = []
	polar = []
	#open raw data, first sheet
	wb = xlrd.open_workbook(file_raw)
	sheet_raw = wb.sheet_by_index(0)
	#this is convoluted-looking because I couldn't think of a better way at the time
	#scan column and rows for polarization data
	for col in range(sheet_raw.ncols):
		for row in range(sheet_raw.nrows):
			if str(sheet_raw.cell_value(row,1)).find('Polarization') == 0:
				for c in range (24):
					for r in range(2,18):
						if isinstance(sheet_raw.cell_value(row+r, col+c), str) == False and sheet_raw.cell_value(row+r, col+c) > 0:
							holder.append(sheet_raw.cell_value(row+r,col+c))
					polar.append(holder)
					holder = []		

	polar = [x for x in polar if x!=[]]

	return polar

#trims data and averages if needed
def format(parallel, perpendicular, concentrations, dilution_factors, titrations, samples, dupe, exclude):
	holder = []
	FA = []
	FAavg = []
	for a in range(len(parallel)):
		holder = []
		for b in range(len(parallel[a])):
			holder.append(((parallel[a][b]-perpendicular[a][b])/(parallel[a][b]+2*perpendicular[a][b])))
		FA.append(holder)
	holder=[]
	if dupe == True:#if side-by-side duplicates, average the anisotropies
		for a in range(len(FA)):
			if a%2 == 0:
				for b in range(len(FA[a])):
					holder.append((FA[a][b]+FA[a+1][b])/2.0)
				FAavg.append(holder)
				holder = []
	else:
		FAavg = FA

	anisos = []
	for n in range(len(FAavg)):
		anisos.append([])
	for i in range(len(titrations)):#list
		for n in range(len(samples[i])):#list of lists
			for x in range(titrations[i]):#get number of titrations to add
				anisos[samples[i][n]-1].append(FAavg[samples[i][n]-1][x])

	#calculates titration concentrations based on max conc, dilution factor, and number of titrations
	conc_calculated = []
	conc_calculated_all = []
	for n in range(len(anisos)):
		conc_calculated_all.append([])
	for n in range(len(concentrations)):
		for i in range(titrations[n]):
			holder.append(float(concentrations[n])/(float(dilution_factors[n])**(i)))
		conc_calculated.append(holder)
		holder = []
	for i in range(len(concentrations)):#list
		for n in range(len(samples[i])):#list of lists
			conc_calculated_all[samples[i][n]-1] = [x for x in conc_calculated[i]]
	#deal with excluded points by changing them to None and then taking them out
	for i in range(len(exclude)):
		sampleind = [x-1 for x in samples[i]]
		if exclude[i] != [None]:
			for n in sampleind:
				for x in exclude[i]:
					conc_calculated_all[n][x-1] = None
					anisos[n][x-1] = None
	for i in range(len(conc_calculated_all)):
		conc_calculated_all[i] = [x for x in conc_calculated_all[i] if x!=None]
	for i in range(len(anisos)):
		anisos[i] = [x for x in anisos[i] if x!=None]
	#remove empty lists
	conc_calculated_all = [x for x in conc_calculated_all if x!=[]]
	anisos = [x for x in anisos if x!=[]]

	return conc_calculated_all, anisos

def polarization_format(polarization, concentrations, dilution_factors, titrations, samples, dupe, exclude):
	holder = []
	polarizationavg = []
	
	if dupe == True:#if side-by-side duplicates, average the polarizations
		for a in range(len(polarization)):
			if a%2 == 0:
				for b in range(len(polarization[a])):
					holder.append((polarization[a][b]+polarization[a+1][b])/2.0)
				polarizationavg.append(holder)
				holder = []
	else:
		polarizationavg = polarization

	polars = []
	for n in range(len(polarizationavg)):
		polars.append([])
	for i in range(len(titrations)):#list
		for n in range(len(samples[i])):#list of lists
			for x in range(titrations[i]):#get number of titrations to add
				polars[samples[i][n]-1].append(polarizationavg[samples[i][n]-1][x])

	#calculates titration concentrations based on max conc, dilution factor, and number of titrations
	conc_calculated = []
	conc_calculated_all = []
	for n in range(len(polars)):
		conc_calculated_all.append([])
	for n in range(len(concentrations)):
		for i in range(titrations[n]):
			holder.append(float(concentrations[n])/(float(dilution_factors[n])**(i)))
		conc_calculated.append(holder)
		holder = []
	for i in range(len(concentrations)):#list
		for n in range(len(samples[i])):#list of lists
			conc_calculated_all[samples[i][n]-1] = [x for x in conc_calculated[i]]
	#deal with excluded points by changing them to None and then taking them out
	for i in range(len(exclude)):
		sampleind = [x-1 for x in samples[i]]
		if exclude[i] != [None]:
			for n in sampleind:
				for x in exclude[i]:
					conc_calculated_all[n][x-1] = None
					polars[n][x-1] = None
	for i in range(len(conc_calculated_all)):
		conc_calculated_all[i] = [x for x in conc_calculated_all[i] if x!=None]
	for i in range(len(polars)):
		polars[i] = [x for x in polars[i] if x!=None]
	#remove empty lists
	conc_calculated_all = [x for x in conc_calculated_all if x!=[]]
	polars = [x for x in polars if x!=[]]

	return conc_calculated_all, polars

#writes a new excel sheet with concentrations and anisotropy values for each sample. also includes sample labels
def data_write(concentrations, anisos, labels, filepath_new):
	wb = xlwt.Workbook()
	ws = wb.add_sheet("data")
	colcounter = 0
	for n in range(len(concentrations)):
		ws.write(0, colcounter, "Concentration")
		ws.write(0, colcounter+1, labels[n])
		for i in range(len(concentrations[n])):
			ws.write(i+1, colcounter, concentrations[n][i])
			ws.write(i+1, colcounter+1, anisos[n][i])
		colcounter+=2

	wb.save(filepath_new)

#function for reading a sheet that has concentration and anisotropy/fraction bound
def data_read(file):
	wb = xlrd.open_workbook(file)
	sheet = wb.sheet_by_index(0)
	concentrations = []
	anisos = []
	holder = []
	holder2 = []

	for n in range(sheet.ncols):
		if n%2 == 0:
			for i in range(sheet.nrows-1):
				holder.append((sheet.cell_value(i+1, n)))
				holder2.append((sheet.cell_value(i+1, n+1)))
			#these remove empty cells that show up as u'' (a string)
			holder = [float(x) for x in holder if isinstance(x, float) == True]
			holder2 = [float(x) for x in holder2 if isinstance(x, float) == True]
			concentrations.append(holder)
			anisos.append(holder2)
			holder = []
			holder2 = []

	return concentrations, anisos


