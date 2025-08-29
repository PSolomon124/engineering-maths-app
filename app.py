import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
from langchain_google_genai import ChatGoogleGenerativeAI

# Load Firebase credentials from Streamlit secrets
firebase_secrets = st.secrets["firebase"]

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

# Initialize Firebase only once
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)

db = firestore.client()

# Initialize AI Tutor
llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro", google_api_key=st.secrets["GOOGLE_API_KEY"])

st.title("📘 Collaborative Math Tutor")
st.write("Students can collaboratively pick a topic and learn together with an AI tutor.")

# Topic selection
topic = st.text_input("Enter a topic (e.g., Differentiation, Matrix, Integration):")

if topic:
    st.subheader(f"Topic Selected: {topic}")

    # Save to Firestore
    doc_ref = db.collection("math_topics").document("current")
    doc_ref.set({"topic": topic})

    # AI Tutor Guidance
    prompt = f"Explain {topic} step by step with one worked example for students."
    response = llm.invoke(prompt)
    st.write("### AI Tutor Response")
    st.write(response.content)

    # Collaborative Q&A
    question = st.text_input("Ask a question about this topic:")
    if question:
        q_response = llm.invoke(f"Answer this math question with steps: {question}")
        st.write("### Answer")
        st.write(q_response.content)

        # Store question for other students
        db.collection("questions").add({"topic": topic, "question": question})
