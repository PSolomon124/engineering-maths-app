# app.py

import os
import time
import json
import streamlit as st
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader, TextLoader
from langchain.prompts import PromptTemplate

# -----------------------
# Load environment variables
load_dotenv()
google_api_key = os.getenv("GOOGLE_API_KEY")

if not google_api_key:
    st.error("❌ GOOGLE_API_KEY not found. Please set it in .env or Streamlit secrets.")
    st.stop()

# -----------------------
# Initialize Gemini LLM (use Flash for higher rate limits)
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    google_api_key=google_api_key,
    temperature=0.3
)

# -----------------------
# Safe invoke with retries (handles ResourceExhausted errors)
def safe_invoke(llm, question, retries=3, delay=5):
    for attempt in range(retries):
        try:
            return llm.invoke(question)
        except Exception as e:
            if "ResourceExhausted" in str(e) and attempt < retries - 1:
                wait = delay * (attempt + 1)
                st.warning(f"⚠️ Resource limit hit. Retrying in {wait}s...")
                time.sleep(wait)
                continue
            raise e

# -----------------------
# Streamlit UI
st.set_page_config(page_title="Resume Parser", layout="centered")
st.title("📄 AI Resume Parser")
st.write("Upload your resume and ask questions about it.")

uploaded_file = st.file_uploader("Upload Resume", type=["pdf", "docx", "txt"])
question = st.text_input("Ask something about this resume:")

if uploaded_file and question:
    # Save uploaded file
    file_path = f"temp_{uploaded_file.name}"
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Load file
    if uploaded_file.type == "application/pdf":
        loader = PyPDFLoader(file_path)
    elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        loader = Docx2txtLoader(file_path)
    else:
        loader = TextLoader(file_path)

    documents = loader.load()
    resume_text = " ".join([doc.page_content for doc in documents])

    # Prompt
    prompt_template = PromptTemplate(
        input_variables=["resume", "question"],
        template="""
        You are an AI Resume Assistant.
        Resume: {resume}
        Question: {question}
        Provide a clear, concise answer.
        """
    )

    prompt = prompt_template.format(resume=resume_text, question=question)

    with st.spinner("Analyzing resume..."):
        try:
            response = safe_invoke(llm, prompt)
            st.success("✅ Done!")
            st.write(response.content if hasattr(response, "content") else response)
        except Exception as e:
            st.error(f"❌ Error: {e}")
