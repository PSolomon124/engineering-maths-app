# app.py

import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate

# Load API Key from Streamlit secrets
gemini_api_key = st.secrets["gemini"]["api_key"]

# Initialize Gemini model
llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=gemini_api_key)

st.title("📐 Engineering Maths AI Tutor")
st.write("Solve problems OR generate practice questions automatically.")

# Dropdown menu for action
action = st.selectbox("Choose Action", ["Solve My Problem", "Generate Practice Question"])

# --- SOLVE PROBLEM MODE ---
if action == "Solve My Problem":
    user_question = st.text_area("✍️ Enter your engineering math problem (calculation-based):")
    if st.button("Solve"):
        if user_question.strip() == "":
            st.warning("Please enter a problem.")
        else:
            template = """You are an Engineering Mathematics tutor.
            Solve the problem step by step with full explanations:
            {question}"""
            prompt = PromptTemplate(input_variables=["question"], template=template)
            response = llm.invoke(prompt.format(question=user_question))
            st.subheader("✅ Step-by-Step Solution")
            st.write(response.content)

# --- GENERATE PRACTICE MODE ---
elif action == "Generate Practice Question":
    topic = st.selectbox("Choose Topic", [
        "Differentiation",
        "Integration",
        "Linear Algebra",
        "Probability & Statistics",
        "Complex Numbers",
        "Laplace Transform",
        "Fourier Series"
    ])
    num_qs = st.slider("Number of Questions", 1, 5, 1)

    if st.button("Generate Questions"):
        template = """You are an Engineering Mathematics tutor.
        Generate {n} exam-style practice questions from the topic: {topic}.
        The questions should require calculations, not just theory.
        Do not provide solutions yet."""
        prompt = PromptTemplate(input_variables=["n", "topic"], template=template)
        response = llm.invoke(prompt.format(n=num_qs, topic=topic))
        
        st.subheader("📘 Practice Questions")
        st.write(response.content)

        # Ask if user wants solutions
        if st.button("Show Solutions"):
            sol_template = """Now provide detailed step-by-step solutions for these {n} {topic} problems:
            {questions}"""
            sol_prompt = PromptTemplate(
                input_variables=["n", "topic", "questions"],
                template=sol_template
            )
            sol_response = llm.invoke(sol_prompt.format(
                n=num_qs, topic=topic, questions=response.content
            ))
            st.subheader("✅ Solutions")
            st.write(sol_response.content)
