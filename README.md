# Sexten 2017 school repository
This repository contains examples, scripts, ipython notebooks and other utilities which will be used for the hands-on session of the "Gamma Ray Astrophysics with CTA" school held in Sexten in July 2017.

## Prerequisites
Since the softwares used during the hands-on sessions are many, we set up a Virtual Machine with everything pre-installed. The software needed to run the Virtual Machine is VirtualBox.
Everything you need to know about installing VirtualBox and running the Virtual Machine is in the [User Guide](https://github.com/sharingan90/sexten_2017/blob/master/VM_Sexten_2017_User_guide.pdf).

## Hands-on available
During the school, there will be few hands-on on softwares used in High Energy and Very High Energy Astrophysics, namely:

1. Fermi Science Tools ([https://fermi.gsfc.nasa.gov/ssc/data/analysis/scitools/overview.html](https://fermi.gsfc.nasa.gov/ssc/data/analysis/scitools/overview.html)), used for the analysis of Fermi-LAT data
2. ctools ([http://cta.irap.omp.eu/ctools/](http://cta.irap.omp.eu/ctools/)), the software currently being developed for the analysis of the future Cherenkov observatory CTA
3. gammapy ([http://docs.gammapy.org/en/latest/](http://docs.gammapy.org/en/latest/)), an alternative of ctools but can be used for the analysis of general gamma-ray astronomy data

## Settings for the tutorials
Since the Fermi Science Tools were not compiled from source but installed as a binary, the built-in python of the Fermi Science Tools is incompatible with the python installed by default in the system, which was used to compiled the *ctools* and *gammalib*. So, in order not to have conflicts when working with the Fermi Science Tools and with the *ctools*, there are two bash scripts which set the proper environment variables to use one or the other software. <br>
That said, open the terminal and type ($ is the command prompt) in the home directory:

      $ source fermitools_heasoft.sh

to use the Fermi Science Tools, or:

      $ source gammalib_ctools.sh

to use the *ctools*.

## Programming knowledge
For some of the hands-on we will use Python and some Python modules widely used in Astrophysics and general data analysis e.g. numpy, Astropy, matplotlib. Here below you can find some links if you want to get comfortable using these tools:

- Python: [http://nbviewer.jupyter.org/github/jakevdp/WhirlwindTourOfPython/blob/master/Index.ipynb](http://nbviewer.jupyter.org/github/jakevdp/WhirlwindTourOfPython/blob/master/Index.ipynb)
- Numpy and matplotlib: [http://nbviewer.jupyter.org/github/jakevdp/PythonDataScienceHandbook/blob/master/notebooks/Index.ipynb](http://nbviewer.jupyter.org/github/jakevdp/PythonDataScienceHandbook/blob/master/notebooks/Index.ipynb)
- Astropy: [https://nbviewer.jupyter.org/github/gammapy/gammapy-extra/blob/master/notebooks/astropy\_introduction.ipynb](https://nbviewer.jupyter.org/github/gammapy/gammapy-extra/blob/master/notebooks/astropy_introduction.ipynb) and [https://github.com/Asterics2020-Obelics/School2017/blob/master/astropy/astropy\_hands\_on.ipynb](https://github.com/Asterics2020-Obelics/School2017/blob/master/astropy/astropy_hands_on.ipynb)

## ipython notebooks
For the ctools and gammapy hands-on, we will make use of the so called *jupyter notebooks*. With these notebooks it's easy to share code and create tutorials, where the code can be actually run and results can be inspected right away. <br>
To view any of the jupyter notebooks of this repository (.ipynb extension), just open a terminal and type ($ is the command prompt):

      $ jupyter-notebook example_notebook.ipynb

A browser page will open with the notebook content. In a notebook, there are cells with text and cells with code. <br>
The former are meant to explain what's going on, while the latter are meant to run the code they contain. <br>
To execute the code, just select the cell with the code and press "Shift+Enter". <br>
On the left of the cell, if the cell was not run before, you will see "In[]". When running, it will change to "In[*]": when done, it becomes "In[#]", where # stands for an integer number. <br>
If a code cell is running and you execute another code cell, the second one will not be executed until the first finishes its job, so be patient :) <br>
A good thing of these notebooks is that you can change the code inside the cells and test. But remember: if you run a code cell and you change something in previous cells, generally you have to run them again because the results in a cell usually depend on what is run in previous cells. <br>
If you really mess up, you can go to the menu **Kernel > Restart & Clear Output**. <br>
To exit, just close the web page and do "Ctrl+C" in the terminal and answer yes to the prompt. 
