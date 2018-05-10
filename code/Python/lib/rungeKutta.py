#!/usr/bin/env python
# Runge-Kutta method of order 4 
import math

# Approximates y(t) over [a,b] at n + 1 points, given y(a) = init and fpr(t,y) = dy/dt
def rungeKutta(fpr, a, b, n, init):
    dif = (b - a)/float(n)
    current = a                    # current = start of current interval
    approx = [init]                # approx[i] = approximation after i intervals

    for i in range(1, n+1):
        k1 = dif * fpr(current, approx[i-1])
        k2 = dif * fpr(current + dif/2, approx[i-1] + k1/2)
        k3 = dif * fpr(current + dif/2, approx[i-1] + k2/2)
        k4 = dif * fpr(current + dif, approx[i-1] + k2/2 + k3/2)
        approx.append(approx[i-1] + (k1 + 2*k2 + 2*k3 + k4)/6)
        current += dif
        
    return approx

# evolFunc = RHS(mu, zarray, fun_array)
# fun_array[str(mu0)] = [delta(z, a) for z in zarray]
def jetRungeKutta(evolFunc, initial, mu0, muf, dmu, zarray, init_fn):
    fun_array = {}
    fun_array[str(mu0)] = init_fn
    n = int((muf - mu0)/dmu)     
    mu = mu0                    # current = start of current interval
    length = len(zarray)

    for i in range(1, n+1):
        if i == 1:
            k1 = initial
        else:
            k1 = evolFunc(mu, fun_array[str(mu)])
        fun_array[str(mu + dmu/2)] = [dmu*k1[j]/2 + fun_array[str(mu)][j] for j in range(length)]
        k2 = evolFunc(mu + dmu/2, fun_array[str(mu + dmu/2)])
        fun_array[str(mu + dmu/2)] = [dmu*k2[j]/2 + fun_array[str(mu)][j] for j in range(length)]
        k3 = evolFunc(mu + dmu/2, fun_array[str(mu + dmu/2)])
        fun_array[str(mu + dmu)] = [dmu*k3[j] + fun_array[str(mu)][j] for j in range(length)]
        k4 = evolFunc(mu + dmu, fun_array[str(mu + dmu)])
        fun_array[str(mu + dmu)] = [fun_array[str(mu)][j] + dmu*(k1[j] + 2*k2[j] + 2*k3[j] + k4[j])/6 for j in range(length)]
        mu += dmu
    return fun_array

# Double variable version
# Approximates y(t,z) over [t0,t1],[z0,z1] at n + 1 points, given y(t0,z0) = init
# fpr is a function of (t, z, y)
# Implicitly varying z linearly with t; not sure this is justified
def rungeKuttaDouble(fpr, t0, t1, z0, z1, n, init):
    dif = (t1 - t0)/float(n)
    difz = (z1 - z0)/float(n)
    currentt = t0                  
    currentz = z0
    approx = [init]                
    
    for i in range(1, n+1):
        k1 = dif * fpr(currentt, currentz, approx[i-1])
        k2 = dif * fpr(currentt + dif/2, currentz + difz/2, approx[i-1] + k1/2)
        k3 = dif * fpr(currentt + dif/2, currentz + difz/2, approx[i-1] + k2/2)
        k4 = dif * fpr(currentt + dif, currentz + difz, approx[i-1] + k3)
        approx.append(approx[i-1] + (k1 + 2*k2 + 2*k3 + k4)/6)
        currentt += dif
        currentz += difz
        
    return approx

# Testing 

def testFunc(t, y):
    return y - t*t + 1

def testFuncDouble(t, z, y):
    return y - t*t + 1 + z

# print rungeKutta(testFunc, 1, 3, 100, 0.5)
# print rungeKuttaDouble(testFuncDouble, 1, 3, 1, 3, 100, 0.5)