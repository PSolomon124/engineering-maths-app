import streamlit as st
import random
from google import genai
from google.genai import types
import firebase_admin
from firebase_admin import credentials, db

# ----------------
# Firebase Setup
# ----------------
if not firebase_admin._apps:
    cred = credentials.Certificate("firebase_key.json")  # Add your Firebase key
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://YOUR_PROJECT.firebaseio.com/'
    })

# ----------------
# Gemini Setup
# ----------------
client = genai.Client(api_key=st.secrets["gemini"]["api_key"])

st.title("📚 Collaborative AI Tutor")

# Generate or join session
session_id = st.text_input("Enter Session Code (or leave blank to create new):")
if not session_id:
    session_id = str(random.randint(10000, 99999))
    st.success(f"New session created: {session_id}")

ref = db.reference(f"sessions/{session_id}")

# Start with a question
if st.button("Generate New Question"):
    prompt = "Generate a university-level calculus question."
    response = client.models.generate_content(
        model="gemini-1.5-flash",
        contents=prompt
    )
    question = response.text
    ref.child("question").set(question)
    ref.child("answers").set({})  # reset answers

# Display question
question = ref.child("question").get()
if question:
    st.subheader("📖 Current Question")
    st.write(question)

    # Student submits answer
    answer = st.text_input("Your Answer:")
    if st.button("Submit Answer"):
        ref.child("answers").push(answer)

    # Show all answers
    st.subheader("📝 Group Answers")
    answers = ref.child("answers").get()
    if answers:
        for k, v in answers.items():
            st.write(f"- {v}")

    # AI Tutor Response
    if st.button("Get Tutor Guidance"):
        answers_text = "\n".join(answers.values()) if answers else "No answers yet."
        tutor_prompt = f"Question: {question}\nStudent Answers: {answers_text}\nProvide step-by-step explanation as a friendly human tutor."
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=tutor_prompt
        )
        st.subheader("👩‍🏫 Tutor's Guidance")
        st.write(response.text)
