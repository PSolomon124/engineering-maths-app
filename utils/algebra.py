from sympy import symbols, Eq, solve, Matrix

def solve_linear_eq(equation_str, var_str):
    x = symbols(var_str)
    eq = Eq(eval(equation_str.split('=')[0]), eval(equation_str.split('=')[1]))
    sol = solve(eq, x)
    return sol

def solve_matrix_eq(A_list, B_list):
    A = Matrix(A_list)
    B = Matrix(B_list)
    sol = A.LUsolve(B)
    return sol
