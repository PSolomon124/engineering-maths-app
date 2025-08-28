from sympy import symbols, diff, integrate

def derivative(expr_str, var_str):
    x = symbols(var_str)
    expr = eval(expr_str)
    return diff(expr, x)

def integral(expr_str, var_str):
    x = symbols(var_str)
    expr = eval(expr_str)
    return integrate(expr, x)
