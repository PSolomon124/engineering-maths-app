import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
from langchain_google_genai import ChatGoogleGenerativeAI

# ✅ Load API key
google_api_key = st.secrets["GOOGLE_API_KEY"]

# ✅ Init Firebase
if not firebase_admin._apps:
    cred = credentials.Certificate(dict(st.secrets["firebase"]))
    firebase_admin.initialize_app(cred)
db = firestore.client()

# ✅ LLM setup
llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro", google_api_key=google_api_key)

st.title("📐 Engineering Maths App (Collaborative)")

question = st.text_input("Enter a math question:")
if st.button("Solve"):
    if question:
        response = llm.invoke(question)
        st.write("**Answer:**", response.content)

        # ✅ Store question/answer in Firestore
        doc_ref = db.collection("math_questions").add({
            "question": question,
            "answer": response.content
        })
        st.success("Saved to Firebase!")
