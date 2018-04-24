# Integrating using right Riemann sum
# Used for integral from 1-a to 1 of (1 - (1-a)/x) * J(z/x, mu) dx
# z = array of n+1 points in descending order from 1 to zn: (1 = z0, z1, z2, ..., zn)
def rightIntegrate(f, z, a):
    total = 0
    n = len(z) - 1
    end = 0
    
    for i in range(n, -1, -1):
        if z[n]/z[i] <= (1 - a):
            end = i + 1
            break
        
    for i in range(n, end, -1):
        total += (z[n]/z[i] - z[n]/z[i-1]) * (1 - (1-a)*z[i]/z[n]) * f(z[i])
        
    total += (z[n]/z[end] - 1 + a) * (1 - (1-a)*z[end]/z[n]) * f(z[end])
    
    return total

# Testing
    
def testFunc(x):
    return x

def fRange(start, stop, dif):
    frange = []
    current = start
    frange.append(current)
    current += dif
    if dif > 0:
        while current < stop:
            frange.append(current)
            current += dif
    else:
        while current > stop:
            frange.append(current)
            current += dif
    return frange

testPoints = fRange(1, 1, -0.001)
testBound = 0.1

# print rightIntegrate(testFunc, testPoints, testBound)