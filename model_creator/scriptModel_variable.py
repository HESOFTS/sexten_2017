#! /usr/bin/env python
import gammalib
import sys

# =========================================== #
# Create a model container filled with models #
# =========================================== #

def numdiv(num):
	#divide number into number and power 
	numlist =("%.5e" %num).split('e')
	numlist[1]="1e"+numlist[1]
	return numlist

def EnConv(energy, unit):
	# divide energy 
	# 50.0*GeV ---> 50000.0 , if in MeV
	listEnergy = [0.0,0.0]
	
	if (unit == "MeV"):
		listEnergy[0] = gammalib.GEnergy(float(energy.split('*')[0]),energy.split('*')[1]).MeV()
		listEnergy[1] = "1.0" 
	elif (unit == "GeV"):
		listEnergy[0] = gammalib.GEnergy(float(energy.split('*')[0]),energy.split('*')[1]).GeV()
		listEnergy[1] = "1e3" 
	elif (unit == "TeV"):
		listEnergy[0] = gammalib.GEnergy(float(energy.split('*')[0]),energy.split('*')[1]).TeV()
		listEnergy[1] = "1e6" 
	else:
		print("Wrong Energy conversion! CHECK value "+energy)            
   
	return listEnergy


def sourceDef(info):
	# --------------------
	# CREATE SOURCE BRANCH
	# --------------------
	# spectral and spatial components will be appended to this branch
	# 1 branch for each source in the XML model

	srcname = info[0]
	modelname = info[1]     #extract model name for SOURCE
	ts = info[2]
	#if ver != '': print('--------------------------------')

	
	pointList = ['Point']
	extendedList = ['RadDisk','RadGauss','RadShell', 'EllDisk', 'EllGauss']
	diffuseList = ['DiffIso','DiffMap','DiffMapCube']
	bkg_radial = ['BkgGauss', 'Profile', 'Polynom']
	bkg_irf = ['CTAIrf'] 
	bkg_cube = ['CTACube']

	if (modelname in pointList):
		source_txt = 'source type="PointSource"  name="'+str(srcname)+'"'
	elif (modelname in extendedList):
		source_txt = 'source type="ExtendedSource"  name="'+str(srcname)+'"'
	elif (modelname in diffuseList):
		source_txt = 'source type="DiffuseSource"  name="'+str(srcname)+'"'
	elif (modelname in bkg_radial):
		source_txt = 'source name="Background"  type="RadialAcceptance" instrument="CTA"'
	elif (modelname in bkg_irf):
		source_txt = 'source name="Background" type="CTAIrfBackground" instrument="CTA"'
	elif (modelname in bkg_cube):
		source_txt = 'source name="Background" type="CTACubeBackground" instrument="CTA"'
	else:        
		print("Mispelled spatial model, open the .txt and check it!")
		sys.exit() 

	if (ts == "1"):
		source_txt = source_txt + ' tscalc="1"'

	source_branch = gammalib.GXmlElement(source_txt)           
	if (srcname[0:2] == "BKG"):
		if ver != '': print("-----------background-----------")
		if ver != '': print('The source ' + srcname + ' is a ' + modelname)    

		#create SPECTRAL model
		spectral = specFun(info[8:])        #string        
		source_branch.append(spectral)    
	else:       
		if ver != '': print("------source: " + srcname + "-------")
		if ver != '': print('The source ' + srcname + ' is a ' + modelname)    

		#create SPECTRAL model
		spectral = specFun(info[8:])        #string        
		source_branch.append(spectral)    

		if (modelname != 'CTAIrf' and modelname != 'CTACube'):
			#create SPATIAL model    
			spatial = spatFun(info[1:])
			source_branch.append(spatial)

		#check if the last item is a file fits for the TEMPORAL evolution 
		if (info[-1][-4:] == 'fits'):
			#create TEMPORAL model (use last two item in list, NORMALIZATION and FITS file)
			temporal = temporalFun(info[-2:])
			source_branch.append(temporal)

	if (ts == "1"):
		if ver != '': print("TS calculation: yes")
		#source_txt=source_txt+'  tscalc="1"'
	else:
		if ver != '': print("TS calculation: no")

	return source_branch

