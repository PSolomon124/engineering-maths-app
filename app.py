import os
import streamlit as st
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials, firestore
from langchain_google_genai import ChatGoogleGenerativeAI

# Load environment variables (for local dev)
load_dotenv()

# ------------------------------
# Google API setup
# ------------------------------
GOOGLE_API_KEY = st.secrets.get("GOOGLE_API_KEY") or os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    st.error("❌ Missing GOOGLE_API_KEY in secrets.toml or .env")
    st.stop()

llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=GOOGLE_API_KEY)

# ------------------------------
# Firebase setup
# ------------------------------
if "firebase" in st.secrets:
    firebase_secrets = st.secrets["firebase"]

    firebase_creds = {
        "type": firebase_secrets.get("type"),
        "project_id": firebase_secrets.get("project_id"),
        "private_key_id": firebase_secrets.get("private_key_id"),
        "private_key": firebase_secrets.get("private_key").replace("\\n", "\n"),
        "client_email": firebase_secrets.get("client_email"),
        "client_id": firebase_secrets.get("client_id"),
        "auth_uri": firebase_secrets.get("auth_uri"),
        "token_uri": firebase_secrets.get("token_uri"),
        "auth_provider_x509_cert_url": firebase_secrets.get("auth_provider_x509_cert_url"),
        "client_x509_cert_url": firebase_secrets.get("client_x509_cert_url"),
    }

    if not firebase_admin._apps:
        cred = credentials.Certificate(firebase_creds)
        firebase_admin.initialize_app(cred)

    db = firestore.client()
else:
    db = None
    st.warning("⚠️ Firebase not configured. Add it in secrets.toml")

# ------------------------------
# Streamlit UI
# ------------------------------
st.title("🚀 Engineering Maths App")

user_input = st.text_input("Enter your math problem:")

if st.button("Solve") and user_input:
    with st.spinner("Thinking..."):
        response = llm.invoke(user_input)
        st.write("### ✅ Solution:")
        st.write(response.content)

        if db:
            db.collection("problems").add({"question": user_input, "answer": response.content})
            st.success("Saved to Firebase!")
