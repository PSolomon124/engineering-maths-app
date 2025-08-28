import streamlit as st
from utils import algebra, calculus, diff_eq, numerical
import matplotlib.pyplot as plt
import numpy as np

st.title("Engineering Mathematics Interactive App")

option = st.sidebar.selectbox(
    "Select Topic",
    ["Algebra", "Calculus", "Differential Equations", "Numerical Methods"]
)

if option == "Algebra":
    st.header("Linear Algebra Solver")
    eq_input = st.text_input("Enter equation (e.g., '2*x + 3 = 7'):")
    var_input = st.text_input("Variable (e.g., 'x'):")
    if st.button("Solve"):
        try:
            solution = algebra.solve_linear_eq(eq_input, var_input)
            st.success(f"Solution: {solution}")
        except:
            st.error("Invalid equation input.")

elif option == "Calculus":
    st.header("Calculus Operations")
    calc_option = st.radio("Operation", ["Derivative", "Integral"])
    expr_input = st.text_input("Enter expression (e.g., 'x**2 + 3*x'):")
    var_input = st.text_input("Variable (e.g., 'x'):")
    if st.button("Compute"):
        try:
            if calc_option == "Derivative":
                result = calculus.derivative(expr_input, var_input)
            else:
                result = calculus.integral(expr_input, var_input)
            st.success(f"Result: {result}")
        except:
            st.error("Invalid input.")

elif option == "Differential Equations":
    st.header("ODE Solver")
    eq_input = st.text_input("Enter ODE expression (e.g., 'f.diff(x) - f = 0'):")
    func_input = st.text_input("Function (e.g., 'f'):")
    var_input = st.text_input("Variable (e.g., 'x'):")
    if st.button("Solve ODE"):
        try:
            solution = diff_eq.solve_ode(eq_input, func_input, var_input)
            st.success(f"Solution: {solution}")
        except:
            st.error("Invalid ODE input.")

elif option == "Numerical Methods":
    st.header("Numerical Operations")
    num_option = st.radio("Operation", ["Root Finding", "Numerical Integration"])
    if num_option == "Root Finding":
        st.info("Example: Define a function like lambda x: x**2 - 4")
        func_input = st.text_input("Enter function:")
        x0 = st.number_input("Initial guess:", value=1.0)
        if st.button("Find Root"):
            try:
                func = eval(func_input)
                root = numerical.find_root(func, x0)
                st.success(f"Root: {root}")
            except:
                st.error("Invalid function input.")
    else:
        st.info("Example: Define a function like lambda x: x**2")
        func_input = st.text_input("Enter function:")
        a = st.number_input("Lower limit:", value=0.0)
        b = st.number_input("Upper limit:", value=1.0)
        if st.button("Integrate"):
            try:
                func = eval(func_input)
                result = numerical.numerical_integral(func, a, b)
                st.success(f"Integral Result: {result}")
            except:
                st.error("Invalid input.")
