#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 16 15:31:49 2019

@author: anthony
"""

# DBiPlot5 is born
# Primarily adapted from 4.2 with the addition of plotting Peclet numbers

###############################################################################
# Section 0: Importing Libraries
###############################################################################

# Responsible for creating all of our pretty graphs at the end
import matplotlib.pyplot as plt
# The bread and butter of working with scientific Python
# Goal is to take more use from this through arrays
import numpy as np
# Very excellent for dealing with files
import tkinter as tk
# Helps us pull up that nice little dialogue box
import tkinter.filedialog as fd
# Really just after curve_fit right now
import scipy as sc
from scipy.optimize import curve_fit
# Used for dealing with directories and whatnot
import os
# regexp has a wonderful little thing to pull out bits from strings
# Need this for pulling variable data from
import re

###############################################################################
# Section 1: Loading in files
###############################################################################
# This section is all about finding all of the data from whatever directory

# A diaglogue window will popup asking for where the folders are
# You'll tell it the overarching folder where all of the data folders are
# Data folders should be in the form ***Force_***Potential
# It will pull the Force for each data set based on that folder name

# This diaglogue window will start wherever initialdir says
# You can always just move away from that folder
# If it throughs an error, change so initialdir = '/'
root = tk.Tk()
root.withdraw()
startdir = fd.askdirectory(initialdir = '/',title='Where are the folders?') 
#startdir = '/home/anthony'
# Then tell Python where we're going to be working from
os.chdir(startdir)
print('Working out of %s' % startdir)
# And we'll figure out everything that's in the folder we've selected
biglist = (os.listdir(startdir))
# But now we need to isolate only the folders with data that we want
# We'll save them all here
foldlist = []
# Now we check if the folders match our naming scheme
for i in range(0, len(biglist)):
    # This is kind of a sloppy workaround, but whatever
    if 'Pot' in biglist[i]:
        foldlist.append(biglist[i])
        # Now we'll have a list of only the folders with good stuff in them
        
        
# We're going to make a list of all data
datalist = []
# It'd be nice to know what forces and gammas are used too
forcelist = []
gammalist = []
for i in range(0,len(foldlist)):
    # Start with a blank file list each time
    # This creates a string of the path name for a particular data folder
    path = (startdir + '/' + foldlist[i])
    # Now we change directory to that particular folder
    # Remember to change back afterwards!
    os.chdir(path)
    # And produce a list of those files in our folder
    filelist = (os.listdir(path))
    
    for j in range(0,len(filelist)):
        # Now we're going to go through a load each of the files
        # Give this thing a name for what we're going to be saving
        # tempname is going to be the ***Gam.dat file
        tempname = filelist[j]
        # Combine with folder name, trim off '.dat'
        newname = foldlist[i] + '_' + tempname[:-4]
        # Load a data file into a temporary variable
        # This now has six columns of data we want
        tempload = np.genfromtxt(filelist[j])
        # From the file name,
        rs = re.findall("[-+]?[.]?[\d]+(?:,\d\d\d)*[\.]?\d*(?:[eE][-+]?\d+)?",newname)
        tempgam = float(rs[2])
        gammalist.append(tempgam)
        tempforce = float(rs[0])
        forcelist.append(tempforce)
        for k in range(0,len(tempload)):
            # This is in a particular order for data
            # Element 1 is the force F0, element 2 is the gamma
            # element 3 is the phi, element 4 is the average velocity
            # element 5 is the error of that velocity, 6 is the diffusion
            # 7 the error in diffusion, 8 the Peclet number
            # Filthy backend, clean frontend
            temptuple = (tempforce,tempgam,tempload[k,0],tempload[k,1],tempload[k,2],tempload[k,3],tempload[k,4],tempload[k,5])
            datalist.append(temptuple)
        
# Now we have this big ol' list of all the numbers we want

# Turn it into an array
darray = np.array(datalist)
# Now any time we want a particular value, we just have to use 
# array[array[:,*] == value]


# Lastly, remove any duplicates from the forces and gammas
forcelist = list(set(forcelist))
gammalist = list(set(gammalist))
gammalist.sort(key=float)
forcelist.sort(key=float)

###############################################################################
# Section 2: Analysis
###############################################################################
# We don't really need the breaking apart like from version 2

# Give the function that we'll be fitting with
# x is the phis we feed in
def func(x,A,phi0):
    return A*(np.sin(x-phi0))


fittedlist = []

for i in range(0,len(forcelist)):
    # Let's pull out all of the data with a single force
    tempforcearray = darray[darray[:,0] == forcelist[i]]
    # Now we want to do a similar thing to get the gammas pulled out individually
    for j in range(0,len(gammalist)):
        # This is an array of ONLY one force and one gamma at a time
        tempgammaarray = tempforcearray[tempforcearray[:,1] == gammalist[j]]
        # Fit our function to the data from this set
        # fittemp[0] is A, fittemp[1] is phi0
        # Set bounds so that A can't be smaller than 0
        # phi can only be between negative and positive pi
        fittemp,fiterror = curve_fit(func,tempgammaarray[:,2],tempgammaarray[:,3],bounds=((0,-.5),(1000000,1.9*np.pi)))
        # Now we'll save the force, gamma, A, and phi0
        temptuple = (forcelist[i],gammalist[j],fittemp[0],fittemp[1])
        fittedlist.append(temptuple)
        
# And I like these NumPy arrays so I'll convert the fittedlist
fittedarray = np.array(fittedlist)
        

#!#!#!#!#!#!#!#!#!#!#!#!#!#!#!#!#!#!#!#!#!#!#!#!#!#!#!#!#!#!#!#!#!#!#!#!#!#!#!#
# Doing the Peclet Shit
#!#!#!#!#!#!#!#!#!#!#!#!#!#!#!#!#!#!#!#!#!#!#!#!#!#!#!#!#!#!#!#!#!#!#!#!#!#!#!#

peclist = []
for i in range(0,len(forcelist)):
    # Let's pull out all of the data with a single force
    tempforcearray = darray[darray[:,0] == forcelist[i]]
    # Now we want to do a similar thing to get the gammas pulled out individually
    for j in range(0,len(gammalist)):
        # This is an array of ONLY one force and one gamma at a time
        tempgammaarray = tempforcearray[tempforcearray[:,1] == gammalist[j]]
        # ...but instead finds the max Peclet number of all of them
        # Just in case that number isn't exactly at the pi/2 phase
        maxPec = max(tempgammaarray[:,7])
        # Same old method of saving to a tuple
        temptuple = (forcelist[i],gammalist[j],maxPec)
        # Then putting it all into a big list of tuples
        peclist.append(temptuple)
        
# Now we define a function for plotting like the later sections
def pecplot():
    # Convert that list of tuples into a Numpy array
    pecarray = np.asarray(peclist)
    # Then break it into generic x, y, and z
    x = pecarray[:,0] # This is magnitude of force F0
    y = pecarray[:,1] # This is gammaP value
    z = pecarray[:,2] # This is the corresponding Peclet number
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    ax.plot_trisurf(x, y, z)
    
###############################################################################
# Secton 3: Plotting
###############################################################################
        
# Now all that's left is plotting the points together
def phiplot():     
    for i in range(0,len(forcelist)):
        # Now we're doing the same thing as last section with data...
        tempforcearray = darray[darray[:,0] == forcelist[i]]
        #...but also doing the same thing for pulling the A and phi0 values
        tempfitarray = fittedarray[fittedarray[:,0] == forcelist[i]]
        for j in range(0,len(gammalist)):
            tempgammaarray = tempforcearray[tempforcearray[:,1]==gammalist[j]]
            tmpfitarray2 = tempfitarray[tempfitarray[:,1] == gammalist[j]]
            
            aaa = len(gammalist)
            color = ((aaa-j)/aaa,0,j/aaa)
            plt.plot(tempgammaarray[:,2],tempgammaarray[:,3],'o',color=color,label=r"$\Gamma' = %s\omega_r$" % gammalist[j])
            ydata = func(tempgammaarray[:,2],tmpfitarray2[0,2],tmpfitarray2[0,3])
            plt.plot(tempgammaarray[:,2],ydata,color=color)
            
        plt.legend()
        plt.ylabel(r'$Average\ velocity\ \langle v\rangle /v_r$')
        plt.xlabel(r'$\phi\ (radians)$')
        plt.title(r'$Average\ velocity\ for\ F_o = %s$' % forcelist[i])
        plt.show()
    
# Now we'll plot the A and phi0 values
# Start with A
def AplotA():
    for i in range(0,len(forcelist)):
        tempforcearray = fittedarray[fittedarray[:,0] == forcelist[i]]
        plt.plot(tempforcearray[:,1],tempforcearray[:,2],label=r"$F_o = %s$" %forcelist[i])
        
    plt.xlabel(r"$\Gamma'/\omega_r$")
    plt.ylabel(r"$A$")
    plt.title(r'$Fitted\ amplitude$')
    plt.legend()
    plt.show()
def AplotB():
    for i in range(0,len(gammalist)):
        tempgammaarray = fittedarray[fittedarray[:,1] == gammalist[i]]
        plt.plot(tempgammaarray[:,0],tempgammaarray[:,2],label=r"$\Gamma'=%s\omega_r$" % gammalist[i])
    plt.xlabel(r"$F_o/E_r$")
    plt.ylabel(r"$A$")
    plt.title(r'$Fitted\ amplitude$')
    plt.legend()
    plt.show()

# And now the phi0 values
def phiplotA():
    for i in range(0,len(forcelist)):
        tempforcearray = fittedarray[fittedarray[:,0] == forcelist[i]]
        plt.plot(tempforcearray[:,1],tempforcearray[:,3],label=r"$F_o = %s$" %forcelist[i])
    plt.xlabel(r"$\Gamma'/\omega_r$")
    plt.ylabel(r"$\phi_o$")
    plt.title(r'$Fitted\ phase\ difference$')
    plt.legend()
    plt.show()

def phiplotB():
    for i in range(0,len(gammalist)):
        tempgammaarray = fittedarray[fittedarray[:,1] == gammalist[i]]
        plt.plot(tempgammaarray[:,0],tempgammaarray[:,3],label=r"$\Gamma'=%s\omega_r$" % gammalist[i])
    plt.xlabel(r"$F_o/E_r$")
    plt.ylabel(r"$\phi_o$")
    plt.title(r'$Fitted\ phase\ difference$')    
    plt.legend()
    plt.show()

# Here is the tkinter/menu mini-section
# All plotting should be defined as functions
# Attach those functions to buttons in a pop-up menu
# Allows individualized and specific plotting
    
# Version 4.2 is looking to turn the tk section into a class rather than lines
# Goal is to fix the bug where an extra tk window pops up

root = tk.Tk()
frame = tk.Frame(root)
frame.pack()


plotopt1 = tk.Button(frame,text="Phi plot",command=phiplot)
plotopt1.pack()
plotopt2 = tk.Button(frame,text="Amplitude versus gamma",command=AplotA)
plotopt2.pack()
plotopt3 = tk.Button(frame,text="Amplitude versus force",command=AplotB)
plotopt3.pack()
plotopt4 = tk.Button(frame,text="Phase versus gamma",command=phiplotA)
plotopt4.pack()
plotopt5 = tk.Button(frame,text="Phase versus force",command=phiplotB)
plotopt5.pack()
button = tk.Button(frame,text="(Click to exit)",fg="red",command=root.destroy)
button.pack(side="bottom")

tk.mainloop()