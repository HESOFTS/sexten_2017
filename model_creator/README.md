### README : scriptModel_variable.py 

The script generates a .xml file to caraterise one or more source models in the
ctools standard starting from .txt file.


[General references at this page](http://cta.irap.omp.eu/ctools "ctools Homepage" )

[Specific references about ctools models](http://cta.irap.omp.eu/ctools/users/user_manual/getting_started/models.html "ctools models page")

If you need to use diffuse map model, save map file as "map.fits" 
	in the same directory

If you need to use diffuse map cube, save map cube file as "map_cube.fits" 
	in the same directory	

--------------------------------------------------------------------------------

*One line* in the .txt file represent a source. There, all the values **must** be separeted
by at least *one* space charater. If the value is not necessary, put anyway *at least*
one character (0 as standard).

EXAMPLE:
GRB_name  Point  1  329.719  -30.2217   0    0   0   FUNC  1.0  data/GRB_name.out  2.0   data/lightcrv_GRB_name.fits

The order must be as follow:

- **Source name** or background name (must start with BKG)

- **type of model**. Must be one of this list: 

	Point, RadDisk, RadGauss, RadShell, EllDisk, EllGauss, DiffIso,
	DiffMap, DiffMapCube, BkgGauss, Profile, Polynom, CTAIrf, CTACube

- 1 to execute **test statistics**, else 0 	

- after the first 3 values you have 5 values that depends on the model. It is better
	to use a standard character (*0*) when the model have less than 5 values.

	|         Model          |  I   |  II  |   III    |   VI    |   V     |
	| ---------------------- |  --- |------|----------|---------|---------|
	| Point Source  	     | RA   | DEC  |0  		  |0   	    |0        |
	| Radial Disk   	     | RA   | DEC  |Radius 	  |0 	    |0        |
	| Radial Gaussian 	     | RA   | DEC  |Sigma     |0	    |0        |
	| Radial Shell  	     | RA   | DEC  |Radius    |Width    |0        |
	| Elliptical disk 	     | RA   | DEC  |PA 		  |MinorRad |MajorRad |
	| Elliptical Gaussian 	 | RA   | DEC  |PA 		  |MinorRad |MajorRad |
	| Isotropic source 	     | Cost | 0	   |0	      |0	    |0        |
	| Diffuse Map 	         | Pref | 0	   |0	      |0	    |0        |
	| Diffuse Map Cube 	     | Norm | 0	   |0	      |0	    |0        |


EXAMPLE:
GRB_name  Point  1  329.719  -30.2217   0    0   0   FUNC  1.0  data/GRB_name.out  2.0   data/lightcrv_GRB_name.fits
