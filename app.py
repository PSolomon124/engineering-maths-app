import streamlit as st
import google.generativeai as genai
import random

# Configure API
gemini_api_key = st.secrets["gemini"]["api_key"]
genai.configure(api_key=gemini_api_key)

# Load Gemini model
model = genai.GenerativeModel("gemini-1.5-flash")

# Sample engineering maths questions
questions = [
    "Solve for x: 5x + 7 = 27",
    "Find the derivative of f(x) = 3x^3 + 2x^2 - 5x + 7",
    "Evaluate the integral ∫ (2x^2 + 3x - 4) dx",
    "A particle moves such that s(t) = t^3 - 6t^2 + 9t. Find velocity and acceleration at t = 2.",
    "Find the Laplace transform of f(t) = e^(-2t) * sin(3t)",
    "If A = [[2,1],[3,4]], find det(A) and A⁻¹."
]

st.title("📘 Engineering Maths Tutor (Humanized Solutions)")
st.write("Generate random engineering maths problems with step-by-step solutions explained in a natural, human-like way.")

# Random question button
if st.button("🎲 Generate Random Question"):
    q = random.choice(questions)
    st.session_state["question"] = q

# Show current question
if "question" in st.session_state:
    st.subheader("Question:")
    st.write(st.session_state["question"])

    if st.button("🧾 Show Solution"):
        # Step 1: Generate AI solution
        solution = model.generate_content(
            f"Solve this engineering maths question step by step:\n{st.session_state['question']}"
        ).text

        # Step 2: Humanize the explanation
        humanized = model.generate_content(
            f"Rewrite the following explanation as if a human tutor is teaching a student. "
            f"Make it natural, avoid AI wording, and explain step-by-step like in a classroom:\n\n{solution}"
        ).text

        st.subheader("Solution:")
        st.write(humanized)
