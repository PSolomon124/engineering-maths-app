import numpy as np
from scipy.optimize import fsolve, root_scalar
from scipy.integrate import quad

def find_root(func, x0):
    return fsolve(func, x0)

def numerical_integral(func, a, b):
    result, _ = quad(func, a, b)
    return result
