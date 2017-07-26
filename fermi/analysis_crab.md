# Crab Nebula analysis #

## Introduction ##

This file contains all the commands I run to perform the pulse assignment of the events
and the likelihood analysis. <br>
All the commands were run from the Crab\_Flare\_2014 directory. <br>
In order not to overwrite the files in the directory, you can create a new one and copy the
event and spacescraft files (L1707191221448796F97375\_PH00.fits and L1707191221448796F97375\_SC00.fits) and 
the ephemerides file (Crab\_ephem\_new.par) in the new directory. <br>
After that you can issue the same commands you find below. 

You can find the content of this tutorial at the links [https://fermi.gsfc.nasa.gov/ssc/data/analysis/scitools/pulsar_gating_tutorial.html](https://fermi.gsfc.nasa.gov/ssc/data/analysis/scitools/pulsar_gating_tutorial.html) and [https://fermi.gsfc.nasa.gov/ssc/data/analysis/scitools/likelihood_tutorial.html](https://fermi.gsfc.nasa.gov/ssc/data/analysis/scitools/likelihood_tutorial.html).

## Setup and data selection ##

The data were already downloaded, so we don't need to download them. In any case, the link to
the LAT Data Server is [https://fermi.gsfc.nasa.gov/cgi-bin/ssc/LAT/LATDataQuery.cgi](https://fermi.gsfc.nasa.gov/cgi-bin/ssc/LAT/LATDataQuery.cgi). <br>

First we setup the Fermi tools:

      [fermi-cta@localhost Crab_Flare_2014]$ source $HOME/fermitools_heasoft.sh

Then we use **gtselect** to do data selection. Since the data I downloaded were on a region of 30 deg radius and 100 MeV-500 GeV energy range, I will shrink the radius down to 15 deg and modify the energy range
to 100 MeV-300 GeV. When running **gtselect** and other Fermi tools executables, you will get a prompt with the inputs needed. Also, I specify the event class and event type (see the introduction to the hands on done on Monday by Francesco).

      [fermi-cta@localhost Crab_Flare_2014]$ gtselect evclass=128 evtype=3
      Input FT1 file[] L1707191221448796F97375_PH00.fits
      Output FT1 file[] Crab_Flare_2014_select.fits 
      RA for new search center (degrees) (0:360) [INDEF] 83.63308333
      Dec for new search center (degrees) (-90:90) [INDEF] 22.0145
      radius of new search region (degrees) (0:180) [15] 
      start time (MET in s) (0:) [INDEF] 
      end time (MET in s) (0:) [INDEF] 
      lower energy limit (MeV) (0:) [] 100 
      upper energy limit (MeV) (0:) [] 300000
      maximum zenith angle value (degrees) (0:180) [] 90 
      Done.

In this case I specified the coordinates of the Crab which were the ones when I downloaded the data. To see which are the coordinates in the event file, you can run **gtvcut**:

      fermi-cta@localhost Crab_Flare_2014]$ gtvcut L1707191221448796F97375_PH00.fits

From *gtvcut* output you can find easily the RA nad Dec of the source (Crab). <br>

You can see that for the *start time* and *end time* parameters we left **INDEF**. It means that **gtselect** will read those values from the input FT1 file.

**NOTE: a known bug of gtselect is that if you choose one of RA, Dec or radius as INDEF, also the other two will be left as INDEF. See the end of the README for gtselect at the link [https://fermi.gsfc.nasa.gov/ssc/data/analysis/scitools/help/gtselect.txt](https://fermi.gsfc.nasa.gov/ssc/data/analysis/scitools/help/gtselect.txt)**

After the selection in time, energy and position, we want to select from the spacecraft file the so called *Good Time Intervals*, that is the time intervals in which Fermi did not have any problems. To do that, we use **gtmktime**:

      [fermi-cta@localhost Crab_Flare_2014]$ gtmktime 
      Spacecraft data file[] L1707191221448796F97375_SC00.fits
      Filter expression[] (DATA_QUAL>0) && (LAT_CONFIG==1)
      Apply ROI-based zenith angle cut[] no
      Event data file[] Crab_Flare_2014_select.fits
      Output event file name[] Crab_Flare_2014_gti.fits

Before going on, we check the selection we made with **gtvcut**:

      [fermi-cta@localhost Crab_Flare_2014]$ gtvcut Crab_Flare_2014_gti.fits 
      Extension name[EVENTS] 
      DSTYP1: BIT_MASK(EVENT_CLASS,128,P8R2)
      DSUNI1: DIMENSIONLESS
      DSVAL1: 1:1
      
      DSTYP2: POS(RA,DEC)
      DSUNI2: deg
      DSVAL2: CIRCLE(83.63308333,22.0145,15)
      
      DSTYP3: TIME
      DSUNI3: s
      DSVAL3: TABLE
      DSREF3: :GTI
      
      GTIs: (suppressed)
      
      DSTYP4: BIT_MASK(EVENT_TYPE,3,P8R2)
      DSUNI4: DIMENSIONLESS
      DSVAL4: 1:1
      
      DSTYP5: ENERGY
      DSUNI5: MeV
      DSVAL5: 100:300000
      
      DSTYP6: ZENITH_ANGLE
      DSUNI6: deg
      DSVAL6: 0:95

The several parameters are described by DSS keys which you can see from **gtvcut** output. For example, the first DSS key describes the event class we selected, the second the position and radius region and so on. <br>
**NOTE: check that there are not two DSS keys with the same name (TYP): it means that you have two cuts on that parameter. If you go on with the analysis, you will get a crash. So, go back and run again gtselect and gtmktime properly!**

## Count map and count cube ##

When you have the selected data, you can create a count map (integrate over all the energy range) with **gtbin**:

      [fermi-cta@localhost Crab_Flare_2014]$ gtbin
      This is gtbin version ScienceTools-v10r0p5-fssc-20150518
      Type of output file (CCUBE|CMAP|LC|PHA1|PHA2|HEALPIX) [CMAP] 
      Event data file name[Crab_Flare_2014_gti.fits] 
      Output file name[Crab_Flare_2014_cmap.fits] 
      Spacecraft data file name[L1707191221448796F97375_SC00.fits] 
      Size of the X axis in pixels[150] 300
      Size of the Y axis in pixels[150] 300
      Image scale (in degrees/pixel)[0.2] 0.1
      Coordinate system (CEL - celestial, GAL -galactic) (CEL|GAL) [CEL] 
      First coordinate of image center in degrees (RA or galactic l)[83.63308333] 
      Second coordinate of image center in degrees (DEC or galactic b)[22.0145] 
      Rotation angle of image axis, in degrees[0] 
      Projection method e.g. AIT|ARC|CAR|GLS|MER|NCP|SIN|STG|TAN:[AIT]

You can see the output fits file with **ds9**:

      [fermi-cta@localhost Crab_Flare_2014]$ ds9 Crab_Flare_2014_cmap.fits

You can create a count cube (count map binned in energy) again with **gtbin**:

      [fermi-cta@localhost Crab_Flare_2014]$ gtbin
      This is gtbin version ScienceTools-v10r0p5-fssc-20150518
      Type of output file (CCUBE|CMAP|LC|PHA1|PHA2|HEALPIX) [CMAP] CCUBE
      Event data file name[Crab_Flare_2014_gti.fits] 
      Output file name[Crab_Flare_2014_cmap.fits] Crab_Flare_2014_ccube.fits 
      Spacecraft data file name[L1707191221448796F97375_SC00.fits] 
      Size of the X axis in pixels[300] 
      Size of the Y axis in pixels[300] 
      Image scale (in degrees/pixel)[0.1] 
      Coordinate system (CEL - celestial, GAL -galactic) (CEL|GAL) [CEL] 
      First coordinate of image center in degrees (RA or galactic l)[83.63308333] 
      Second coordinate of image center in degrees (DEC or galactic b)[22.0145] 
      Rotation angle of image axis, in degrees[0] 
      Projection method e.g. AIT|ARC|CAR|GLS|MER|NCP|SIN|STG|TAN:[AIT] 
      Algorithm for defining energy bins (FILE|LIN|LOG) [LOG] 
      Start value for first energy bin in MeV[100] 
      Stop value for last energy bin in MeV[300000] 
      Number of logarithmically uniform energy bins[30] 35

Again, check the image with **ds9**:

      [fermi-cta@localhost Crab_Flare_2014]$ ds9 Crab_Flare_2014_ccube.fits

## Pulse assignment ##

Since when I did the analysis in the Crab\_Flare\_2014 directory I had two ephemerides files, I renamed Crab\_Flare\_2014\_gti.fits:

      [fermi-cta@localhost Crab_Flare_2014]$ mv Crab_Flare_2014_gti.fits Crab_Flare_gti_new_ephem.fits

To perform the pulse assignment of the events, we use the Fermi plugin of TEMPO2. It will add a column called PULSE\_PHASE to our event file with the pulse phase of each event.

      [fermi-cta@localhost Crab_Flare_2014]$ tempo2 -gr fermi -ft1 Crab_Flare_2014_gti_new_ephem.fits -ft2 L1707191221448796F97375_SC00.fits -f Crab_ephem_new.par -phase -graph 0
      This program comes with ABSOLUTELY NO WARRANTY.
      This is free software, and you are welcome to redistribute it
      under conditions of GPL license.
      
      Looking for /usr/share/tempo2/T2runtime/plugins//fermi_linux-gnu_plug.t2
      
      ------------------------------------------
      Output interface:    fermi
      Author:              Lucas Guillemot
      Updated:             10 April 2017
      Version:             6.0
      ------------------------------------------
      
      First photon date in FT1: 383272238.211687 MET (s)
       Last photon date in FT1: 385297201.030515 MET (s)
      
      Adding new column PULSE_PHASE.
      
      First START date in FT2:  383270375.600000 MET (s)
       Last START date in FT2:  385299302.600000 MET (s)
      
      [tempo2Util.C:360] Warning: [CLK3] no clock corrections available for clock UTC(coe) for MJD 56303.2
      [tempo2Util.C:360] Warning: [CLK4] Trying assuming UTC = UTC(coe)
      [tempo2Util.C:360] Warning: [CLK9] ... ok, using stated approximation 
      [tempo2Util.C:365] Warning: [DUP1] duplicated warnings have been suppressed.
      [tempo2Util.C:360] Warning: [CLK6] Proceeding assuming UTC =  UTC(coe)
      Treating events # 1 to 10000... 
      Treating events # 10001 to 20000... 
      Treating events # 20001 to 30000... 
      Treating events # 30001 to 40000... 
      Treating events # 40001 to 50000... 
      Treating events # 50001 to 55207... 
      Done with J0534+2200

After inspecting the pulse phase light curve with **fv**:

      [fermi-cta@localhost Crab_Flare_2014]$ fv Crab_Flare_2014_gti_new_ephem.fits

we see that the so called off-phase region (so the nebula contribution) is between 0.5 and 0.9 pulse phase. We use again **gtselect** to select the pulse phase interval:

      [fermi-cta@localhost Crab_Flare_2014]$ gtselect evclass=128 evtype=3 phasemin=.5 phasemax=.9
      Input FT1 file[L1707191221448796F97375_PH00.fits] Crab_Flare_2014_gti_new_ephem.fits 
      Output FT1 file[Crab_Flare_2014_select.fits] Crab_Flare_2014_05_09_phasecut.fits
      RA for new search center (degrees) (0:360) [83.63308333] 
      Dec for new search center (degrees) (-90:90) [22.0145] 
      radius of new search region (degrees) (0:180) [15] 
      start time (MET in s) (0:) [INDEF] 
      end time (MET in s) (0:) [INDEF] 
      lower energy limit (MeV) (0:) [100] 
      upper energy limit (MeV) (0:) [300000] 
      maximum zenith angle value (degrees) (0:180) [95] 
      Done.

We can create a count map of the output file (Crab\_Flare\_2014\_05\_09\_phasecut.fits) and compare it with the one we did before. You can see that the Crab is a lot fainter.

      [fermi-cta@localhost Crab_Flare_2014]$ gtbin
      This is gtbin version ScienceTools-v10r0p5-fssc-20150518
      Type of output file (CCUBE|CMAP|LC|PHA1|PHA2|HEALPIX) [CCUBE] CMAP
      Event data file name[Crab_Flare_2014_gti.fits] Crab_Flare_2014_05_09_phasecut.fits 
      Output file name[Crab_Flare_2014_ccube.fits] Crab_Flare_2014_05_09_phasecut_cmap.fits
      Spacecraft data file name[L1707191221448796F97375_SC00.fits] 
      Size of the X axis in pixels[300] 
      Size of the Y axis in pixels[300] 
      Image scale (in degrees/pixel)[0.1] 
      Coordinate system (CEL - celestial, GAL -galactic) (CEL|GAL) [CEL] 
      First coordinate of image center in degrees (RA or galactic l)[83.63308333] 
      Second coordinate of image center in degrees (DEC or galactic b)[22.0145] 
      Rotation angle of image axis, in degrees[0] 
      Projection method e.g. AIT|ARC|CAR|GLS|MER|NCP|SIN|STG|TAN:[AIT] 

      [fermi-cta@localhost Crab_Flare_2014]$ ds9 Crab_Flare_2014_05_09_phasecut_cmap.fits

## Exposure map calculation ##

To compute the exposure map, first you have to produce the so called livetime cube (the time that the LAT observed a given position on the sky at a given inclination angle) with **gtltcube**:

      [fermi-cta@localhost Crab_Flare_2014]$ gtltcube zmax=90
      Event data file[Crab_Flare_2014_gti_new_ephem.fits] Crab_Flare_2014_05_09_phasecut.fits 
      Spacecraft data file[L1707191221448796F97375_SC00.fits] L1707191221448796F97375_SC00.fits 
      Output file[Crab_Flare_2014_ltcube.fits] Crab_Flare_2014_nebula_ltcube.fits
      Step size in cos(theta) (0.:1.) [0.025] 
      Pixel size (degrees)[1] 
      Working on file L1707191221448796F97375_SC00.fits
      .....................!

After that, we can compute the exposure map (takes time) with **gtexpmap**:

      [fermi-cta@localhost Crab_Flare_2014]$ gtexpmap 
      The exposure maps generated by this tool are meant
      to be used for *unbinned* likelihood analysis only.
      Do not use them for binned analyses.
      Event data file[] Crab_Flare_2014_05_09_phasecut.fits 
      Spacecraft data file[] L1707191221448796F97375_SC00.fits 
      Exposure hypercube file[] Crab_Flare_2014_nebula_ltcube.fits 
      output file name[] Crab_Flare_2014_nebula_expmap.fits 
      Response functions[CALDB] 
      Radius of the source region (in degrees)[30] 
      Number of longitude points (2:1000) [120] 
      Number of latitude points (2:1000) [120] 
      Number of energies (2:100) [20] 30
      Computing the ExposureMap using Crab_Flare_2014_nebula_ltcube.fits
      ....................!

You can inspect the exposure in the energy bins with **ds9**:

      [fermi-cta@localhost Crab_Flare_2014]$ ds9 Crab_Flare_2014_nebula_expmap.fits

<!--
## Model creation ##

To create your source model, first I downloaded some needed files:

      [fermi-cta@localhost Crab_Flare_2014]$ wget -q https://fermi.gsfc.nasa.gov/ssc/data/analysis/software/aux/gll_iem_v06.fits &

      [fermi-cta@localhost Crab_Flare_2014]$ wget -q https://fermi.gsfc.nasa.gov/ssc/data/analysis/software/aux/iso_P8R2_SOURCE_V6_v06.txt &

      [fermi-cta@localhost Crab_Flare_2014]$ wget -q https://fermi.gsfc.nasa.gov/ssc/data/analysis/user/make3FGLxml.py &

      [fermi-cta@localhost Crab_Flare_2014]$ wget -q https://fermi.gsfc.nasa.gov/ssc/data/access/lat/4yr_catalog/gll_psc_v16.fit &

[fermi-cta@localhost Crab_Flare_2014]$ python make3FGLxml.py gll_psc_v16.fit Crab_Flare_2014_05_09_phasecut.fits -r 10
This is make3FGLxml version 01r0.
The default diffuse model files and names are for pass 8 and assume you have v10r00p05 of the Fermi Science Tools or higher.
Creating file and adding sources from 3FGL
Extended source S 147 in ROI, make sure $(LATEXTDIR)/Templates/S147.fits is the correct path to the extended template.
Extended source IC443 in ROI, make sure $(LATEXTDIR)/Templates/IC443.fits is the correct path to the extended template.
Added 123 point sources and 2 extended sources
If using unbinned likelihood you will need to rerun gtdiffrsp for the extended sources or rerun the makeModel function with optional argument psForce=True

[fermi-cta@localhost Crab_Flare_2014]$ wget -q https://fermi.gsfc.nasa.gov/ssc/data/access/lat/4yr_catalog/LAT_extended_sources_v15.tgz &

[fermi-cta@localhost Crab_Flare_2014]$ tar -xvzf LAT_extended_sources_v15.tgz

[fermi-cta@localhost Crab_Flare_2014]$ cp Extended_archive_v15/Templates/IC443.fits .

[fermi-cta@localhost Crab_Flare_2014]$ cp Extended_archive_v15/Templates/S147.fits .

[fermi-cta@localhost Crab_Flare_2014]$ python make3FGLxml.py gll_psc_v16.fit Crab_Flare_2014_05_09_phasecut.fits -r 0.1
This is make3FGLxml version 01r0.
The default diffuse model files and names are for pass 8 and assume you have v10r00p05 of the Fermi Science Tools or higher.
Warning: mymodel.xml already exists, file will be overwritten if you proceed with makeModel.
Creating file and adding sources from 3FGL
Extended source S 147 in ROI, make sure $(LATEXTDIR)/Templates/S147.fits is the correct path to the extended template.
Extended source IC443 in ROI, make sure $(LATEXTDIR)/Templates/IC443.fits is the correct path to the extended template.
Added 123 point sources and 2 extended sources
If using unbinned likelihood you will need to rerun gtdiffrsp for the extended sources or rerun the makeModel function with optional argument psForce=True

[fermi-cta@localhost Crab_Flare_2014]$ mv mymodel.xml Crab_nebula.xml

[fermi-cta@localhost Crab_Flare_2014]$ gtdiffrsp 
Event data file[Crab_Flare_2014_05_09_phasecut.fits] 
Spacecraft data file[L1707191221448796F97375_SC00.fits] 
Source model file[Crab_nebula.xml] 
Response functions to use[CALDB] 
adding source IC443
adding source S 147
adding source gll_iem_v06
adding source iso_P8R2_SOURCE_V6_v06
Working on...
Crab_Flare_2014_05_09_phasecut.fits.....................!

[fermi-cta@localhost Crab_Flare_2014]$ gtlike refit=yes plot=yes sfile=Crab_nebula_output.xml
Statistic to use (BINNED|UNBINNED) [UNBINNED] 
Spacecraft file[none] L1707191221448796F97375_SC00.fits 
Event file[none] Crab_Flare_2014_05_09_phasecut.fits 
Unbinned exposure map[none] Crab_Flare_2014_nebula_expmap.fits 
Exposure hypercube file[none] Crab_Flare_2014_nebula_ltcube.fits 
Source model file[] Crab_nebula.xml 
Response functions to use[CALDB] 
Optimizer (DRMNFB|NEWMINUIT|MINUIT|DRMNGB|LBFGS) [MINUIT] NEWMINUIT

CrabNebula:
Prefactor: 3.751911779 +/- 0.1355590489
Index: 3.124514894 +/- 0.04227568586
Scale: 100.797539
Npred: 2618.147627
ROI distance: 0
TS value: 5158.178961
Flux: 1.814841543e-06 +/- 4.671329399e-08 photons/cm^2/s

IC443:
norm: 1.207444332 +/- 0.1475324524
alpha: 1.829382688 +/- 0.08240889151
beta: 0.1283599027 +/- 0.0492879851
Eb: 1444.22
Npred: 257.2745557
Flux: 1.27875749e-07 +/- 1.795900505e-08 photons/cm^2/s

S 147:
Prefactor: 1.121540998 +/- 0.4350005657
Index: 2.604827655 +/- 0.2840344868
Scale: 705.126282
Npred: 179.1997756
Flux: 1.133792631e-07 +/- 2.675292344e-08 photons/cm^2/s

gll_iem_v06:
Prefactor: 0.4011867121 +/- 0.00744211308
Index: 0
Scale: 100
Npred: 12224.65993
Flux: 0.0001960401586 +/- 3.63629064e-06 photons/cm^2/s

iso_P8R2_SOURCE_V6_v06:
Normalization: 0.2242893312 +/- 0.04966209095
Npred: 929.3634311
Flux: 3.355467134e-05 +/- 7.423042468e-06 photons/cm^2/s

WARNING: Fit may be bad in range [100, 12197.6] (MeV)
WARNING: Fit may be bad in range [40536, 60491.9] (MeV)

Total number of observed counts: 20499
Total number of model events: 23446.86653

-log(Likelihood): 200819.0294

Writing fitted model to Crab_nebula_output.xml
Refit? [y] 
n
Elapsed CPU time: 1281.94
-->