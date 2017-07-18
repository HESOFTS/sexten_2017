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
    #print('--------------------------------')

    
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
    if (srcname == "BKG"):
        print("-----------background-----------")
        print('The source ' + srcname + ' is a ' + modelname)    

        #create SPECTRAL model
        spectral = specFun(info[8:])        #string        
        source_branch.append(spectral)    
    else:       
        print("------source: " + srcname + "-------")
        print('The source ' + srcname + ' is a ' + modelname)    

        #create SPECTRAL model
        spectral = specFun(info[8:])        #string        
        source_branch.append(spectral)    

        #create SPATIAL model    
        spatial = spatFun(info[1:])
        source_branch.append(spatial)

        #check if the last item is a file fits for the TEMPORAL evolution 
        if (info[-1][-4:] == 'fits'):
            #create TEMPORAL model (use last two item in list, NORMALIZATION and FITS file)
            temporal = temporalFun(info[-2:])
            source_branch.append(temporal)

    if (ts == "1"):
        print("TS calculation: yes")
        #source_txt=source_txt+'  tscalc="1"'
    else:
        print("TS calculation: no")

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
        spatial = gammalib.GXmlElement('spatialModel type="SkyDirFunction"')
        spatial.append(gammalib.GXmlElement(ra_text))
        spatial.append(gammalib.GXmlElement(dec_text))

    elif (SpatModel == 'RadDisk'):
        spatial = gammalib.GXmlElement('spatialModel type="DiskFunction"')
        spatial.append(gammalib.GXmlElement(ra_text))
        spatial.append(gammalib.GXmlElement(dec_text))
        radius = inSpat[4]
        radius_text = 'name="Radius" scale="1.0"  min="0.01" max="10"  free="0"   value="' + radius +'"'
        spatial.append(gammalib.GXmlElement(radius_text))

    elif (SpatModel == 'RadGauss'):
        spatial = gammalib.GXmlElement('spatialModel type="GaussFunction"')
        spatial.append(gammalib.GXmlElement(ra_text))
        spatial.append(gammalib.GXmlElement(dec_text))
        sig = inSpat[4]
        sig_text = 'name="Sigma" scale="1.0"  min="0.01" max="10"  free="0"   value="' + sig +'"'
        spatial.append(gammalib.GXmlElement(sig_text))

    elif (SpatModel == 'RadShell'):
        spatial = gammalib.GXmlElement('spatialModel type="ShellFunction"')
        spatial.append(gammalib.GXmlElement(ra_text))
        spatial.append(gammalib.GXmlElement(dec_text))
        radius = inSpat[4]
        width  = inSpat[5]
        radius_text = 'name="Radius" scale="1.0"  min="0.01" max="10"  free="0"  value="' + radius +'"'
        width_text  = 'name="Width"  scale="1.0"  min="0.01" max="10"  free="0"  value="' + width + '"'
        spatial.append(gammalib.GXmlElement(radius_text))
        spatial.append(gammalib.GXmlElement(width_text))

    elif (SpatModel == 'EllDisk'):
        spatial = gammalib.GXmlElement('spatialModel type="EllipticalDisk"')
        spatial.append(gammalib.GXmlElement(ra_text))
        spatial.append(gammalib.GXmlElement(dec_text))
        PA = inSpat[4]
        minr  = inSpat[5]
        maxr  = inSpat[6]
        PA_text   = 'name="PA"           scale="1.0"  min="-360"   max="360" free="0"  value="' + PA +'"'
        minr_text = 'name="MinorRadius"  scale="1.0"  min="0.001"  max="10"  free="0"  value="' + minr + '"'
        maxr_text = 'name="MajorRadius"  scale="1.0"  min="0.001"  max="10"  free="0"  value="' + maxr + '"'
        spatial.append(gammalib.GXmlElement(PA_text))
        spatial.append(gammalib.GXmlElement(minr_text))
        spatial.append(gammalib.GXmlElement(maxr_text))

    elif (SpatModel == 'EllGauss'):
        spatial = gammalib.GXmlElement('spatialModel type="EllipticalGauss"')
        spatial.append(gammalib.GXmlElement(ra_text))
        spatial.append(gammalib.GXmlElement(dec_text))
        PA = inSpat[4]
        minr  = inSpat[5]
        maxr  = inSpat[6]
        PA_text   = 'name="PA"           scale="1.0"  min="-360"   max="360" free="0"  value="' + PA +'"'
        minr_text = 'name="MinorRadius"  scale="1.0"  min="0.001"  max="10"  free="0"  value="' + minr + '"'
        maxr_text = 'name="MajorRadius"  scale="1.0"  min="0.001"  max="10"  free="0"  value="' + maxr + '"'
        spatial.append(gammalib.GXmlElement(PA_text))
        spatial.append(gammalib.GXmlElement(minr_text))
        spatial.append(gammalib.GXmlElement(maxr_text))

    elif (SpatModel == 'DiffIso'):
        spatial = gammalib.GXmlElement('spatialModel type="DiffuseSource"')
        value = inSpat[4]
        value_text = 'name="Value" scale="1" min="1"  max="1" free="0" value="' + value +'"'
    	spatial.append(gammalib.GXmlElement(value_text))

    elif (SpatModel == 'DiffMap'):
        spatial = gammalib.GXmlElement('spatialModel type="DiffuseSource" file="map.fits"')
        value = inSpat[4]
        value_text = 'name="Prefactor" scale="1" min="0.001"  max="1000.0" free="0" value="' + value +'"'
    	spatial.append(gammalib.GXmlElement(value_text))

    elif (SpatModel == 'DiffMapCube'):
        spatial = gammalib.GXmlElement('spatialModel type="MapCubeFunction" file="map_cube.fits"')
        value = inSpat[4]
        value_text = 'name="Normalization" scale="1" min="0.001"  max="1000.0" free="0" value="' + value +'"'
    	spatial.append(gammalib.GXmlElement(value_text))	

    else:
        print("Wrong input model")
        sys.exit()
    return spatial

