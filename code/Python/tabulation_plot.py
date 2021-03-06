#! usr/bin/env python
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Patch
from matplotlib.lines import Line2D

# mode = 1 if plotting hoppet default data, 2 if individual PDFs, 2.1 if plotting u from multiple files, 2.2 if plotting g from multiple files
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
    
    plotfile = "../../paper/figures/unevolved.pdf"
    with open("../data/allNLO-175-250-0.01-0.01.txt") as f:
        lines = f.readlines()
        for line in lines:
            for vals in data:
                vals.append(float((line[: line.find('  ')])))
                line = line[line.find('  ') + 2: ]
    
    data = np.array(data)
    for i in range(1,14):
        data[i] = data[i]/data[0]
    
    plt.xlabel('z', fontsize=20)
    plt.ylabel('J(z)', fontsize=15)
    plt.xscale('log')
    #plt.yscale('log')
    plt.xlim(0.01,1.05)
    plt.ylim(-10,10)
    plt.title('(Nearly) Unevolved Functions',fontsize=12)
    
    if (tvals != [0.0]*len(tvals)):
        plt.plot(data[0], data[1], 'bo-', label = "$t$")
    if (tbarvals != [0.0]*len(tbarvals)):
        plt.plot(data[0], data[2], 'b^--', label = "$\\bar{t}$")
    if (bvals != [0.0]*len(bvals)):
        plt.plot(data[0], data[3], 'ro:', label = "$b$")
    if (bbarvals != [0.0]*len(bbarvals)):
        plt.plot(data[0], data[4], 'r^--', label = "$\\bar{b}$")
    if (cvals != [0.0]*len(cvals)):
        plt.plot(data[0], data[5], 'go:', label = "$c$")
    if (cbarvals != [0.0]*len(cbarvals)):
        plt.plot(data[0], data[6], 'g^--', label = "$\\bar{c}$")
    if (svals != [0.0]*len(svals)):
        plt.plot(data[0], data[7], 'mo:', label = "$s$")
    if (sbarvals != [0.0]*len(sbarvals)):
        plt.plot(data[0], data[8], 'm^--', label = "$\\bar{s}$")
    if (uvals != [0.0]*len(uvals)):
        plt.plot(data[0], data[9], 'co-', label = "$u$")
    if (ubarvals != [0.0]*len(ubarvals)):
        plt.plot(data[0], data[10], 'c^--', label = "$\\bar{u}$")
    if (dvals != [0.0]*len(dvals)):
        plt.plot(data[0], data[11], 'yo:', label = "$d$")
    if (dbarvals != [0.0]*len(dbarvals)):
        plt.plot(data[0], data[12], 'y^--', label = "$\\bar{d}$")
    if (gvals != [0.0]*len(gvals)):
        plt.plot(data[0], data[13], 'ko-', label = "$g$")
        
    plt.legend(bbox_to_anchor=(1,0), loc=3)
        
""" Plotting uvals from multiple files """
if (mode == 2.1):
    plotfile = "../../paper/figures/NLO-quark-0.pdf"
    filenames = ["../data/qNLO-250-250-0.01-0.01.txt",
                 "../data/qNLO-247.5-250-0.01-0.01.txt",
                 "../data/qNLO-175-250-0.01-0.01.txt",
                 "../data/qNLO-125-250-0.01-0.01.txt",
                 "../data/qNLO-75-250-0.01-0.01.txt",
                 "../data/qNLO-25-250-0.01-0.01.txt",
                 "../data/qNLO-12.5-250-0.01-0.01.txt"]
    labels = []
    for filename in filenames:
#        label = "Q0 = " + filename[12 : filename.find("-",12)]
#        shortname = filename[filename.find("-",12) + 1 :]
#        label = label + ", Q = " + shortname[: shortname.find("-")]
#        shortname = shortname[shortname.find("-") + 1 :]
#        label = label + ", dy = " + shortname[: shortname.find("-")]
#        shortname = shortname[shortname.find("-") + 1 :]
#        label = label + ", dlnlnQ = " + shortname[: shortname.find(".t")]
        shortname = filename[filename.find("-",13) + 1 :]
        Q0 = filename[13 : filename.find("-",13)]
        Q = shortname[: shortname.find("-")]
        R = str(float(Q0)/float(Q))
        if (R == "1.0"):
            labels.append("Almost unevolved")
        else:
            labels.append("R = " + str(float(Q0)/float(Q)))
#        if (shortname[: shortname.find("-")] == "10"):
#            labels.append("Q = 10+1e-8")
#        else:
#            labels.append("Q = " + shortname[: shortname.find("-")])
      
#    ## Custom version for plotting large number of datasets
#    colors = ['m:o','m:v','m:^','m:*','m--x','b:o','b:v','b:^','b:*','b--x',
#              'g:o','g:v','g:^','g:*','g--x','r:o','r:v','r:^','r:*','r--x']
#    legendElements = [Line2D([0],[0], color='k', linestyle=':', marker='o', label='dlnlnQ = 0.001'),
#                      Line2D([0],[0], color='k', linestyle=':', marker='v', label='dlnlnQ = 0.01'),
#                      Line2D([0],[0], color='k', linestyle=':', marker='^', label='dlnlnQ = 0.05'),
#                      Line2D([0],[0], color='k', linestyle=':', marker='*', label='dlnlnQ = 0.1'),
#                      Line2D([0],[0], color='k', linestyle='--', marker='x', label='dlnlnQ = 0.5'),
#                      Patch(facecolor='m', label='Q = 10+1e-8'),
#                      Patch(facecolor='b', label='Q = 40'),
#                      Patch(facecolor='g', label='Q = 70'),
#                      Patch(facecolor='r', label='Q = 100')]  
#    ##   
    
    plt.xlabel('z', fontsize=20)
    plt.ylabel('J(z)', fontsize=15)
    plt.xscale('log')
    #plt.yscale('log')
    plt.xlim(0.01,1.05)
    plt.ylim(-10,10)
    plt.title('NLO quark evolution, $J(1) = 0$',fontsize=15)
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
    
    for i in range(np.shape(uvals)[0]):
        if not (np.array_equal(uvals[i],np.zeros(np.shape(uvals[i])[0]))):
            plt.plot(xvals[i], uvals[i], '-', label = labels[i])
    plt.legend(bbox_to_anchor=(1,.3), loc=3)
    
