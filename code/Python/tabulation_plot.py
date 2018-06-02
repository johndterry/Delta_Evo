#! usr/bin/env python
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Patch
from matplotlib.lines import Line2D

# mode = 1 if plotting hoppet default data, 2 if individual PDFs, 2.1 if plotting u from multiple files
mode = 2.1

""" Plotting hoppet's default data """
if (mode == 1):
    xvals = []
    uvals = [] # u-ubar
    dvals = [] # d-dbar
    udvals = [] # 2*(ubar+dbar)
    cvals = [] # c-cbar
    gvals = [] # gluon
    data = [xvals, uvals, dvals, udvals, cvals, gvals]
    
    with open("../data/pdf-1.41421-1.41421-0.01.txt") as f:
        lines = f.readlines()
        for line in lines:
            for vals in data:
                vals.append(float((line[: line.find('  ')])))
                line = line[line.find('  ') + 2: ]
    
    plt.set_xlabel('x', fontsize=20)
    plt.ylabel('J(x)', fontsize=15)
    plt.xscale('log')
    plt.yscale('log')
    plt.plot(xvals, uvals, 'bo-')
    plt.plot(xvals, dvals, 'ro-')
    plt.plot(xvals, udvals, 'mo-')
    plt.plot(xvals, cvals, 'go-')
    plt.plot(xvals, gvals, 'ko-')

""" Plotting individual PDF functions """
if (mode == 2):
    xvals = []
    tvals = []
    tbarvals = []
    bvals = []
    bbarvals = []
    cvals = []
    cbarvals = []
    svals = []
    sbarvals = []
    uvals = []
    ubarvals = []
    dvals = []
    dbarvals = []
    gvals = []
    data = [xvals, tvals, tbarvals, bvals, bbarvals, cvals, cbarvals, svals, sbarvals, uvals, ubarvals, dvals, dbarvals, gvals]
    
    with open("../data/pdf-1.41421-100-0.01.txt") as f:
        lines = f.readlines()
        for line in lines:
            for vals in data:
                vals.append(float((line[: line.find('  ')])))
                line = line[line.find('  ') + 2: ]
    
    plt.xlabel('x', fontsize=20)
    plt.ylabel('J(x)', fontsize=15)
    plt.xscale('log')
    plt.yscale('log')
    if (tvals != [0.0]*len(tvals)):
        plt.plot(xvals, tvals, 'bo:')
    if (tbarvals != [0.0]*len(tbarvals)):
        plt.plot(xvals, tbarvals, 'bo--')
    if (bvals != [0.0]*len(bvals)):
        plt.plot(xvals, bvals, 'ro:')
    if (bbarvals != [0.0]*len(bbarvals)):
        plt.plot(xvals, bbarvals, 'ro--')
    if (cvals != [0.0]*len(cvals)):
        plt.plot(xvals, cvals, 'go:')
    if (cbarvals != [0.0]*len(cbarvals)):
        plt.plot(xvals, cbarvals, 'go--')
    if (svals != [0.0]*len(svals)):
        plt.plot(xvals, svals, 'mo:')
    if (sbarvals != [0.0]*len(sbarvals)):
        plt.plot(xvals, sbarvals, 'mo--')
    if (uvals != [0.0]*len(uvals)):
        plt.plot(xvals, uvals, 'co-')
    if (ubarvals != [0.0]*len(ubarvals)):
        plt.plot(xvals, ubarvals, 'co--')
    if (dvals != [0.0]*len(dvals)):
        plt.plot(xvals, dvals, 'yo:')
    if (dbarvals != [0.0]*len(dbarvals)):
        plt.plot(xvals, dbarvals, 'yo--')
    if (gvals != [0.0]*len(gvals)):
        plt.plot(xvals, gvals, 'ko--')
        
