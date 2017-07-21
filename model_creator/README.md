# README : scriptModel_variable.py 

The script, written in python, generates a .xml file to caraterise one or more source or background models in the
ctools standard starting from plain text file.

To launch, in a bash terminal, write: `python scriptModel_variable.py flie_name`

[General references at this page](http://cta.irap.omp.eu/ctools "ctools Homepage" )

[Specific references about ctools models](http://cta.irap.omp.eu/ctools/users/user_manual/getting_started/models.html "ctools models page")

If you need to use diffuse map model, save map file as "map.fits" 
	in the same directory

If you need to use diffuse map cube, save map cube file as "map_cube.fits" 
	in the same directory	

# How to setup the source file

*One line* in the plain text file represent a source. There, all the values **must** be separeted
by at least *one* space charater. If the value is not necessary, put anyway *at least*
one character (0 as standard).

*EXAMPLE:*
`name  Point  1  329.719  -30.2217   0    0   0   FUNC  1.0  name.out  2.0   name.fits `

The order must be as follow:
<ol>

<li>  <b>Source name</b> (whatever you want) or background name (must start with BKG) 
 <p></p>
</li>

<li> <b>type of spatial model</b>. Must be one of the following: 
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
   <li>BkgGauss</li>
   <li>Profile</li>
   <li>Polynom</li>
   <li>CTAIrf</li>
   <li>CTACube</li>
   </ul>
    <p></p>
</li>
<li> 1 to execute <b>test statistics</b>, else 0 	 
 <p></p>
</li>

   <li>  
    After the first 3 values there are 5 values that depend on the model's type. It is better
   to use a standard character (0) when the model have less than 5 values.
   
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
<b>Type of spectral model </b><small><i>(This is after 5 strings, then position 9) </i></small>.
   Must be on of the following:
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
   must have one MeV, GeV, TeV units, and formatted as number*unit <i><small>(example: 50.3*GeV)</i></small>:

| Function model                        | I             | II       | III         | IV           | V            |  VI |
|---------------------------------------|---------------|----------|-------------|--------------|--------------|-----|
| Constant                              | Normalization |          |             |              |              |     |
| File function                         | Normalization | FileName |             |              |              |     |
| Node                                  | N. parameters | Energy1  | Intensity1  | Energy2      | Intensity2   | ... |
| Power law                             | Prefactor     | Index    | Pivot Energy |              |             |     |
| Power law 2                           | Integral      | Index    | Lower Limit  | Upper Limit   |            |     |
| Broken power law                      | Prefactor     | Index1   | Index2      | Break Energy   |             |     |
| Exponential cut-off power law         | Prefactor     | Index    | Pivot Energy | Cutoff Energy |              |     |
| Super exponentially cut-off power law | Prefactor     | Index1   | Index2      | Pivot Energy  | Cutoff Energy |     |
| Log parabola                          | Prefactor     | Index    | Curvature   | Pivot Energy  |              |     |
| Gaussian function                     | Normalization | Mean     | Sigma       |              |              |     |
 
 <p> </p>
 
   </li>

   <li>
   <i> NOT MANDATORY:</i> You can put here the normalization and the name or directory of a .fits file for
   temporal evolution. <i><small>EXAMPLE: 20.4   temp_ev.fits</i></small>
    <p></p>
   </li>
</ol> 	


*EXAMPLE:*
`name  Point  1  329.719  -30.2217   0    0   0   FUNC  1.0  name.out  2.0   name.fits`
 
####Authors

@thomasgas :+1: :+1:  :stuck_out_tongue_closed_eyes:  :stuck_out_tongue_closed_eyes:
@IlDordollano
