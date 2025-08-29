import streamlit as st
import firebase_admin
from firebase_admin import credentials, db
from langchain_google_genai import ChatGoogleGenerativeAI
import json

# ================================
# 🔑 Load secrets
# ================================
GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
firebase_secrets = st.secrets["firebase"]

# ================================
# 🚀 Firebase Initialization
# ================================
if not firebase_admin._apps:
    cred = credentials.Certificate(dict(firebase_secrets))
    firebase_admin.initialize_app(cred, {
        'databaseURL': f"https://{firebase_secrets['project_id']}.firebaseio.com/"
    })

ref = db.reference("/questions")

# ================================
# 🤖 AI Tutor Initialization
# ================================
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=GOOGLE_API_KEY)

# ================================
# 🌍 Streamlit UI
# ================================
st.title("📚 Collaborative AI Tutor")
st.write("Students can join from anywhere and learn from **one shared question** together.")

# Teacher/Student Toggle
mode = st.radio("Choose mode:", ["Student", "Teacher"])

# ---------------- Teacher ----------------
if mode == "Teacher":
    new_question = st.text_input("Enter a new question for everyone:")
    if st.button("Post Question"):
        ref.set({"question": new_question, "answer": ""})
        st.success("✅ Question posted for all students!")

# ---------------- Student ----------------
data = ref.get()
if data and "question" in data:
    st.subheader("📌 Current Question:")
    st.info(data["question"])

    if mode == "Student":
        if st.button("Get AI Help"):
            with st.spinner("AI Tutor is preparing..."):
                response = llm.invoke(data["question"])
                ref.update({"answer": response.content})
                st.success("Answer ready!")

    if "answer" in data and data["answer"]:
        st.subheader("🤖 AI Tutor Answer:")
        st.write(data["answer"])
else:
    st.warning("No question has been posted yet.")