def spatFun(inSpat):
	# --------------------
	# CREATE SPATIAL MODEL
	# --------------------

	#get model name
	SpatModel = inSpat[0] 

	# set RA and DEC, common for all the spatial models
	ra = inSpat[2]
	dec = inSpat[3]

	# set text to be put in the xml file
	ra_text='parameter scale="1.0"  name="RA"  min="-360"   max="360"  free="0" value="'+ra+'"'
	dec_text='parameter scale="1.0"  name="DEC"  min="-90"   max="90"  free="0" value="'+dec+'"'

	if (SpatModel == 'Point'):
		spatial = gammalib.GXmlElement('spatialModel type="SkyDirFunction"') #compatibility with Fermi/LAT
		spatial.append(ra_text)
		spatial.append(dec_text)

	elif (SpatModel == 'RadDisk'):
		spatial = gammalib.GXmlElement('spatialModel type="DiskFunction"')
		spatial.append(ra_text)
		spatial.append(dec_text)
		radius = inSpat[4]
		radius_text = 'name="Radius" scale="1.0"  min="0.01" max="10"  free="0"   value="' + radius +'"'
		spatial.append(radius_text)

	elif (SpatModel == 'RadGauss'):
		spatial = gammalib.GXmlElement('spatialModel type="GaussFunction"')
		spatial.append(ra_text)
		spatial.append(dec_text)
		sig = inSpat[4]
		sig_text = 'name="Sigma" scale="1.0"  min="0.01" max="10"  free="0"   value="' + sig +'"'
		spatial.append(sig_text)

	elif (SpatModel == 'RadShell'):
		spatial = gammalib.GXmlElement('spatialModel type="ShellFunction"')
		spatial.append(ra_text)
		spatial.append(dec_text)
		radius = inSpat[4]
		width  = inSpat[5]
		radius_text = 'name="Radius" scale="1.0"  min="0.01" max="10"  free="0"  value="' + radius +'"'
		width_text  = 'name="Width"  scale="1.0"  min="0.01" max="10"  free="0"  value="' + width + '"'
		spatial.append(radius_text)
		spatial.append(width_text)

	elif (SpatModel == 'EllDisk'):
		spatial = gammalib.GXmlElement('spatialModel type="EllipticalDisk"')
		spatial.append(ra_text)
		spatial.append(dec_text)
		PA = inSpat[4]
		minr  = inSpat[5]
		maxr  = inSpat[6]
		PA_text   = 'name="PA"           scale="1.0"  min="-360"   max="360" free="0"  value="' + PA +'"'
		minr_text = 'name="MinorRadius"  scale="1.0"  min="0.001"  max="10"  free="0"  value="' + minr + '"'
		maxr_text = 'name="MajorRadius"  scale="1.0"  min="0.001"  max="10"  free="0"  value="' + maxr + '"'
		spatial.append(PA_text)
		spatial.append(minr_text)
		spatial.append(maxr_text)

	elif (SpatModel == 'EllGauss'):
		spatial = gammalib.GXmlElement('spatialModel type="EllipticalGauss"')
		spatial.append(ra_text)
		spatial.append(dec_text)
		PA = inSpat[4]
		minr  = inSpat[5]
		maxr  = inSpat[6]
		PA_text   = 'name="PA"           scale="1.0"  min="-360"   max="360" free="0"  value="' + PA +'"'
		minr_text = 'name="MinorRadius"  scale="1.0"  min="0.001"  max="10"  free="0"  value="' + minr + '"'
		maxr_text = 'name="MajorRadius"  scale="1.0"  min="0.001"  max="10"  free="0"  value="' + maxr + '"'
		spatial.append(PA_text)
		spatial.append(minr_text)
		spatial.append(maxr_text)

	elif (SpatModel == 'DiffIso'):
		spatial = gammalib.GXmlElement('spatialModel type="DiffuseSource"')
		value = inSpat[4]
		value_text = 'name="Value" scale="1" min="1"  max="1" free="0" value="' + value +'"'        
		spatial.append(value_text)

	elif (SpatModel == 'DiffMap'):
		spatial = gammalib.GXmlElement('spatialModel type="DiffuseSource" file="map.fits"')
		value = inSpat[4]
		value_text = 'name="Prefactor" scale="1" min="0.001"  max="1000.0" free="0" value="' + value +'"'
		spatial.append(value_text)

	elif (SpatModel == 'DiffMapCube'):
		spatial = gammalib.GXmlElement('spatialModel type="MapCubeFunction" file="map_cube.fits"')
		value = inSpat[4]
		value_text = 'name="Normalization" scale="1" min="0.001"  max="1000.0" free="0" value="' + value +'"'
		spatial.append(value_text)   


		#---------- Here starts background spatial models

	elif (SpatModel == 'BkgGauss'):
		spatial = gammalib.GXmlElement('radialModel type="Gaussian"')
		sig = inSpat[2]
		sig_text = 'name="Sigma" scale="1.0"  min="0.01" max="10.0"  free="0"   value="' + sig +'"'
		spatial.append(sig_text)
			 
	elif (SpatModel == 'Profile'):
		spatial = gammalib.GXmlElement('radialModel type="Profile"')
		width = inSpat[2]
		core = inSpat[3]
		tail = inSpat[4]
		width_text = 'name="Width" scale="1.0"  min="0.01" max="10000.0"  free="0"   value="' + width +'"'
		core_text = 'name="Core" scale="1.0"  min="0.01" max="10000.0"  free="0"   value="' + core +'"'
		tail_text = 'name="Tail" scale="1.0"  min="0.01" max="10000.0"  free="0"   value="' + tail +'"'

		spatial.append(width_text)
		spatial.append(core_text)
		spatial.append(tail_text)

	elif (SpatModel == 'Polynom'):
		spatial = gammalib.GXmlElement('radialModel type="Polynom"')
		coef = inSpat[2]
		coef = coef.split("_")
		for i in range(0,len(coef)):
			name_coef = 'Coeff' + str(i)
			coef_text = 'name="' + name_coef +'" scale="1.0" value="'+coef[i]+'"  min="-10.0" max="10.0" free="0"'
			spatial.append(coef_text)
	
	else:
		print("Wrong input model")
		sys.exit()
	return spatial

