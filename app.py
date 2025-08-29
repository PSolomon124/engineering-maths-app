import streamlit as st
import google.generativeai as genai

# Configure API Key from Streamlit secrets
genai.configure(api_key=st.secrets["gemini"]["api_key"])

# Humanizer function to remove "AI tone"
def humanize_response(text):
    replacements = {
        "AI": "tutor",
        "I am an AI": "I am your tutor",
        "As an AI": "As your tutor",
        "AI model": "guide",
        "assistant": "tutor"
    }
    for k, v in replacements.items():
        text = text.replace(k, v)
    return text

# Streamlit App Layout
st.set_page_config(page_title="Engineering Maths Tutor", layout="wide")
st.title("📘 Collaborative Engineering Maths Tutor")

st.write("👨‍🏫 Pick a topic, ask questions together, and let your **tutor** guide you step by step.")

# Sidebar for topics
topics = [
    "Calculus", "Linear Algebra", "Differential Equations",
    "Complex Numbers", "Probability & Statistics",
    "Vector Analysis", "Transforms (Laplace, Fourier, Z)",
    "Numerical Methods", "Engineering Mechanics (Maths-based)"
]

topic_choice = st.sidebar.selectbox("📂 Choose a Topic", topics)
st.sidebar.write(f"✅ Current Topic: **{topic_choice}**")

# Chat history for collaboration
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Display chat history
for role, content in st.session_state.chat_history:
    if role == "student":
        st.chat_message("user").write(content)
    else:
        st.chat_message("assistant").write(content)

# Student input
if prompt := st.chat_input("Ask your tutor a question or suggest a problem..."):
    # Save student message
    st.session_state.chat_history.append(("student", prompt))
    st.chat_message("user").write(prompt)

    # AI Tutor Response
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(f"You are a human tutor. Topic: {topic_choice}. Question: {prompt}. \
    Answer like a human professor with clear steps, examples, and explanations. Avoid AI references.")

    answer = humanize_response(response.text)
    st.session_state.chat_history.append(("tutor", answer))
    st.chat_message("assistant").write(answer)
