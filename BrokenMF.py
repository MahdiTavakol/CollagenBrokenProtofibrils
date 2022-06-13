#!/usr/bin/env python
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import csv
from mpl_toolkits.axes_grid1 import ImageGrid
from scipy import misc
import matplotlib.gridspec as gridspec
plt.rcParams.update({'errorbar.capsize': 2})
import os
from math import sqrt
import math
import statistics

outputwidth   = 3.7
outputheight  = 2.08
fontsize      = 8
lblfontsize   = 18
lblfontsize2  = 10
linewidth     = 2.5
lgndmarkersize= 3.5
markersize    = 5
linelength    = 5
lgndmarkersize = 5
elinewidth     = 1
fontweight     = 'bold'
xMax           = 80

def distance(x,y,z,a,b,c):
	return sqrt((x-a)*(x-a)+(y-b)*(y-b)+(z-c)*(z-c))


#Just for debugging, it should be turned off
plt.ioff()


# Create the figure
fig, ax = plt.subplots(1,1)

Step = []
Broken = []
brokenCids = []
cutoff = 21*1.0



with open("../dump.defo.lammpstrj", 'r') as eqFile :
	dump = eqFile.readlines()
tsFound = False
numAtoms = 0
xmin = xmax = ymin = ymax = zmin = zmax = 0.0
for i in range(len(dump)):
	line = dump[i]
	if "ITEM: TIMESTEP" in line:
		ts = int(dump[i+1])
		i = i + 1
		if ((ts%400000)==0):
			tsFound = True
			print "working on frame " , ts
	elif "ITEM: NUMBER OF ATOMS" in line:
		numAtoms = int(dump[i+1])
		i = i + 1
	elif "ITEM: BOX BOUNDS" in line:
		line = dump[i+1].split()
		i = i + 1
		xmin = float(line[0])
		xmax = float(line[1])
		line = dump[i+1].split()
		i = i + 1
		ymin = float(line[0])
		ymax = float(line[1])
		line = dump[i+1].split()
		i = i + 1
		zmin = float(line[0])
		zmax = float(line[1])
	elif "ITEM: ATOMS" in line:
		if tsFound == False :
			i = i + numAtoms
		else :
			#if (ts == 15600000):
			#	break
			tsFound = False
			#X   = []
			#Y   = []
			Z   = []
			Aid = []

			for j in range(numAtoms):
				#print j
				i = i + 1
				line   = dump[i].split()
				aid    = int(line[1])-1 # The Lammps has 1-based indexing system
				pType  = int(line[2])
				if (pType == 1):
					if (True):
						#x      = float(line[3])
						#y      = float(line[4])
						z      = float(line[5])
						#x      = xmin + (xmax-xmin)*x
						#y      = ymin + (ymax-ymin)*y
						z      = zmin + (zmax-zmin)*z
						#X.append(x)
						#Y.append(y)
						Z.append(z)
						Aid.append(aid)

			for l in range(0,len(Aid)):
				a = Aid[l]
				c = int(a/219)
				if (c in brokenCids):
					continue
				if (a%219 == 0):
					continue
				if a-1 in Aid:
					if (Z[l] < Z[Aid.index(a-1)]):
						Z[l] = Z[l] + zmax - zmin
					dist1 = abs(Z[l]-Z[Aid.index(a-1)])
					dist2 = abs(dist1 - (zmax-zmin))
					dist = min([dist1,dist2])
					#dist = distance(X[l],Y[l],Z[l],X[Aid.index(a-1)],Y[Aid.index(a-1)],Z[Aid.index(a-1)])
					if (dist > cutoff):
						brokenCids.append(c)
			broken = len(brokenCids)
			Step.append(ts/400000)
			Broken.append(broken)
Broken0 = Broken[0]
for i in range(0,len(Broken)):
	Broken[i] = Broken[i] - Broken0


with open('BrokenMFs.csv', 'w') as csvfilew:
	plotsw = csv.writer(csvfilew,delimiter=',')
	plotsw.writerow(["Strain(%)","BrokenMF(#)"])
	plotsw.writerows(zip(Step,Broken))

color = 'blue'
ax.scatter( Step, Broken, s=0.8,alpha=1, marker='o', c = color)
#ax.set_xlim(0,max(Step))
#ax.set_ylim(0,max(Broken)+5)
#ax.set_xticks([])
ax.set_xlabel("Strain (%)",color='k',fontsize=fontsize, fontweight=fontweight)
ax.set_ylabel("Broken MFs (#)",fontsize=fontsize, fontweight=fontweight)


		
for axis in ['top','bottom','left','right']:
	ax.spines[axis].set_linewidth(2.5)

ax.xaxis.set_tick_params(width=2.5,length=5)
ax.yaxis.set_tick_params(width=2.5,length=5)
plt.xticks(fontsize=fontsize, fontweight=fontweight)
plt.yticks(fontsize=fontsize, fontweight=fontweight)

fig.tight_layout()

plt.subplots_adjust(top=0.95, bottom=0.12, left=0.18, right=0.95, hspace=0.,wspace=0.05)

#Setting the output resolution
fileName = "BrokenMFs"
fig.set_dpi(300)
fig.set_size_inches(outputwidth, outputheight)
fig.savefig(fileName+"-test.tif")

# Compressing the image
command = "tiffcp -c lzw " + fileName + "-test.tif " +fileName + ".tif"
os.popen(command)
command = "rm " + fileName + "-test.tif"
os.popen(command)