def specFun(inSpec):
	# --------------------
	# CREATE SPECTRAL MODEL
	# --------------------
	# CHOOSE BETWEEN = "PowerLaw2", "PowerLaw", "NodeFunction", "LogParabola", "Gaussian", "FileFunction", "ExpCutoff", "ConstantValue", "BrokenPowerLaw"

	#set spectral model name
	SpecModel = inSpec[0]
	
	if (SpecModel == 'CONST'):
		#CONSTANT MODEL
		if ver != '': print('Spectral model: ' + SpecModel)
		norm = float(inSpec[1])        
		norm_text='parameter scale="'+numdiv(pref)[1]+'"  name="Normalization"  min="1e-7"   max="1000"  free="1" value="'+numdiv(pref)[0]+'"'
		spectral = gammalib.GXmlElement('spectrum type="ConstantValue"')                
		spectral.append(norm_text)

	elif (SpecModel == 'FUNC'):
		# FILE FUNCTION
		if ver != '': print('Spectral model: ' + SpecModel)
		norm = float(inSpec[1])
		filepath = inSpec[2]
		norm_text='parameter scale="'+numdiv(norm)[1]+'"  name="Normalization"  min="1e-7"   max="1000"  free="1" value="'+numdiv(norm)[0]+'"'
		spectral = gammalib.GXmlElement('spectrum type="FileFunction"  file="'+filepath+'"')                
		spectral.append(norm_text)
	
	elif (SpecModel == 'NODE'):
		if ver != '': print(SpecModel)
		n_param = int(inSpec[1]) #number of parameters

		if n_param % 2 != 0:
			if ver != '': print("Wrong number of parameters in NODE SPECTRAL MODEL")
			sys.exit()            

		spectral = gammalib.GXmlElement('spectrum type="NodeFunction"')

		values = []
		for n in range(2, n_param + 2, 2):
			if ver != '': print(inSpec[n])
			if ver != '': print(type(inSpec[n]))
			values.append(EnConv(inSpec[n], "MeV")) #energy
			values.append(inSpec[n+1])				#intensity

		val_x = values[0::2] #select only even characters
		val_y = values[1::2] #select only odd characters
		if ver != '': print(val_x)
		points = [(val_x[i],val_y[i]) for i in range(0, len(val_x))] #making list of points
		pointss = sorted(points, key=lambda k: k[1])  #sort points by energy
		if ver != '': print(pointss)
		for n in range(0, len(pointss)):	
			energy_text = 'parameter scale="'+str(pointss[n][0][1])+'"   name="Energy"    min="0.1"   max="1.0e20" free="0"  value="'+str(pointss[n][0][0])+'"'
			intens_text = 'parameter scale="1e-07" name="Intensity" min="1e-07" max="1000.0" free="1" value="'+pointss[n][1]+'"'
			node = spectral.append('node')
			node.append(energy_text)
			node.append(intens_text)

	elif (SpecModel == 'PL'):
		#POWER LAW MODEL
		if ver != '': print('Spectral model: '+SpecModel)
		pref = float(inSpec[1])
		index = inSpec[2]
		PivotEnergy = EnConv(inSpec[3], "MeV") #convert the energy in MeV

		pref_text='parameter scale="'+numdiv(pref)[1]+'"  name="Prefactor"  min="1e-7"   max="1000"  free="1" value="'+numdiv(pref)[0]+'"'
		index_text='parameter scale="-1.0"  name="Index"  min="0.0"   max="+10.0"  free="1" value="'+index+'"'
		energy_text='parameter scale="'+str(PivotEnergy[1])+'"  name="Scale"  min="0.0"   max="+10000000.0"  free="0" value="'+str(PivotEnergy[0])+'"'

		spectral = gammalib.GXmlElement('spectrum type="PowerLaw"')
		spectral.append(pref_text)
		spectral.append(index_text)
		spectral.append(energy_text)

	elif (SpecModel == 'PL2'):
		#POWER LAW 2 MODEL
		if ver != '': print('Spectral model: '+SpecModel)
		pref = float(inSpec[1])
		index = inSpec[2]
		MinEnergy = EnConv(inSpec[3], "MeV") #convert the energy in MeV
		MaxEnergy = EnConv(inSpec[4], "MeV") #convert the energy in MeV
		if ver != '': print(MaxEnergy)

		pref_text='parameter scale="'+numdiv(pref)[1]+'"  name="Integral"  min="1e-7"   max="1000"  free="1" value="'+numdiv(pref)[0]+'"'
		index_text='parameter scale="-1.0"  name="Index"  min="0.0"   max="+10.0"  free="1" value="'+index+'"'
		min_energy_text='parameter scale="'+str(MinEnergy[1])+'"  name="LowerLimit"  min="10.0"   max="+100000000.0"  free="0" value="'+str(MinEnergy[0])+'"'
		max_energy_text='parameter scale="'+str(MaxEnergy[1])+'"  name="UpperLimit"  min="10.0"   max="+100000000.0"  free="0" value="'+str(MaxEnergy[0])+'"'

		spectral = gammalib.GXmlElement('spectrum type="PowerLaw2"')
		spectral.append(pref_text)
		spectral.append(index_text)
		spectral.append(min_energy_text)
		spectral.append(max_energy_text)

	elif (SpecModel == 'BRPL'):
		# BrokenPowerLaw MODEL
		if ver != '': print('Spectral model: ' + SpecModel)
		pref = float(inSpec[1])
		index1 = inSpec[2]                      #must be negative
		CutEnergy = EnConv(inSpec[3],"GeV")     #convert the energy in GeV
		index2 = inSpec[4]                      # must be negative

		pref_text='parameter scale="'+numdiv(pref)[1]+'"  name="Prefactor"  min="1e-7"   max="1000"  free="1" value="'+numdiv(pref)[0]+'"'
		index1_text='parameter scale="-1.0"  name="Index1"  min="0.01"   max="+10.0"  free="1" value="'+index1+'"'
		cut_energy_text='parameter scale="'+str(CutEnergy[1])+'"  name="BreakValue"  min="10.0"   max="+100000000.0"  free="1" value="'+str(CutEnergy[0])+'"'
		index2_text='parameter scale="-1.0"  name="Index2"  min="0.01"   max="+10.0"  free="1" value="'+index2+'"'

		spectral = gammalib.GXmlElement('spectrum type="BrokenPowerLaw"')
		spectral.append(pref_text)
		spectral.append(index1_text)
		spectral.append(cut_energy_text)
		spectral.append(index2_text)

	elif (SpecModel == 'EXPL'):
		#Exponential CUT OFF POWER LAW MODEL
		if ver != '': print('Spectral model: ' + SpecModel)
		pref = float(inSpec[1])
		index = inSpec[2]
		PivotEnergy = EnConv(inSpec[3], "MeV") #convert the energy in MeV
		CutEnergy = EnConv(inSpec[4], "MeV") #convert the energy in MeV
		
		pref_text='parameter scale="'+numdiv(pref)[1]+'"  name="Prefactor"  min="1e-7"   max="1000"  free="1" value="'+numdiv(pref)[0]+'"'
		index_text='parameter scale="-1.0"  name="Index"  min="0.0"   max="+10.0"  free="1" value="'+index+'"'
		cut_energy_text='parameter scale="1.0"  name="Cutoff"  min="0.01"   max="100000000.0"  free="1" value="'+str(CutEnergy[0])+'"'
		piv_energy_text='parameter scale="1.0"  name="Scale"  min="0.01"   max="100000000.0"  free="0" value="'+str(PivotEnergy[0])+'"'

		spectral = gammalib.GXmlElement('spectrum type="ExpCutoff"')
		spectral.append(pref_text)
		spectral.append(index_text)
		spectral.append(cut_energy_text)
		spectral.append(piv_energy_text)

	elif (SpecModel == 'SEPL'):
		#SUPER EXPONENTIALY CUY-OFF POWER LAW
		if ver != '': print('Spectral model: ' + SpecModel)
		pref = float(inSpec[1])
		index1 = inSpec[2]
		index2 = inSpec[3]
		PivotEnergy = EnConv(inSpec[4], "MeV") #convert the energy in MeV 
		CutEnergy = EnConv(inSpec[5], "MeV") #convert the energy in MeV   

		pref_text='parameter scale="'+numdiv(pref)[1]+'"  name="Prefactor"  min="1e-7"   max="1000"  free="1" value="'+numdiv(pref)[0]+'"'
		index1_text='parameter scale="-1.0"  name="Index1"  min="0.0"   max="+10.0"  free="1" value="'+index1+'"'
		index2_text='parameter scale="1.0"   name="Index2"  min="0.1"   max="10.0"   free="1" value="'+index2+'"'
		cut_energy_text='parameter scale="'+str(CutEnergy[1])+'"  name="Cutoff"  min="0.01"   max="100000000.0"  free="1" value="'+str(CutEnergy[0])+'"'
		piv_energy_text='parameter scale="'+str(PivotEnergy[1])+'"  name="Scale"   min="0.01"   max="100000000.0"  free="0" value="'+str(PivotEnergy[0])+'"'


		spectral = gammalib.GXmlElement('spectrum type="PLSuperExpCutoff"')
		spectral.append(pref_text)
		spectral.append(index1_text)
		spectral.append(index2_text)
		spectral.append(cut_energy_text)
		spectral.append(piv_energy_text)

	elif (SpecModel == 'LOGPAR'):
		if ver != '': print('Spectral model: ' + SpecModel)
		#LOG PARABOLA
		pref = float(inSpec[1])
		index = inSpec[2]
		curv = inSpec[3]
		E_scale = EnConv(inSpec[4], "MeV") #convert the energy in MeV

		pref_text='parameter scale="'+numdiv(pref)[1]+'"  name="Prefactor"  min="1e-7"   max="1000"  free="1" value="'+numdiv(pref)[0]+'"'
		index_text='parameter scale="-1.0"  name="Index"  min="0.0"   max="+10.0"  free="1" value="'+index+'"'
		curv_text='parameter scale="-1.0"  name="Curvature"  min="-5.0"   max="+5.0"  free="1" value="'+ curv +'"'
		E_scale_text='parameter scale="1.0"  name="Scale"  min="0.01"   max="100000000.0"  free="0" value="'+str(E_scale[0])+'"'
		
		spectral = gammalib.GXmlElement('spectrum type="LogParabola"')

		spectral.append(pref_text)
		spectral.append(index_text)
		spectral.append(curv_text)
		spectral.append(E_scale_text)

	elif (SpecModel == 'GAUSS'):
		if ver != '': print('Spectral model: ' + SpecModel)
		#GAUSSIAN FUNCTION
		norm = float(inSpec[1])
		mean = EnConv(inSpec[2],"GeV")
		sigma = inSpec[3]

		norm_text  = 'parameter scale="'+numdiv(norm)[1]+'"  name="Normalization"  min="1e-7"   max="1000.0"  free="1" value="'+numdiv(norm)[0]+'"'
		mean_text  = 'parameter scale="1e6"   name="Mean"    value="'+str(mean[0])+'"'
		sigma_text = 'parameter scale="1e6"   name="Sigma"     min="0.01"  max="100.0"  free="1"  value="'+sigma+'"'

		spectral = gammalib.GXmlElement('spectrum type="Gaussian"')
		spectral.append(norm_text)
		spectral.append(mean_text)
		spectral.append(sigma_text)

	else:
	   print("Wrong Spectral model!!! CHECK MODEL NAME!!!")
	   sys.exit()

	return spectral
	  
