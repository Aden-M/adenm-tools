This repository contains a series of data-analysis tools which were developed for use in the Texas A&M Engineering 217 course.

Summary of tools:

**Matrix_Flat_To_Full.xlsx** is an excel workbook which contains a scalable system for creating matrices
from a "flat" list of data.
A flat list of data consisting of x,y,z components was outputted by various tools used throughout the labs in 217.
Lab requirements necessitated that vector plots be created, but this could not be readily done with the form of the outputted data.
This tool prepares two matrices from an inputted dataset, and the user can scale the areas with little difficulty.

**adenlib.py** is a python library which contains useful data analysis functions for the data analysis required
in several 217 labs.

**vector_plotter.py** is a modified version of the vector plotter tool (provided by Texas A&M) which includes
several bugfixes related to data input, data plotting, and NAN input errors.
It is meant to be used in conjunction with matrix data (.csv format) from the Visualization Studio or 
from the Matrix_Flat_To_Full.xlsx tool.

**Two Dimensional Gradient Tool** is an excel workbook which creates x and y gradient components for an inputted dataset,
**BEWARE** there is currently a bug which seems to affect the direction of generated vectors in the vector plotting tool,
thus, it is the users responsibility to ensure that the data outputted is both reasonable and factual.
