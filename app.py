import streamlit as st
import pandas as pd
import os
import google.generativeai as genai

# --- PAGE SETUP ---
st.set_page_config(page_title="Smart Career Mentor", page_icon="🎓", layout="wide")

st.title("Smart Career Mentor 🎓")
st.caption("Strict Mode Active: Generating structured, semester-level roadmaps.")

# --- DIAGNOSTICS (This helps us see what is working) ---
with st.expander("🔌 System Status (Click to Debug)", expanded=False):
    # Check 1: API Key
    api_key = st.secrets.get("GOOGLE_API_KEY")
    if api_key:
        st.success("✅ Google API Key found.")
        genai.configure(api_key=api_key)
    else:
        st.error("❌ Google API Key is MISSING in Secrets.")
    
    # Check 2: CSV Data
    csv_file = "career_data.csv"
    if os.path.exists(csv_file):
        try:
            df = pd.read_csv(csv_file)
            st.success(f"✅ Career Database Loaded ({len(df)} roles found).")
        except Exception as e:
            st.error(f"❌ Database Error: {e}")
    else:
        st.warning("⚠️ 'career_data.csv' not found. Using AI-only mode.")

# --- THE SEARCH BAR (This should ALWAYS appear now) ---
st.divider()
st.subheader("🚀 Build Your Career Path")

user_role = st.text_input("Enter a Job Role (e.g., 'AI Engineer' or 'Digital Marketer'):", placeholder="Type your dream job here...")

# --- MAIN LOGIC ---
if user_role:
    if not api_key:
        st.error("Please add your Google API Key in Streamlit Secrets to generate a roadmap.")
        st.stop()
        
    with st.spinner(f"🧠 Designing a university-grade curriculum for {user_role}..."):
        try:
            # Simple AI Call to test connection
            model = genai.GenerativeModel('gemini-pro')
            response = model.generate_content(f"Give me a 3-step summary to become a {user_role}.")
            
            st.success("Roadmap Generated!")
            st.markdown(response.text)
            
        except Exception as e:
            st.error(f"An error occurred while generating the roadmap: {e}")