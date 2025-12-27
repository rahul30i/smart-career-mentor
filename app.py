import streamlit as st
import pandas as pd
import os
import google.generativeai as genai

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Smart Career Mentor", page_icon="🎓", layout="wide")

# --- SAFETY CHECK: LOAD API KEY ---
try:
    api_key = st.secrets.get("GOOGLE_API_KEY") or os.getenv("GOOGLE_API_KEY")
    if not api_key:
        st.error("🚨 Critical Error: Google API Key is missing.")
        st.stop()
    genai.configure(api_key=api_key)
except Exception as e:
    st.error(f"Connection Error: {e}")
    st.stop()

# --- HELPER: SMART MODEL SELECTOR ---
def get_gemini_model():
    """
    Dynamically finds a supported model to avoid 404 errors.
    Prioritizes 'gemini' models that support 'generateContent'.
    Returns the exact model name.
    """
    try:
        available_models = []
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                if 'gemini' in m.name:
                    return m.name
        return None 
    except Exception as e:
        return None

# --- APP HEADER ---
st.title("🎓 Smart Career Mentor")
st.markdown("### Your AI-Powered Path to a New Career")
st.write("Enter a role (e.g., *'AI Engineer'*, *'Product Manager'*) to get a university-grade roadmap.")

# --- SIDEBAR: SYSTEM & MODEL STATUS ---
with st.sidebar:
    st.info("Built with Google Gemini + Streamlit")
    
    # Run Smart Model Detection
    active_model = get_gemini_model()
    
    if active_model:
        st.success(f"✅ Connected to: {active_model}")
    else:
        st.error("❌ No Gemini models found")
        st.stop() # Stop execution if no model is found

# --- MAIN INPUT ---
user_role = st.text_input("What role do you want to target?", placeholder="e.g. Full Stack Developer")

# --- THE MENTOR LOGIC ---
if user_role:
    with st.spinner("🧠 Designing your curriculum... (This takes about 10 seconds)"):
        try:
            # 1. THE PROMPT
            prompt = f"""
            Act as a Senior Career Mentor. The user wants to become a: {user_role}.
            
            Generate a strict, structured roadmap in this exact format:
            
            SECTION 1: VISUAL TIMELINE
            Create a Mermaid.js chart code (wrapped in ```mermaid) showing a 3-phase timeline (Foundations -> Advanced -> Job Ready).
            
            SECTION 2: THE SYLLABUS
            - Phase 1 (Weeks 1-4): List 3 core topics.
            - Phase 2 (Weeks 5-12): List 3 advanced skills.
            - Phase 3 (Weeks 13+): List 2 job-ready projects.
            
            SECTION 3: RESOURCES
            - Best Free Course: (Name & Description)
            - Best Paid Course: (Name & Description)
            
            SECTION 4: GETTING HIRED
            - 5 Keywords for Resume:
            - 1 Insider Tip:
            """
            
            # 2. GET AI RESPONSE
            model = genai.GenerativeModel(active_model)
            response = model.generate_content(prompt)
            content = response.text
            
            # 3. DISPLAY RESULT
            st.divider()
            
            # Extract Mermaid Code for Visuals
            if "```mermaid" in content:
                parts = content.split("```mermaid")
                graph_code = parts[1].split("```")[0]
                st.subheader("🗺️ Your Career Timeline")
                st.markdown(f"```mermaid\n{graph_code}\n```")
                
                # Show the rest of the text
                st.subheader("📝 Detailed Guide")
                text_content = parts[0] + parts[2] if len(parts) > 2 else content.replace("```mermaid" + graph_code + "```", "")
                st.markdown(text_content)
            else:
                st.markdown(content)
                
        except Exception as e:
            st.error(f"An error occurred: {e}")
