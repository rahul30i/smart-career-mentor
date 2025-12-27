import streamlit as st
import google.generativeai as genai
import os

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

# --- SIDEBAR status ---
with st.sidebar:
    active_model = get_gemini_model()
    if active_model:
        st.success(f"✅ Connected to: {active_model}")
    else:
        st.error("❌ No Gemini models found")
        st.stop()

# --- MAIN INPUT ---
user_role = st.text_input("What role do you want to target?", placeholder="e.g. Full Stack Developer")

# --- THE MENTOR LOGIC ---
if user_role:
    with st.spinner("🧠 Designing your curriculum... (This takes about 10 seconds)"):
        try:
            # 1. ENHANCED PROMPT
            prompt = f"""
            Act as a Senior Career Coach. The user wants to become a: {user_role}.
            
            Generate a detailed, strict mentorship guide in this exact structure using Markdown headers:
            
            ## 🗺️ Visual Timeline
            Provide a Mermaid.js chart code (wrapped in ```mermaid ... ```) for a 6-month timeline (Foundations -> Deep Dive -> Job Ready).
            
            ## 📚 Learning Path
            - Phase 1: Foundations (Key concepts and theory)
            - Phase 2: Deep Dive (Advanced skills and stacks)
            - Phase 3: Mastery (Real-world application)
            
            ## 🛠️ Portfolio Projects
            List 2 distinct real-world projects. For each, specify:
            - Project Name
            - Tech Stack
            - Key Features
            
            ## 🔗 Best Resources
            - 1 Free Course (Name & specific URL if known or description)
            - 1 Paid Course (Name & Platform)
            - 1 Recommended YouTube Channel
            
            ## 💼 Getting Hired
            - Where to apply (platforms)
            - 5 Keyword tags for Resume
            - 1 Crucial Interview Tip
            """
            
            # 2. GET AI RESPONSE
            model = genai.GenerativeModel(active_model)
            response = model.generate_content(prompt)
            content = response.text
            
            # 3. ORGANIZE OUTPUT INTO TABS
            st.divider()
            
            # Create Tabs
            tab1, tab2, tab3, tab4 = st.tabs(["Roadmap", "Projects", "Resources", "Jobs"])
            
            # Helper to extract sections based on headers
            def extract_section(text, header, next_header=None):
                try:
                    start = text.find(header)
                    if start == -1: return "Section not found."
                    if next_header:
                        end = text.find(next_header)
                        if end == -1: return text[start:] # If next header not found, go to end
                        return text[start:end]
                    return text[start:]
                except:
                    return "Error parsing section."

            # Tab 1: Roadmap (Visual + Learning Path)
            with tab1:
                # Extract and Render Mermaid
                timeline_section = extract_section(content, "## 🗺️ Visual Timeline", "## 📚 Learning Path")
                if "```mermaid" in timeline_section:
                    try:
                        # Extract just the code block
                        parts = timeline_section.split("```mermaid")
                        code_block = parts[1].split("```")[0]
                        st.subheader("🗺️ Visual Timeline")
                        st.markdown(f"```mermaid\n{code_block}\n```")
                    except:
                        st.error("Could not render timeline.")
                
                # Extract and Render Learning Path
                learning_path = extract_section(content, "## 📚 Learning Path", "## 🛠️ Portfolio Projects")
                st.markdown(learning_path)

            # Tab 2: Projects
            with tab2:
                projects = extract_section(content, "## 🛠️ Portfolio Projects", "## 🔗 Best Resources")
                st.markdown(projects)

            # Tab 3: Resources
            with tab3:
                resources = extract_section(content, "## 🔗 Best Resources", "## 💼 Getting Hired")
                st.markdown(resources)

            # Tab 4: Jobs
            with tab4:
                jobs = extract_section(content, "## 💼 Getting Hired")
                st.markdown(jobs)

        except Exception as e:
            st.error(f"An error occurred: {e}")