def specFun(inSpec):
    # --------------------
    # CREATE SPECTRAL MODEL
    # --------------------
    # CHOOSE BETWEEN = "PowerLaw2", "PowerLaw", "NodeFunction", "LogParabola", "Gaussian", "FileFunction", "ExpCutoff", "ConstantValue", "BrokenPowerLaw".
    # "PLSuperExpCutoff" NOT IMPLEMENTED

    #set spectral model name
    SpecModel = inSpec[0]
    
    if (SpecModel == 'CONST'):
        #CONSTANT MODEL
        print(SpecModel)
        norm = float(inSpec[1])        
        norm_text='parameter scale="'+numdiv(pref)[1]+'"  name="Normalization"  min="1e-7"   max="1000"  free="1" value="'+numdiv(pref)[0]+'"'
        spectral = gammalib.GXmlElement('spectrum type="ConstantValue"')                
        normalization = spectral.append(gammalib.GXmlElement(norm_text))
    elif (SpecModel == 'FUNC'):
        # FILE FUNCTION
        print(SpecModel)
        norm = float(inSpec[1])
        filepath = inSpec[2]
        norm_text='parameter scale="'+numdiv(norm)[1]+'"  name="Normalization"  min="1e-7"   max="1000"  free="1" value="'+numdiv(norm)[0]+'"'
        spectral = gammalib.GXmlElement('spectrum type="FileFunction"  file="'+filepath+'"')                
        normalization = spectral.append(gammalib.GXmlElement(norm_text))
    elif (SpecModel == 'NODE'):
        print(SpecModel)
    elif (SpecModel == 'PL'):
        #POWER LAW MODEL
        print('Spectral model: '+SpecModel)
        pref = float(inSpec[1])
        index = inSpec[2]
        PivotEnergy = EnConv(inSpec[3], "MeV") #convert the energy in MeV

        pref_text='parameter scale="'+numdiv(pref)[1]+'"  name="Prefactor"  min="1e-7"   max="1000"  free="1" value="'+numdiv(pref)[0]+'"'
        index_text='parameter scale="-1.0"  name="Index"  min="0.0"   max="+10.0"  free="1" value="'+index+'"'
        energy_text='parameter scale="'+str(PivotEnergy[1])+'"  name="Scale"  min="0.0"   max="+10000000.0"  free="0" value="'+str(PivotEnergy[0])+'"'

        spectral = gammalib.GXmlElement('spectrum type="PowerLaw"')
        prefactor = spectral.append(gammalib.GXmlElement(pref_text))
        indice = spectral.append(gammalib.GXmlElement(index_text))
        energia = spectral.append(gammalib.GXmlElement(energy_text))

    elif (SpecModel == 'PL2'):
        #POWER LAW 2 MODEL
        print('Spectral model: '+SpecModel)
        pref = float(inSpec[1])
        index = inSpec[2]
        MinEnergy = EnConv(inSpec[3], "MeV") #convert the energy in MeV
        MaxEnergy = EnConv(inSpec[4], "MeV") #convert the energy in MeV
        print(MaxEnergy)

        pref_text='parameter scale="'+numdiv(pref)[1]+'"  name="Integral"  min="1e-7"   max="1000"  free="1" value="'+numdiv(pref)[0]+'"'
        index_text='parameter scale="-1.0"  name="Index"  min="0.0"   max="+10.0"  free="1" value="'+index+'"'
        min_energy_text='parameter scale="'+str(MinEnergy[1])+'"  name="LowerLimit"  min="10.0"   max="+100000000.0"  free="0" value="'+str(MinEnergy[0])+'"'
        max_energy_text='parameter scale="'+str(MaxEnergy[1])+'"  name="UpperLimit"  min="10.0"   max="+100000000.0"  free="0" value="'+str(MaxEnergy[0])+'"'

        spectral = gammalib.GXmlElement('spectrum type="PowerLaw2"')
        prefactor = spectral.append(gammalib.GXmlElement(pref_text))
        indice = spectral.append(gammalib.GXmlElement(index_text))
        energia_min = spectral.append(gammalib.GXmlElement(min_energy_text))
        energia_max = spectral.append(gammalib.GXmlElement(max_energy_text))

    elif (SpecModel == 'BRPL'):
        # BrokenPowerLaw MODEL
        print(SpecModel)
        pref = float(inSpec[1])
        index1 = inSpec[2]                      #must be negative
        CutEnergy = EnConv(inSpec[3],"GeV")     #convert the energy in GeV
        index2 = inSpec[4]                      # must be negative

        pref_text='parameter scale="'+numdiv(pref)[1]+'"  name="Prefactor"  min="1e-7"   max="1000"  free="1" value="'+numdiv(pref)[0]+'"'
        index1_text='parameter scale="-1.0"  name="Index1"  min="0.01"   max="+10.0"  free="1" value="'+index1+'"'
        cut_energy_text='parameter scale="'+str(CutEnergy[1])+'"  name="BreakValue"  min="10.0"   max="+100000000.0"  free="1" value="'+str(CutEnergy[0])+'"'
        index2_text='parameter scale="-1.0"  name="Index2"  min="0.01"   max="+10.0"  free="1" value="'+index2+'"'

        spectral = gammalib.GXmlElement('spectrum type="BrokenPowerLaw"')
        prefactor = spectral.append(gammalib.GXmlElement(pref_text))
        indice1 = spectral.append(gammalib.GXmlElement(index1_text))
        energia_min = spectral.append(gammalib.GXmlElement(cut_energy_text))
        indice2_max = spectral.append(gammalib.GXmlElement(index2_text))

    elif (SpecModel == 'EXPL'):
        #Exponential CUT OFF POWER LAW MODEL
        print('Spectral model: '+SpecModel)
        pref = float(inSpec[1])
        index = inSpec[2]
        CutEnergy = EnConv(inSpec[3], "MeV") #convert the energy in MeV
        PivotEnergy = EnConv(inSpec[4], "MeV") #convert the energy in MeV

        pref_text='parameter scale="'+numdiv(pref)[1]+'"  name="Prefactor"  min="1e-7"   max="1000"  free="1" value="'+numdiv(pref)[0]+'"'
        index_text='parameter scale="-1.0"  name="Index"  min="0.0"   max="+10.0"  free="1" value="'+index+'"'
        cut_energy_text='parameter scale="1.0"  name="Cutoff"  min="1.0"   max="100000000.0"  free="1" value="'+str(CutEnergy[0])+'"'
        piv_energy_text='parameter scale="1.0"  name="Scale"  min="10.0"   max="100000000.0"  free="0" value="'+str(PivotEnergy[0])+'"'

        spectral = gammalib.GXmlElement('spectrum type="ExpCutoff"')
        prefactor = spectral.append(gammalib.GXmlElement(pref_text))
        indice = spectral.append(gammalib.GXmlElement(index_text))
        cut_energia = spectral.append(gammalib.GXmlElement(cut_energy_text))
        pivot_energia = spectral.append(gammalib.GXmlElement(piv_energy_text))
    elif (SpecModel == 'SEPL'):
        print(SpecModel)
    elif (SpecModel == 'LOGPAR'):
        print(SpecModel)
    elif (SpecModel == 'GAUSS'):
        print(SpecModel)
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
    print(url.string())
    
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

    # read first line
    #inputs = f.readline()
    #inputs = inputs.split()

    with open(nomefile) as openfile:
        for line in openfile:
            inputs = line.split()
            sourcebranch = sourcelibrary.append(sourceDef(inputs))
    print('--------------------------------')
    
    #SHOW XML FILE    
    show_xml(xml)

    #print(models)
    # Save the XML document into a file
    xml.save(sys.argv[1][:-4]+'.xml')
