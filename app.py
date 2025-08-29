import streamlit as st
import google.generativeai as genai
import firebase_admin
from firebase_admin import credentials, db

# ---------------------------
# Firebase Setup
# ---------------------------
if not firebase_admin._apps:
    cred = credentials.Certificate({
        "type": "service_account",
        "project_id": st.secrets["firebase"]["project_id"],
        "private_key_id": st.secrets["firebase"]["private_key_id"],
        "private_key": st.secrets["firebase"]["private_key"].replace("\\n", "\n"),
        "client_email": st.secrets["firebase"]["client_email"],
        "client_id": st.secrets["firebase"]["client_id"],
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": f"https://www.googleapis.com/robot/v1/metadata/x509/{st.secrets['firebase']['client_email']}"
    })
    firebase_admin.initialize_app(cred, {
        "databaseURL": f"https://{st.secrets['firebase']['project_id']}.firebaseio.com/"
    })

# ---------------------------
# Gemini Setup
# ---------------------------
genai.configure(api_key=st.secrets["generation"]["api_key"])
model = genai.GenerativeModel("gemini-1.5-pro")

# ---------------------------
# Streamlit App
# ---------------------------
st.title("📘🤝 Collaborative Engineering Maths Tutor")

topic = st.text_input("Enter a math topic (e.g., Differentiation, Laplace Transform, Matrices):")

if st.button("Generate Collaborative Question"):
    if topic:
        prompt = (
            f"Generate a collaborative math question on '{topic}' for students. "
            "Write like a human tutor (not AI), guide step by step, "
            "make it engaging for group learning."
        )
        response = model.generate_content(prompt)

        if response and response.text:
            question = response.text

            # Save to Firebase
            ref = db.reference("shared_question")
            ref.set({"topic": topic, "question": question})

            st.success("New collaborative question generated and shared ✅")
            st.write("### Shared Question")
            st.write(question)
    else:
        st.warning("Please enter a topic first!")

# ---------------------------
# Display Shared Question
# ---------------------------
st.subheader("📡 Current Collaborative Question (for all students):")
ref = db.reference("shared_question")
shared = ref.get()

if shared:
    st.write(f"**Topic:** {shared['topic']}")
    st.write(shared["question"])
else:
    st.info("No question generated yet. Ask your tutor to create one!")
