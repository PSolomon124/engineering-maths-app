from sympy import symbols, Function, Eq, dsolve

def solve_ode(expr_str, func_str, var_str):
    x = symbols(var_str)
    f = Function(func_str)(x)
    eq = Eq(eval(expr_str), 0)
    sol = dsolve(eq, f)
    return sol
