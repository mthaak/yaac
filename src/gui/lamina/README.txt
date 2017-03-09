
Lamina module

When you set the display mode for OpenGL, you enable all the coolness 
of 3D rendering, but you disable the bread-and-butter raster SDL 
functionality like fill() and blit(). Since the GUI libraries use 
those surface methods extensively, they cannot readily be used in 
OpenGL displays.

Lamina provides the LaminaPanelSurface and LaminaScreenSurface classes, 
which bridge between the two.

The LaminaPanelSurface requires you to stipulate where the paneloverlay 
will be drawn, and (possibly) to make adjustments for mouse coordinates. 
This is most useful if your viewer does not pan or pivot. I may add a 
feature to pin the paneloverlay to a fixed location in eyespace.

The LaminaScreenSurface will always be the size of the window (or screen 
if fullscreen), and needs refreshPos called whenever the camera moves.

The demonstration scripts are complete and functional, so look there for 
details.

There are six demonstration scripts in the distribution: The PGU and Ocemp
versions of my GUI comparison script have been converted to use 
LaminaPanelSurfaces. The two L04_lam_* scripts are conversions of Nehe 
tutorial lesson04 for Ocemp and PGU; the GUI provides buttons to toggle 
the image rotations on and off.  The two L04_lamzoom_* scripts are the 
same, except with a zoom button to demonstrate the refreshPositioning 
method, which repositions the texture to remain full-screen after a camera 
move.

	l04_lam_ocemp.py     : Nehe lesson 4, with added Ocemp GUI widgets
	l04_lam_pgu.py       : Nehe lesson 4, with added PGU widgets
	l04_lamzoom_ocemp.py : same as above, with zoom to demo repositioning
	l04_lamzoom_pgu.py   : same as above, with zoom to demo repositioning
	ocemp_lam.py	     : GUI comparison script (ocemp version)
	pgu_lam.py           : GUI comparison script (pgu version)
	pyg_lam.py           : demo with no GUI, just pygame


The lamina classes are all contained in the lamina.py file.  The other 
files are demonstration scripts and auxiliary files for those demos.  
Put the lamina.py file in your python path somewhere.


Code is by David Keeney, 2006, 2007
Find the latest at http://pduel.sourceforge.net
