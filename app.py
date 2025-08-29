import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
from langchain_google_genai import ChatGoogleGenerativeAI

# --- Setup Firebase ---
if not firebase_admin._apps:
    cred = credentials.Certificate("firebase_key.json")  # Add your Firebase service account key
    firebase_admin.initialize_app(cred)

db = firestore.client()

# --- Setup Gemini ---
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash", 
    google_api_key=st.secrets["GOOGLE_API_KEY"]
)

st.title("🤝 Collaborative Engineering Maths Solver")

# Input box
user_input = st.text_input("Enter your math problem:")

if st.button("Solve"):
    if user_input:
        # Get AI response
        response = llm.invoke(user_input)
        solution = response.content

        # Display solution
        st.write("### Solution:")
        st.write(solution)

        # Save to Firebase
        doc_ref = db.collection("math_solutions").add({
            "problem": user_input,
            "solution": solution
        })
        st.success("✅ Saved to collaborative database!")

# Show all solutions from others
st.write("## 🔎 Community Solutions")
solutions = db.collection("math_solutions").stream()
for doc in solutions:
    data = doc.to_dict()
    st.write(f"**Problem:** {data['problem']}")
    st.write(f"**Solution:** {data['solution']}")
    st.markdown("---")
