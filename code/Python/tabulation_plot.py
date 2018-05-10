#! usr/bin/env python
import matplotlib.pyplot as plt

# mode = 1 if plotting hoppet default data, 2 if individual PDFs
mode = 2

""" Plotting hoppet's default data """
if (mode == 1):
    xvals = []
    uvals = [] # u-ubar
    dvals = [] # d-dbar
    udvals = [] # 2*(ubar+dbar)
    cvals = [] # c-cbar
    gvals = [] # gluon
    data = [xvals, uvals, dvals, udvals, cvals, gvals]
    
    with open("pdf.txt") as f:
        lines = f.readlines()
        for line in lines:
            for vals in data:
                vals.append(float((line[: line.find('  ')])))
                line = line[line.find('  ') + 2: ]
    
    plt.xlabel('x')
    plt.ylabel('J(x)')
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
    
    with open("pdf.txt") as f:
        lines = f.readlines()
        for line in lines:
            for vals in data:
                vals.append(float((line[: line.find('  ')])))
                line = line[line.find('  ') + 2: ]
    
    plt.xlabel('x')
    plt.ylabel('J(x)')
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
        plt.plot(xvals, uvals, 'co:')
    if (ubarvals != [0.0]*len(ubarvals)):
        plt.plot(xvals, ubarvals, 'co--')
    if (dvals != [0.0]*len(dvals)):
        plt.plot(xvals, dvals, 'yo:')
    if (dbarvals != [0.0]*len(dbarvals)):
        plt.plot(xvals, dbarvals, 'yo--')
    if (gvals != [0.0]*len(gvals)):
        plt.plot(xvals, gvals, 'ko--')