def temporalFun(inTime):
	# --------------------
	# CREATE TEMPORAL MODEL
	# --------------------

	#get model name (TDB)
	#SpatModel = inTime[0] 
	SpatModel = "Light"
	
	norm = float(inTime[0])
	fitspath = inTime[1]

	# set text to be put in the xml file

	norm_text ='parameter scale="'+numdiv(norm)[1]+'"  name="Normalization"  min="0.0"   max="1000.0"  free="0" value="'+numdiv(norm)[0]+'"'

	if (SpatModel == 'Light'):
		temporal = gammalib.GXmlElement('temporal   type="LightCurve"   file="'+fitspath+'"')
		temporal.append(gammalib.GXmlElement(norm_text))
	else:
		print("The only supported temporal model is the one with Normalization and a fits file")
		sys.exit()

	return temporal

# ================= #
# Show XML document #
# ================= #
def show_xml(xml):
	"""
	Show XML document on the screen.
	"""
	# Allocate string URL
	url = gammalib.GUrlString()
	
	# Write XML document in URL
	xml.write(url)
	
	# Print URL buffer
	if ver != '': print(url.string())
	
	# Return
	return

# ======================== #
# Main routine entry point #
# ======================== #
if __name__ == '__main__':

	nomefile = str(sys.argv[1])
	#f = open(nomefile, 'r')    

	# Allocate XML document
	xml = gammalib.GXml()

	# main branch    
	sourcelibrary = xml.append('source_library title="source library"')

	# if argv has verbose attribute, set verbose on

	global ver

	if len(sys.argv) == 3: 
		ver = 'yes'
	else: 
		ver = ''




	# read lines

	with open(nomefile) as openfile:
		for line in openfile:
			inputs = line.split()
			if len(inputs) != 0:
				if line[0] != '#':
					sourcelibrary.append(sourceDef(inputs))
	if ver != '': print('--------------------------------')
	
	#SHOW XML FILE    
	show_xml(xml)

	#print(models)
	# Save the XML document into a file
	name_fil = sys.argv[1].split('.')

	xml.save(name_fil[0]+'.xml')