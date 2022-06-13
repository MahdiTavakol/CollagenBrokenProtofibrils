#!/usr/bin/env python
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import csv
from mpl_toolkits.axes_grid1 import ImageGrid
from scipy import misc
import matplotlib.gridspec as gridspec
plt.rcParams.update({'errorbar.capsize': 2})
import matplotlib.lines  as mlines
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


#Just for debugging, it should be turned off
plt.ioff()


# Create the figure
fig, ax = plt.subplots(1,1)

Strain    = []
MF        = []
StrainAvg = []
MFAvg     = []
MFErr     = []


Sims =["5-Series5","6-Series6","8-Series8","9-Series9"]

for sim in Sims:
	file = sim + "/dump/z-cId/BrokenMFs.csv"
	with open(file, 'r') as csvfile:
		plots = csv.reader(csvfile,delimiter=',')
		next(plots)
		for row in plots:
			Strain.append(float(row[0]))
			MF.append(float(row[1]))


for strain in Strain:
	if strain not in StrainAvg:
		StrainAvg.append(strain)


for strain in StrainAvg:
	br = []
	for i in range(len(Strain)):
		if (Strain[i] == strain):
			br.append(MF[i])
	if (len(br) < 2):
		break
	MFAvg.append(statistics.mean(br))
	MFErr.append(statistics.stdev(br))




color = 'blue'
ax.errorbar(StrainAvg[0:len(MFAvg)],MFAvg,yerr=MFErr, alpha= 0.8, fmt='bx', color=color , markersize=1.5,capthick=0.5,capsize=1.5,elinewidth=elinewidth-0.5)
#ax.set_xlim(0,xMax)
#ax.set_ylim(0,3)
ax.set_xlabel("Strain (%)",color='k',fontsize=fontsize, fontweight=fontweight)
ax.set_ylabel("Broken MF (#)",fontsize=fontsize, fontweight=fontweight)


		
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
