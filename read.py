#script that can read FP plate excel sheet, calculate anisotropy, and reorganize data to line up with protein concentrations
#also written for use with config file
import config
import plot
import xlrd
import xlwt
from xlutils.copy import copy

file_raw = config.file_raw
file_formatted = config.file_formatted
concentration = config.concentration_start
dilution_factor = config.dilution_factor
dupe = config.duplicates
labels = config.labels

def excel_open_rowsamples(file_raw, titrations, start_col):
	holder = []
	parallel = []
	perpendicular = []
	FA = []

	wb = xlrd.open_workbook(file_raw)
	sheet_raw = wb.sheet_by_index(0)

	for row in range(sheet_raw.nrows):
		if str(sheet_raw.cell_value(row,1)) == "1. Raw Data (parallel)":
			for r in range(2,18):
				if sheet_raw.cell_value(row+r,start_col) > 0 and isinstance(sheet_raw.cell_value(row+r,start_col), basestring) == False:
					for c in range (start_col,start_col+titrations):
						if sheet_raw.cell_value(row+r,c) > 0 and isinstance(sheet_raw.cell_value(row+r,c), basestring) == False:
							holder.append(sheet_raw.cell_value(row+r,c))
					parallel.append(holder)
					holder = []

		elif str(sheet_raw.cell_value(row,1)) == "2. Raw Data (perpendicular)":
			for r in range(2,18):
				if sheet_raw.cell_value(row+r,start_col) > 0 and isinstance(sheet_raw.cell_value(row+r,start_col), basestring) == False:
					for c in range (start_col,start_col+titrations):
						if sheet_raw.cell_value(row+r,c) > 0 and isinstance(sheet_raw.cell_value(row+r,c), basestring) == False:
							holder.append(sheet_raw.cell_value(row+r,c))
					perpendicular.append(holder)
					holder = []

	for a in range(len(parallel)):
		for b in range(len(parallel[a])):
			holder.append(((parallel[a][b]-perpendicular[a][b])/(parallel[a][b]+2*perpendicular[a][b])))
		FA.append(holder)
		holder = []

	return FA

def excel_open_colsamples(file_raw, titrations, start_row):
	holder = []
	parallel = []
	perpendicular = []
	FA = []

	wb = xlrd.open_workbook(file_raw)
	sheet_raw = wb.sheet_by_index(0)

	for col in range(sheet_raw.ncols):
		for row in range(sheet_raw.nrows):
			if str(sheet_raw.cell_value(row,col)) == "1. Raw Data (parallel)":
				for c in range (24):
					if sheet_raw.cell_value(row+1+start_row,col+c) > 0 and isinstance(sheet_raw.cell_value(row+1+start_row,col+c), basestring) == False:
						for r in range(start_row+1, start_row+1+titrations):
							if sheet_raw.cell_value(row+r, col+c) > 0 and isinstance(sheet_raw.cell_value(row+r, col+c), basestring) == False:
								holder.append(sheet_raw.cell_value(row+r,col+c))
						parallel.append(holder)
						holder = []		

			elif str(sheet_raw.cell_value(row,col)) == "2. Raw Data (perpendicular)":
				for c in range (24):
					if sheet_raw.cell_value(row+1+start_row,col+c) > 0 and isinstance(sheet_raw.cell_value(row+1+start_row,col+c), basestring) == False:
						for r in range(start_row+1, start_row+1+titrations):
							if sheet_raw.cell_value(row+r, col+c) > 0 and isinstance(sheet_raw.cell_value(row+r, col+c), basestring) == False:
								holder.append(sheet_raw.cell_value(row+r,col+c))
						perpendicular.append(holder)
						holder = []		

	for a in range(len(parallel)):
		for b in range(len(parallel[a])):
			holder.append(((parallel[a][b]-perpendicular[a][b])/(parallel[a][b]+2*perpendicular[a][b])))
		FA.append(holder)
		holder = []

	return FA

def format(concentration, dilution_factor, dupe, FA):
	dilutions = []
	holder = []
	FAavg = []
	combined = []

	for i in range(len(FA[0])):
		dilutions.append(float(concentration)/(float(dilution_factor)**(i)))

	if dupe == 1:
		for a in range(len(FA)):
			if a%2 == 0:
				for b in range(len(FA[a])):
					holder.append((FA[a][b]+FA[a+1][b])/2.0)
				FAavg.append(holder)
				holder = []
		for i in FAavg:
			holder = zip(dilutions, i)
			combined.append(holder)
			holder = []
	elif dupe == 0:
		for i in FA:
			holder = zip(dilutions, i)
			combined.append(holder)
			holder = []
	
	return combined

def data_write(xypairs, labels, filepath_new):
	wb = xlwt.Workbook()
	ws = wb.add_sheet("data")
	rowcounter = 1

	ws.write(0, 0, "Concentration")
	for i in range(len(xypairs[0])):
		ws.write(i+1, 0, xypairs[0][i][0])
	for i in range(len(xypairs)):
		ws.write(0, i+1, labels[i])
		for n in range(len(xypairs[i])):
			ws.write(rowcounter, i+1, xypairs[i][n][1])
			rowcounter += 1
		rowcounter = 1

	wb.save(filepath_new)


