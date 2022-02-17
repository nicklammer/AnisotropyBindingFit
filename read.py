#script that can read FP plate excel sheet, calculate anisotropy, and reorganize data to line up with protein concentrations
#this works for data formatted in a 384-well format from a clariostar instrument. Rows A-P, columns 1-24
import pandas as pd
import openpyxl
import numpy as np

def excel_open_aniso(file_raw, rc, wells):#get specified parallel and perpendicular data
	dfsheet = pd.read_excel(file_raw, names=range(0,25))
	holder=[]
	holder2=[]
	for i in range(len(dfsheet[1])):#look at second column in sheet
		if type(dfsheet[1][i]) == str and 'parallel' in dfsheet[1][i]:#if parallel header found
			for r in range(2,18):#look to the next 16 rows
				holder.append(dfsheet.iloc[i+r])#append each row to holder list
			dfpara = pd.DataFrame(data=holder, columns=range(0,25)).set_index(0)#make a dataframe for parallel data, set index to be A-P
			holder=[]
		elif type(dfsheet[1][i]) == str and 'perpendicular' in dfsheet[1][i]:#all same as parallel above
			for r in range(2,18):
				holder.append(dfsheet.iloc[i+r])
			dfperp = pd.DataFrame(data=holder, columns=range(0,25)).set_index(0)
			holder=[]
	parallel=[]
	perpendicular=[]
	holder_para=[]
	holder_perp=[]
	for i in range(len(rc)):#extract parallel perpendicular data and put into lists
		for x in rc[i]:
			if x.isalpha()==True:#for titrations done in rows 
				for n in range(int(wells[i][0])+1, int(wells[i][1])+2):#get value from chosen wells in row. idk why i needed to add 1 and 2, some key error
					holder_para.append(dfpara.at[x,n])
					holder_perp.append(dfperp.at[x,n])
				holder.append(holder_para)
				holder2.append(holder_perp)
				holder_para=[]
				holder_perp=[]
			elif x.isdigit()==True:#for titrations done in columns
				for n in range(wells[i][0], wells[i][1]+1):#get value from chosen wells in column
					holder_para.append(dfpara.iat[n,int(x)-1])
					holder_perp.append(dfperp.iat[n,int(x)-1])
				holder.append(holder_para)
				holder2.append(holder_perp)
				holder_para=[]
				holder_perp=[]
		parallel.append(holder)
		perpendicular.append(holder2)
		holder=[]
		holder2=[]
	return parallel, perpendicular

def excel_open_polar(file_raw, rc, wells):#get specified polarization data
	dfsheet = pd.read_excel(file_raw, names=range(0,25))
	holder=[]
	for i in range(len(dfsheet[1])):#look at second column in sheet
		if type(dfsheet[1][i]) == str and dfsheet[1][i].find('Polarization') == 0:#if polarization header found. different because polarization found in multiple places
			for r in range(2,18):#look to the next 16 rows
				holder.append(dfsheet.iloc[i+r])#append each row to holder list
			dfpolar = pd.DataFrame(data=holder, columns=range(0,25)).set_index(0)#make a dataframe for polarization data, set index to be A-P
			holder=[]
	polar=[]
	holder_polar=[]
	for i in range(len(rc)):#extract polarization data and put into lists
		for x in rc[i]:
			if x.isalpha()==True:#for titrations done in rows 
				for n in range(int(wells[i][0])+1, int(wells[i][1])+2):#get value from chosen wells in row
					holder_polar.append(dfpolar.at[x,n])
				holder.append(holder_polar)
				holder_polar=[]
			elif x.isdigit()==True:#for titrations done in columns
				for n in range(wells[i][0], wells[i][1]+1):#get value from chosen wells in column
					holder_polar.append(dfpolar.iat[n,int(x)-1])
				holder.append(holder_polar)
				holder_polar=[]
		polar.append(holder)
		holder=[]
	return polar

