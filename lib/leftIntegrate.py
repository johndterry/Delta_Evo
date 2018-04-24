# Integrating using left Riemann sum
# Used for integral from z to 1 of ((1 + x*x)/(x * (1-x)) * J(z/x, mu) - 2/(1-x) * J(z, mu)) dx
# z = array of n+1 points in descending order from 1 to zn: (1 = z0, z1, z2, ..., zn)
def leftIntegrate(f, z):
    total = 0
    n = len(z) - 1
    
    for i in range(1, n+1):
        total += (z[n]/z[i] - z[n]/z[i-1]) * ((1 + (z[n]/z[i-1])**2)/((z[n]/z[i-1]) * (1-(z[n]/z[i-1]))) * f(z[i-1]) - 2/(1-(z[n]/z[i-1])) * f(z[n]))
    return total
       
# Testing
 
def testFunc(x):
    return x

testPoints = [1, 0.95, 0.9, 0.85, 0.8, 0.75, 0.7, 0.65, 0.6, 0.55, 0.5]

# print leftIntegrate(testFunc, testPoints)