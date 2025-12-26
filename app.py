import streamlit as st
import os

# 1. Force the page title immediately
st.set_page_config(page_title="Debug Mode", layout="wide")
st.title("✅ The App Updated Successfully!")
st.write("If you can see this, your new code is live on the internet.")

# 2. Status Check Section
st.divider()
st.subheader("🔍 System Diagnostics")

# Check API Key
key = st.secrets.get("GOOGLE_API_KEY")
if key:
    st.success(f"API Key Found: {key[:5]}********")
else:
    st.error("❌ API Key is MISSING. Go to Settings -> Secrets.")

# Check CSV File
if os.path.exists("career_data.csv"):
    st.success("✅ 'career_data.csv' file found.")
else:
    st.warning("⚠️ 'career_data.csv' not found (App will use AI only).")

# 3. The Search Bar (Guaranteed to show)
st.divider()
st.subheader("🚀 Career Search")
query = st.text_input("Enter a role:", placeholder="Try 'Data Scientist'")

if query and key:
    st.info(f"You searched for: {query}. (AI generation would happen here)")
