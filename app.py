# app.py
import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate

# ---------------------------
# Load Gemini API key from Streamlit secrets
# ---------------------------
api_key = st.secrets["GEMINI_API_KEY"]

# Initialize Gemini model
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",  # you can also use gemini-1.5-pro
    google_api_key=api_key
)

# Prompt template for math/engineering problems
template = """
You are an expert engineering mathematics tutor.
Solve the following problem step by step and explain clearly:

{problem}
"""

prompt = PromptTemplate(
    input_variables=["problem"],
    template=template
)

# ---------------------------
# Streamlit UI
# ---------------------------
st.set_page_config(page_title="Engineering Math Solver", page_icon="📐")

st.title("📐 Engineering Math Solver")
st.write("Enter any math/engineering problem and get a step-by-step solution powered by Gemini.")

# Text input from user
problem = st.text_area("✍️ Enter your problem here:", height=150)

if st.button("Solve"):
    if problem.strip():
        with st.spinner("Solving with Gemini..."):
            # Build the prompt
            final_prompt = prompt.format(problem=problem)

            # Query Gemini
            response = llm.invoke(final_prompt)

            # Show result
            st.subheader("✅ Step-by-step Solution:")
            st.write(response.content)
    else:
        st.warning("Please enter a problem first.")
