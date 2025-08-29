# app.py

import streamlit as st
import json

st.set_page_config(page_title="Engineering Maths App", layout="wide")

st.title("📘 Engineering Maths App")

# --- Debugging: show what secrets are available ---
st.subheader("🔑 Secrets check")
try:
    st.write("Available secrets keys:", list(st.secrets.keys()))
except Exception as e:
    st.error(f"Could not load secrets: {e}")

# --- Firebase credentials check ---
if "firebase" in st.secrets:
    firebase_creds = st.secrets["firebase"]

    st.success("✅ Firebase section found in secrets.toml")
    st.json({
        "project_id": firebase_creds.get("project_id", "❌ Missing"),
        "client_email": firebase_creds.get("client_email", "❌ Missing"),
        # don’t show private_key for security
    })
else:
    st.warning("⚠️ No [firebase] section found in secrets.toml")

# --- Simple demo function ---
st.subheader("📐 Math Demo")
number = st.number_input("Enter a number", value=2, step=1)
st.write(f"Square of {number} = {number**2}")
