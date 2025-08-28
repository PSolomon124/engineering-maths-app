import streamlit as st
from utils import algebra, calculus, diff_eq, numerical
from langchain_google_genai import ChatGoogleGenerativeAI

st.set_page_config(page_title="Engineering Maths AI Assistant", layout="wide")

# Load Gemini API key
gemini_api_key = st.secrets["gemini"]["api_key"]
chat_model = ChatGoogleGenerativeAI(api_key=gemini_api_key, model="chat-bison-001")

def ask_gemini(question):
    try:
        response = chat_model.predict_messages([{"role": "user", "content": question}])
        return response.content
    except:
        return "Error: Could not get explanation from Gemini."

st.title("Engineering Mathematics Interactive App")

option = st.sidebar.selectbox(
    "Select Topic",
    ["Algebra", "Calculus", "Differential Equations", "Numerical Methods"]
)

if option == "Algebra":
    st.header("Linear Algebra Solver")
    eq_input = st.text_input("Enter equation (e.g., '2*x + 3 = 7'):")
    var_input = st.text_input("Variable (e.g., 'x'):")
    if st.button("Solve Algebra"):
        try:
            solution = algebra.solve_linear_eq(eq_input, var_input)
            st.success(f"Answer (Python computed): {solution}")
            question = f"Solve the equation {eq_input} step by step."
            explanation = ask_gemini(question)
            st.info(f"Explanation (Gemini AI): {explanation}")
        except:
            st.error("Invalid equation input.")

elif option == "Calculus":
    st.header("Calculus Operations")
    calc_option = st.radio("Operation", ["Derivative", "Integral"])
    expr_input = st.text_input("Enter expression (e.g., 'x**2 + 3*x'):")
    var_input = st.text_input("Variable (e.g., 'x'):")
    if st.button("Compute Calculus"):
        try:
            if calc_option == "Derivative":
                result = calculus.derivative(expr_input, var_input)
            else:
                result = calculus.integral(expr_input, var_input)
            st.success(f"Answer (Python computed): {result}")
            question = f"Compute the {calc_option.lower()} of {expr_input} with respect to {var_input} step by step."
            explanation = ask_gemini(question)
            st.info(f"Explanation (Gemini AI): {explanation}")
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
            st.success(f"Answer (Python computed): {solution}")
            question = f"Solve the ODE {eq_input} step by step."
            explanation = ask_gemini(question)
            st.info(f"Explanation (Gemini AI): {explanation}")
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
                st.success(f"Answer (Python computed): {root}")
                question = f"Find root of the function {func_input} starting at {x0} step by step."
                explanation = ask_gemini(question)
                st.info(f"Explanation (Gemini AI): {explanation}")
            except:
                st.error("Invalid function input.")
    else:
        st.info("Example: Define a function like lambda x: x**2")
        func_input = st.text_input("Enter function:")
        a = st.number_input("Lower limit:", value=0.0)
        b = st.number_input("Upper limit:", value=1.0)
        if st.button("Integrate Numerically"):
            try:
                func = eval(func_input)
                result = numerical.numerical_integral(func, a, b)
                st.success(f"Answer (Python computed): {result}")
                question = f"Compute the numerical integral of the function {func_input} from {a} to {b} step by step."
                explanation = ask_gemini(question)
                st.info(f"Explanation (Gemini AI): {explanation}")
            except:
                st.error("Invalid input.")
