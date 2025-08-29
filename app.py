import streamlit as st
import google.generativeai as genai
import random

# Load Gemini API key
gemini_api_key = st.secrets["gemini"]["api_key"]
genai.configure(api_key=gemini_api_key)

# Create Gemini model
model = genai.GenerativeModel("gemini-1.5-flash")

# Engineering Math topics
topics = [
    "Differentiation",
    "Integration",
    "Laplace Transform",
    "Fourier Series",
    "Matrix Algebra",
    "Complex Numbers",
    "Differential Equations",
    "Vector Calculus",
    "Probability & Statistics"
]

# UI
st.title("⚙️ AI Engineering Math Tutor")
st.write("This app generates **Engineering Math problems** and solves them step by step using Gemini API.")

# Sidebar - pick mode
mode = st.sidebar.radio("Choose Mode", ["Generate Question", "Enter Your Own"])

if mode == "Generate Question":
    topic = random.choice(topics)
    st.subheader(f"📘 Auto-Generated Question from {topic}")

    # Ask Gemini to create a question + solution
    question_prompt = f"Generate one challenging {topic} question for engineering students."
    question = model.generate_content(question_prompt).text

    st.write(f"**Question:** {question}")

    if st.button("Solve This Question"):
        solution_prompt = f"Solve this engineering math problem step by step: {question}"
        solution = model.generate_content(solution_prompt).text
        st.success("✅ Step-by-Step Solution:")
        st.write(solution)

else:  # User enters their own question
    user_question = st.text_area("✍️ Enter your Engineering Math question:")
    if st.button("Solve My Question"):
        if user_question.strip():
            solution_prompt = f"Solve this engineering math problem step by step: {user_question}"
            solution = model.generate_content(solution_prompt).text
            st.success("✅ Step-by-Step Solution:")
            st.write(solution)
        else:
            st.warning("Please enter a question.")
