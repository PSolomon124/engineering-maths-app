import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
import firebase_admin
from firebase_admin import credentials, db

# ----------------------------
# Load Gemini API Key
# ----------------------------
if "gemini" not in st.secrets or "GOOGLE_API_KEY" not in st.secrets["gemini"]:
    st.error("❌ Missing [gemini] GOOGLE_API_KEY in secrets.toml")
    st.stop()

llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-pro",
    google_api_key=st.secrets["gemini"]["GOOGLE_API_KEY"]
)

# ----------------------------
# Initialize Firebase
# ----------------------------
if "firebase" not in st.secrets:
    st.error("❌ Missing [firebase] section in secrets.toml")
    st.stop()

firebase_secrets = st.secrets["firebase"]

if not firebase_admin._apps:
    cred = credentials.Certificate({
        "type": firebase_secrets["type"],
        "project_id": firebase_secrets["project_id"],
        "private_key_id": firebase_secrets["private_key_id"],
        "private_key": firebase_secrets["private_key"].replace("\\n", "\n"),
        "client_email": firebase_secrets["client_email"],
        "client_id": firebase_secrets["client_id"],
        "auth_uri": firebase_secrets["auth_uri"],
        "token_uri": firebase_secrets["token_uri"],
        "auth_provider_x509_cert_url": firebase_secrets["auth_provider_x509_cert_url"],
        "client_x509_cert_url": firebase_secrets["client_x509_cert_url"]
    })
    # Add your Firebase Realtime Database URL here 👇
    firebase_admin.initialize_app(cred, {
        "databaseURL": "https://engineering-maths-app.firebaseio.com"
    })

# ----------------------------
# Streamlit UI
# ----------------------------
st.title("📐 Engineering Maths Tutor (Gemini + Firebase)")

user_input = st.text_input("Enter your maths problem:")

if st.button("Solve"):
    if user_input.strip():
        response = llm.invoke(user_input)
        st.write("### 📊 Step-by-Step Solution")
        st.write(response.content)

        # Save query + response to Firebase
        ref = db.reference("math_queries")
        ref.push({
            "problem": user_input,
            "solution": response.content
        })

        st.success("✅ Saved to Firebase Database")
    else:
        st.warning("⚠️ Please enter a maths problem.")
