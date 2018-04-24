# Adaptive Simpson's method integration of f(x) over [a,b]
import math

# Simpson's rule integration over an interval
def simpsons(f, a, b):
    return (b - a)/6 * (f(a) + 4*f((a + b)/2) + f(b))

# error = maximum tolerated error
def integrate(f, a, b, error):
    mid = (a + b)/2.0
    leftInt = simpsons(f, a, mid)
    rightInt = simpsons(f, mid, b)
    estimate = simpsons(f, a, b)
    if abs(estimate - leftInt - rightInt) <= 15.0 * error:
        return leftInt + rightInt + (estimate - leftInt - rightInt)/15.0
    return integrate(f, a, mid, error/2.0) + integrate(f, mid, b, error/2.0)

# Testing
    
def testFunc(x):
    return x*x + 2*math.sin(x)

# print integrate(testFunc, 0, 2, 0.01)