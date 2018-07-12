#!/usr/bin/env python
# Approximating J(z,mu) using rungeKutta
import sys, os
cwd = os.getcwd()
sys.path.append(cwd+'/../') #appends library path for windows
import numpy as np
from lib.rungeKutta import jetRungeKutta
from scipy.integrate import quad, trapz
import pylab as py

# Delta function using heaviside theta
def delta(z, a):
    if (z > 1.0) or (z < 1.0 - a):
        return 0
    else:
        return 2/(a*a) * (z - 1.0 + a)

# Get initial value using quad (quad has great accuracy but will not be usable later)
def initial(zarray, mu0, a, alpha, C):
    leftIntegral = []
    rightIntegral = []
    for z in zarray:
        if z == 1.0:
            leftIntegral.append(0.0)
            rightIntegral.append(0.0)
        else:
            leftIntegral.append(quad(lambda x: (1+x**2)/(x*(1-x))*delta(z/x, a)-2/(1-x)*delta(z, a), z, 1)[0])
            rightIntegral.append(delta(z, a)/2.0) 
            
    RHS = []
    for i in range(len(rightIntegral)):
        if zarray[i] == 1.0:
            RHS.append(0.0)
        else:
            RHS.append((alpha * C)/(mu0 * np.pi) * (leftIntegral[i] + 2*delta(zarray[i], a)*np.log(1-zarray[i]) + 1.5*rightIntegral[i]))
    return RHS

def nearest(zarray, z, x):
    dz = zarray[2]-zarray[1]
    if z == x:
        return len(zarray) - 1
    for i in range(len(zarray)):
        if abs(zarray[i] - z/x) <= dz/1.9:
            return i
    return len(zarray) - 1

#Evolution using Riemann sums
def RHS(mu, zarray, init_fn, alpha, C):
    dz = zarray[2]-zarray[1]
    leftIntegral= []
    rightIntegral = []
    for i in range(len(zarray)):
        z = zarray[i]
        if z == 1.0:
            leftIntegral.append(0.0)
            rightIntegral.append(0.0)
        else:
            points = []
            for j in range(i, len(zarray)):
                x = zarray[j]
                if x == 1.0:
                    points.append(0.0)
                elif x == 0.0:
                    points.append((1+dz**2)/(dz*(1-dz))*init_fn[len(zarray)-1]-2/(1-dz)*init_fn[i])
                else:
                    points.append((1+x**2)/(x*(1-x))*init_fn[nearest(zarray, z, x)]-2/(1-x)*init_fn[i])
            leftIntegral.append(trapz(points, None, dz))
            rightIntegral.append(init_fn[i]/2.0)
            
    RHS = []
    for i in range(len(rightIntegral)):
        if zarray[i] == 1.0:
            RHS.append(0.0)
        else:
            RHS.append((alpha * C)/(mu * np.pi) * (leftIntegral[i] + 2*init_fn[i]*np.log(1-zarray[i]) + 1.5*rightIntegral[i]))
    return RHS

# QCD Parameters
alpha = 1e-1
C = 4.0/3.0

# Delta function parameters
a = 1e-2

# mu spacing
mu0 = 1e1
muf = 1e2
dmu = 0.5

# z spacing
z0 = 0.0
zf = 1.0
zn = 100
zarray = np.linspace(z0, zf, zn)

# Get fun_array
init_dJdmu = initial(zarray, mu0, a, alpha, C)
init_fn = [delta(z, a) for z in zarray]
evolFunc = lambda mu, prev_fn: RHS(mu, zarray, prev_fn, alpha, C)
fun_array = jetRungeKutta(evolFunc, init_dJdmu, mu0, muf, dmu, zarray, init_fn)

#Plot for values of mu
ax = py.subplot(131)
ax.set_xscale('log')
ax.plot(zarray, fun_array[str(mu0)])
ax.set_xlabel('z', fontsize=20)
ax.set_ylabel(r'J(\mu = 10, z)', fontsize=15)

ax = py.subplot(132)
ax.set_xscale('log')
ax.plot(zarray, fun_array[str((muf-mu0)/2)])
ax.set_xlabel('z', fontsize=20)
ax.set_ylabel(r'J(\mu = 45, z)', fontsize=15)

ax = py.subplot(133)
ax.set_xscale('log')
ax.plot(zarray, fun_array[str(muf)])
ax.set_xlabel('z', fontsize=20)
ax.set_ylabel(r'J(\mu = 100, z)', fontsize=15)

py.tight_layout()
cwd = os.getcwd()
#py.savefig(cwd+'/../paper/figures/Jmu1.pdf')
py.show()

# Plot for given z in zarray
#index = 1
#muspace = np.linspace(mu0, muf, int((muf - mu0)/dmu) + 1)
#soln = [fun_array[str(mu)][index] for mu in muspace]
#print 'z = ', zarray[index]
#ax3 = py.subplot(111)
#ax3.plot(muspace, soln)
#ax3.set_xlabel('$\mu$', fontsize=20)
#ax3.set_ylabel(r'J', fontsize=15)
#py.show()

# Plot for given mu in muspace
#index = 90
#muspace = np.linspace(mu0, muf, int((muf - mu0)/dmu) + 1)
#soln = fun_array[str(muspace[index])]
#print r'$\mu$ = ', muspace[index]
#ax4 = py.subplot(111)
#ax4.plot(zarray, soln)
#ax4.set_xlabel('z', fontsize=20)
#ax4.set_ylabel(r'J', fontsize=15)
#py.show()