""" Plotting uvals from multiple files """
if (mode == 2.1):
    filenames = ["../data/pdf-10-10-0.01-0.001.txt",
                 "../data/pdf-10-10-0.01-0.01.txt",
                 "../data/pdf-10-10-0.01-0.05.txt",
                 "../data/pdf-10-10-0.01-0.1.txt",
                 "../data/pdf-10-10-0.01-0.5.txt",
                 "../data/pdf-10-40-0.01-0.001.txt",
                 "../data/pdf-10-40-0.01-0.01.txt",
                 "../data/pdf-10-40-0.01-0.05.txt",
                 "../data/pdf-10-40-0.01-0.1.txt",
                 "../data/pdf-10-40-0.01-0.5.txt",
                 "../data/pdf-10-70-0.01-0.001.txt",
                 "../data/pdf-10-70-0.01-0.01.txt",
                 "../data/pdf-10-70-0.01-0.05.txt",
                 "../data/pdf-10-70-0.01-0.1.txt",
                 "../data/pdf-10-70-0.01-0.5.txt",
                 "../data/pdf-10-100-0.01-0.001.txt",
                 "../data/pdf-10-100-0.01-0.01.txt",
                 "../data/pdf-10-100-0.01-0.05.txt",
                 "../data/pdf-10-100-0.01-0.1.txt",
                 "../data/pdf-10-100-0.01-0.5.txt"]
    labels = []
#    for filename in filenames:
#        label = "Q0 = " + filename[12 : filename.find("-",12)]
#        shortname = filename[filename.find("-",12) + 1 :]
#        label = label + ", Q = " + shortname[: shortname.find("-")]
#        shortname = shortname[shortname.find("-") + 1 :]
#        label = label + ", dy = " + shortname[: shortname.find("-")]
#        shortname = shortname[shortname.find("-") + 1 :]
#        label = label + ", dlnlnQ = " + shortname[: shortname.find(".t")]
#        labels.append(label)
      
    ## Custom version for plotting large number of datasets
    colors = ['m:o','m:v','m:^','m:*','m--x','b:o','b:v','b:^','b:*','b--x',
              'g:o','g:v','g:^','g:*','g--x','r:o','r:v','r:^','r:*','r--x']
    legendElements = [Line2D([0],[0], color='k', linestyle=':', marker='o', label='dlnlnQ = 0.001'),
                      Line2D([0],[0], color='k', linestyle=':', marker='v', label='dlnlnQ = 0.01'),
                      Line2D([0],[0], color='k', linestyle=':', marker='^', label='dlnlnQ = 0.05'),
                      Line2D([0],[0], color='k', linestyle=':', marker='*', label='dlnlnQ = 0.1'),
                      Line2D([0],[0], color='k', linestyle='--', marker='x', label='dlnlnQ = 0.5'),
                      Patch(facecolor='m', label='Q = 10+1e-8'),
                      Patch(facecolor='b', label='Q = 40'),
                      Patch(facecolor='g', label='Q = 70'),
                      Patch(facecolor='r', label='Q = 100')]  
    ##   
    
    plt.xlabel('x', fontsize=20)
    plt.ylabel('u(x)', fontsize=15)
    plt.xscale('log')
    plt.yscale('log')
    xvals = []
    uvals = []
    
    for filename in filenames:
        xvals.append([])
        uvals.append([])
        with open(filename) as f:
            lines = f.readlines()
            for line in lines:
                xvals[len(uvals)-1].append(float((line[: line.find('  ')])))
                for i in range(9):
                    line = line[line.find('  ') + 2: ] 
                uvals[len(uvals)-1].append(float((line[: line.find('  ')])))
    
    uvals = np.array(uvals)
    xvals = np.array(xvals)
    uvals = uvals/xvals   
    
#    for i in range(np.shape(uvals)[0]):
#        if not (np.array_equal(uvals[i],np.zeros(np.shape(uvals[i])[0]))):
#            plt.plot(xvals[i], uvals[i], label = labels[i])
    
    ## Custom version for plotting large number of datasets
    for i in range(np.shape(uvals)[0]):
        if not (np.array_equal(uvals[i],np.zeros(np.shape(uvals[i])[0]))):
            plt.plot(xvals[i], uvals[i], colors[i])
    plt.legend(handles=legendElements, bbox_to_anchor=(0, 1), ncol=2, loc=3)
    ##
                
    #plt.legend(bbox_to_anchor=(0, 1), loc=3)
    plt.savefig("../../paper/figures/dlnlnQ-fourQs.pdf", bbox_inches = "tight")