#    ## Custom version for plotting large number of datasets
#    for i in range(np.shape(uvals)[0]):
#        if not (np.array_equal(uvals[i],np.zeros(np.shape(uvals[i])[0]))):
#            plt.plot(xvals[i], uvals[i], colors[i])
#    plt.legend(handles=legendElements, bbox_to_anchor=(0, 1), ncol=2, loc=3)
#    ##

""" Plotting gvals from multiple files """
if (mode == 2.2):
    plotfile = "../../paper/figures/NLO-gluon-60000.pdf"
    filenames = ["../data/gNLO-250-250-0.01-0.01.txt",
                 "../data/gNLO-247.5-250-0.01-0.01.txt",
                 "../data/gNLO-175-250-0.01-0.01.txt",
                 "../data/gNLO-125-250-0.01-0.01.txt",
                 "../data/gNLO-75-250-0.01-0.01.txt",
                 "../data/gNLO-25-250-0.01-0.01.txt",
                 "../data/gNLO-12.5-250-0.01-0.01.txt"]
    labels = []
    for filename in filenames:
#        label = "Q0 = " + filename[12 : filename.find("-",12)]
#        shortname = filename[filename.find("-",12) + 1 :]
#        label = label + ", Q = " + shortname[: shortname.find("-")]
#        shortname = shortname[shortname.find("-") + 1 :]
#        label = label + ", dy = " + shortname[: shortname.find("-")]
#        shortname = shortname[shortname.find("-") + 1 :]
#        label = label + ", dlnlnQ = " + shortname[: shortname.find(".t")]
        shortname = filename[filename.find("-",13) + 1 :]
        Q0 = filename[13 : filename.find("-",13)]
        Q = shortname[: shortname.find("-")]
        R = str(float(Q0)/float(Q))
        if (R == "1.0"):
            labels.append("Almost unevolved")
        else:
            labels.append("R = " + str(float(Q0)/float(Q)))
#        if (shortname[: shortname.find("-")] == "10"):
#            labels.append("Q = 10+1e-8")
#        else:
#            labels.append("Q = " + shortname[: shortname.find("-")])
      
#    ## Custom version for plotting large number of datasets
#    colors = ['m:o','m:v','m:^','m:*','m--x','b:o','b:v','b:^','b:*','b--x',
#              'g:o','g:v','g:^','g:*','g--x','r:o','r:v','r:^','r:*','r--x']
#    legendElements = [Line2D([0],[0], color='k', linestyle=':', marker='o', label='dlnlnQ = 0.001'),
#                      Line2D([0],[0], color='k', linestyle=':', marker='v', label='dlnlnQ = 0.01'),
#                      Line2D([0],[0], color='k', linestyle=':', marker='^', label='dlnlnQ = 0.05'),
#                      Line2D([0],[0], color='k', linestyle=':', marker='*', label='dlnlnQ = 0.1'),
#                      Line2D([0],[0], color='k', linestyle='--', marker='x', label='dlnlnQ = 0.5'),
#                      Patch(facecolor='m', label='Q = 10+1e-8'),
#                      Patch(facecolor='b', label='Q = 40'),
#                      Patch(facecolor='g', label='Q = 70'),
#                      Patch(facecolor='r', label='Q = 100')]  
#    ##   
    
    plt.xlabel('z', fontsize=20)
    plt.ylabel('J(z)', fontsize=15)
    plt.xscale('log')
    #plt.yscale('log')
    plt.xlim(0.01,1.05)
    plt.ylim(-15,10)
    plt.title('NLO gluon evolution, $J(1) = -60000$',fontsize=15)
    xvals = []
    gvals = []
    
    for filename in filenames:
        xvals.append([])
        gvals.append([])
        with open(filename) as f:
            lines = f.readlines()
            for line in lines:
                xvals[len(gvals)-1].append(float((line[: line.find('  ')])))
                for i in range(13):
                    line = line[line.find('  ') + 2: ] 
                gvals[len(gvals)-1].append(float((line[: line.find('  ')])))
    
    gvals = np.array(gvals)
    xvals = np.array(xvals)
    gvals = gvals/xvals   
    
    for i in range(np.shape(gvals)[0]):
        if not (np.array_equal(gvals[i],np.zeros(np.shape(gvals[i])[0]))):
            plt.plot(xvals[i], gvals[i], '-', label = labels[i])
    plt.legend(bbox_to_anchor=(1,.3), loc=3)
    
#    ## Custom version for plotting large number of datasets
#    for i in range(np.shape(gvals)[0]):
#        if not (np.array_equal(gvals[i],np.zeros(np.shape(gvals[i])[0]))):
#            plt.plot(xvals[i], gvals[i], colors[i])
#    plt.legend(handles=legendElements, bbox_to_anchor=(0, 1), ncol=2, loc=3)
#    ##

plt.savefig(plotfile, bbox_inches = "tight")