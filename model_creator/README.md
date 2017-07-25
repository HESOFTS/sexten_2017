# README : scriptModel_variable.py 

The script, written in Python, generates a .xml file to characterize one or more sources or background models in the
*ctools* standard, starting from plain text file.

The **Python** script need only the **GammaLib** library, which can be downloaded [here](http://gammalib.sourceforge.net/admin/index.html "Getting GammaLib page")

The script can be launched from terminal typing: `$ python scriptModel_variable.py file_name`, where $ denotes the command prompt.
If you add another variable, whatever you write, you get verbose mode on: `python scriptModel_variable.py file_name verb` <br>.

[General references at this page](http://cta.irap.omp.eu/ctools "ctools Homepage" )

[Specific references about ctools models](http://cta.irap.omp.eu/ctools/users/user_manual/getting_started/models.html "ctools models page")

If you need to use diffuse map model, save map file as "map.fits" 
	in the same directory

If you need to use diffuse map cube, save map cube file as "map_cube.fits" 
	in the same directory	
	
The **free parameter** is set as reported on ctools page, but you should check those numbers on xml file and change it if you want differents free parameters.
	
**NOTE**: this script is *far from perfect*. Keep it as it is, double check the resulting xml file, and if you get some errors write to thomas.gasparetto@ts.infn.it.

# How to setup the source file

*Each line* in the plain text file represents a source. There, all the values **must** be separated
by at least *one* space character. If the value is not necessary, put anyway *at least*
one character (we use 0 as standard and we advise you to do so). Comments need to start with `#`.

*EXAMPLE:*
`src_name  Point  1  329.719  -30.2217   0    0   0   FUNC  1.0  name.out  2.0   name.fits`

The order must be as follows:
<ol>

<li><b>Source name</b> (without spaces in the name, but the underscore can be used).
 <p></p>
</li>

<li><b>Spatial models</b> You must be one of the following: 
   <ul>
   <li>Point</li>
   <li>RanDisk</li>
   <li>RadGauss</li>
   <li>RadShell</li>
   <li>EllDisk</li>
   <li>EllGauss</li>
   <li>DiffIso</li>
   <li>DiffMap</li>
   <li>DiffMapCube</li>
   </ul>
    <p></p>
</li>
<li> The third element in the list must be an integer. If it is equal to `1`, then during the computation of the likelihood (via `ctlike`), the [Test Statistics](https://en.wikipedia.org/wiki/Test_statistic) value will be computed. The square root of the TS parameter gives the significance of the detection of the source: the higher is the value, the better the source has been extracted from the background.
If you don't want to compute TS, just put the value equal to `0` in the input text file.

 <p></p>
</li>

   <li>
    After the first 3 values there are 5 values that depend on the spatial model.. It is better
   to use a standard character (0) when the model have less than 5 values, in order to fill the missing entries..
   
   |         Spatial model  |  I   |  II  |   III    |   VI    |   V     |
   | ---------------------- |  --- |------|----------|---------|---------|
   | Point Source           | RA   | DEC  |0         |0        |0        |
   | Radial Disk            | RA   | DEC  |Radius    |0        |0        |
   | Radial Gaussian        | RA   | DEC  |Sigma     |0        |0        |
   | Radial Shell           | RA   | DEC  |Radius    |Width    |0        |
   | Elliptical disk        | RA   | DEC  |PA        |MinorRad |MajorRad |
   | Elliptical Gaussian    | RA   | DEC  |PA        |MinorRad |MajorRad |
   | Isotropic source       | Cost | 0    |0         |0        |0        |
   | Diffuse Map            | Pref | 0    |0         |0        |0        |
   | Diffuse Map Cube       | Norm | 0    |0         |0        |0        |
    
   </li>
<li> 
<b>Spectral models </b><small><i>(This models starts with the 9-th entry, after the 5 entries of the spatial model) </i></small>.
   Must be one of the following:
   <ul>
      <li>CONST</li>
      <li>FUNC</li>
      <li>NODE</li>
      <li>PL</li>
      <li>PL2</li>
      <li>BRPL</li>
      <li>EXPL</li>
      <li>SEPL</li>
      <li>LOGPAR</li>
      <li>GAUSS</li>
   </ul>
    <p></p>
</li>
   <li> 
   You must insert the right number of values, depending on the function model. Energies
   must have MeV, GeV or TeV units, and must be formatted as `number*unit` <i><small>(example: 50.3*GeV)</i></small>. **NOTE**: We have implemented by now only the units for the energy and not for the flux:

| Function model                        | I             | II       | III         | IV           | V            |  VI |
|---------------------------------------|---------------|----------|-------------|--------------|--------------|-----|
| Constant                              | Normalization |          |             |              |              |     |
| File function                         | Normalization | FileName |             |              |              |     |
| Node                                  | N. parameters | Energy1  | Intensity1  | Energy2      | Intensity2   | ... |
| Power law                             | Prefactor     | Index    | Pivot Energy |              |             |     |
| Power law 2                           | Integral      | Index    | Lower Limit  | Upper Limit   |            |     |
| Broken power law                      | Prefactor     | Index1   | Index2      | Break Energy   |            |     |
| Exponential cut-off power law         | Prefactor     | Index    | Pivot Energy | Cutoff Energy |            |     |
| Super exponentially cut-off power law | Prefactor     | Index1   | Index2      | Pivot Energy  | Cutoff Energy |     |
| Log parabola                          | Prefactor     | Index    | Curvature   | Pivot Energy  |             |     |
| Gaussian function                     | Normalization | Mean     | Sigma       |               |             |     |
 
 <p> </p>
 
   </li>

   <li>
   <i> Temporal modeling:</i> If the last element in the row is a .fits file, also the temporal modeling will be "activated": here the last string specifies the name of the fits file (it can be given also with the relative path), and the last but one is the temporal normalization. Remember that the fits file specifying the temporal variation can be only in the range \[0,1\].
<i><small>EXAMPLE: ...... 20.4   temp_ev.fits</i></small>
    <p></p>
   </li>
</ol> 	

# Background
*EXAMPLE:*
`BKGname  CTAIrf  0   0    0    0   0   0   PL    1.0    0.0    0.3*TeV`

<ol>

<li>  <b>Background name</b> (whatever you want) **BUT** it must start with BKG.
 <p></p>
</li>


<li> <b>Spatial model for the background</b>. Must be one of the following: 
   <ul>
   <li>BkgGauss</li>
   <li>Profile</li>
   <li>Polynom</li>
   <li>CTAIrf</li>
   <li>CTACube</li>
   </ul>
    <p></p>
</li>

<li> TS calculation is the same as for the source case: it is not very useful to compute the TS parameter for the background (and it will take a lot of time to compute it).
 <p></p>
</li>

<li> Same as source case, but now you have to choose between:

   |         Spatial model  |  I   |  II  |   III    |   VI    |   V     |
   | ---------------------- |  --- |------|----------|---------|---------|
   | BkgGauss               |Sigma | 0    |0         |0        |0        |
   | Profile                |Width |Core  |Tail      |0        |0        |
   | Polynom                | c1_c2_c3_c4...| 0  |0     |0        |0        |
   | CTAIrf                 | 0    |0     |0         |0        |0        |
   | CTACube                | 0    | 0    |0         |0        |0        |

 <p></p>
</li>

<li> Same as source case.
 <p></p>
</li>
<li> Same as source case.
 <p></p>
</li>

<li> Same as source case.
 <p></p>
</li>
</ol>
 
### Authors

@thomasgas :+1: :+1:

@IlDordollano