#create new lists with all data in order and calculates anisotropy
def format_aniso(parallel, perpendicular, concentrations, dilution_factors, titrations, ligand, labels, dupe, exclude):
	parallel_clean=[]
	perpendicular_clean=[]
	conc_calculated=[]
	ligand_clean=[]
	labels_clean=[]
	exclude_clean=[]
	holder=[]
	for i in range(len(parallel)):#clean up lists by taking samples out of their smaller sets
		for n in range(len(parallel[i])):
			parallel_clean.append(parallel[i][n])
			perpendicular_clean.append(perpendicular[i][n])
			for t in range(titrations[i]):#calculate list of concentrations based on starting conc, dilution factor, and number of titrations
				holder.append(float(concentrations[i])/(float(dilution_factors[i])**(t)))
			conc_calculated.append(holder)
			holder=[]
			ligand_clean.append(ligand[i][n])
			labels_clean.append(labels[i][n])
			exclude_clean.append(exclude[i])
	FA = []
	FAavg = []
	for a in range(len(parallel_clean)):#calculate anisotropy from parallel and perpendicular lists
		holder = []
		for b in range(len(parallel_clean[a])):
			holder.append(((parallel_clean[a][b]-perpendicular_clean[a][b])/(parallel_clean[a][b]+2*perpendicular_clean[a][b])))
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
	#change excluded well to None and remove all Nones
	for i in range(len(exclude_clean)):
		if exclude_clean[i] != [None]:#only look if excluded wells were given
			for x in exclude_clean[i]:#list of excluded wells per sample
				conc_calculated[i][x] = None#change values in both lists so order matches up
				FAavg[i][x] = None
	for i in range(len(conc_calculated)):#remove None values
		conc_calculated[i] = [x for x in conc_calculated[i] if x!=None]
	for i in range(len(FAavg)):
		FAavg[i] = [x for x in FAavg[i] if x!=None]
	return conc_calculated, FAavg, ligand_clean, labels_clean
#create new lists with all data in order for polarization
def format_polar(polar, concentrations, dilution_factors, titrations, ligand, labels, dupe, exclude):
	polar_clean=[]
	conc_calculated=[]
	ligand_clean=[]
	labels_clean=[]
	exclude_clean=[]
	holder=[]
	for i in range(len(polar)):#clean up lists by taking samples out of their smaller sets
		for n in range(len(polar[i])):
			polar_clean.append(polar[i][n])
			for t in range(titrations[i]):#calculate lsit of concentrations based on starting conc, dilution factor, and number of titrations
				holder.append(float(concentrations[i])/(float(dilution_factors[i])**(t)))
			conc_calculated.append(holder)
			holder=[]
			ligand_clean.append(ligand[i][n])
			labels_clean.append(labels[i][n])
		exclude_clean.append(exclude[i])
			
	polar_clean_avg=[]
	if dupe == True:#if side-by-side duplicates, average the polarizations
		for a in range(len(polar_clean)):
			if a%2 == 0:
				for b in range(len(polar_clean[a])):
					holder.append((polar_clean[a][b]+polar_clean[a+1][b])/2.0)
				polar_clean_avg.append(holder)
				holder = []
	else:
		polar_clean_avg = polar_clean
	#change excluded well to None and remove all Nones
	for i in range(len(exclude_clean)):
		if exclude_clean[i] != [None]:#only look if excluded wells were given
			for x in exclude_clean[i]:#list of excluded wells per sample
				conc_calculated[i][x] = None#change values in both lists so order matches up
				polar_clean_avg[i][x] = None
	for i in range(len(conc_calculated)):#remove None values
		conc_calculated[i] = [x for x in conc_calculated[i] if x!=None]
	for i in range(len(polar_clean_avg)):
		polar_clean_avg[i] = [x for x in polar_clean_avg[i] if x!=None]

	return conc_calculated, polar_clean_avg, ligand_clean, labels_clean

#writes a new excel sheet with concentrations and anisotropy values for each sample. also includes sample labels
def data_write(concentrations, anisos, labels, filepath_new):
	headers=[]
	pairs=[]
	for i in range(len(labels)):
		headers.append('Concentration')
		headers.append(labels[i])
	for i in range(len(concentrations)):
		pairs.append(concentrations[i])
		pairs.append(anisos[i])
	dfdata = pd.DataFrame(data=pairs).transpose()#i want the data in 2 columns per sample
	dfdata.to_excel(filepath_new,engine='openpyxl',index=False,header=headers)

#function for reading a sheet that has concentration and some y data
def data_read(file):
	dfopen = pd.read_excel(file, header=None)
	xdata=[]
	ydata=[]
	labels=[]
	xholder=[]
	yholder=[]
	for i in range(len(dfopen.columns)):
		if i%2 == 0:#do pairs of columns
			for n in range(len(dfopen[i])):
				if n != 0: #ignore first row of headers
					if np.isnan(float(dfopen.iat[n,i])) == False:
						if np.isnan(float(dfopen.iat[n,i+1])) == False:
							xholder.append(float(dfopen.iat[n,i]))
							yholder.append(float(dfopen.iat[n,i+1]))
			labels.append(dfopen.iat[0,i+1])#take labels in first row
			xdata.append(xholder)
			ydata.append(yholder)
			xholder=[]
			yholder=[]

	return xdata, ydata, labels