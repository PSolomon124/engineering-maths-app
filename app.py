import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
import firebase_admin
from firebase_admin import credentials, db
import json

# --- Load Google API Key from Streamlit Secrets ---
google_api_key = st.secrets["GOOGLE_API_KEY"]

# --- Firebase Setup ---
firebase_config = st.secrets["firebase"]

if not firebase_admin._apps:
    cred = credentials.Certificate(json.loads(firebase_config["service_account"]))
    firebase_admin.initialize_app(cred, {
        "databaseURL": firebase_config["databaseURL"]
    })

# --- LangChain Model ---
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    google_api_key=google_api_key
)

# --- Streamlit UI ---
st.title("Engineering Maths App 🔢")
user_input = st.text_input("Enter a math problem:")

if st.button("Solve"):
    if user_input.strip():
        response = llm.invoke(user_input)
        solution = response.content

        # Save to Firebase Realtime DB
        ref = db.reference("problems")
        ref.push({
            "question": user_input,
            "solution": solution
        })

        st.write("### ✅ Solution:")
        st.write(solution)
    else:
        st.warning("Please enter a problem.")
