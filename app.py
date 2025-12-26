import streamlit as st
import backend.data_engine as de
import backend.mentor as mentor

# Page Config
st.set_page_config(page_title="Smart Career Mentor (Strict Mode)", page_icon="🎓", layout="wide")

# Custom CSS
st.markdown("""
<style>
    .main { background-color: #ffffff; }
    h1, h2, h3 { font-family: 'Inter', sans-serif; color: #111827; }
    
    .metric-card {
        background: #f3f4f6; border-radius: 8px; padding: 15px;
        text-align: center; border: 1px solid #e5e7eb;
    }
    .metric-val { font-size: 1.5rem; font-weight: 700; color: #2563eb; }
    .metric-label { font-size: 0.9rem; color: #6b7280; font-weight: 500; }
    
    /* Project Cards */
    .project-card {
        border-left: 4px solid #10b981;
        background: #f0fdf4; padding: 1rem; margin-bottom: 1rem; border-radius: 0 8px 8px 0;
    }
    .project-title { font-weight: 700; font-size: 1.1rem; color: #064e3b; }
    .project-stack { font-family: monospace; color: #059669; font-size: 0.9rem; }
    
    /* Global Styling */
    .stExpander { border: 1px solid #e5e7eb; border-radius: 8px; box-shadow: 0 1px 2px rgba(0,0,0,0.05); }
</style>
""", unsafe_allow_html=True)

st.title("Smart Career Mentor 🎓")
st.markdown("**Strict Mode Active**: Generating structured, semester-level roadmaps.")

if 'data_loaded' not in st.session_state:
    with st.spinner("Initializing Engine..."):
        st.session_state.df = de.load_data()
        st.session_state.data_loaded = True
df = st.session_state.df

if not df.empty:
    role = st.text_input("Target Role", placeholder="e.g. DevOps Engineer", label_visibility="collapsed")
    
    if role:
        with st.spinner("Generating Structured Roadmap..."):
            top_skills, count = de.get_top_skills(df, role)
            roadmap = mentor.generate_strict_roadmap(role, top_skills)
            
            # --- HEADER ---
            st.markdown("---")
            col_head1, col_head2 = st.columns([3, 1])
            with col_head1:
                st.header(f"Roadmap: {roadmap['role']}")
                st.write(f"**Total Estimated Time:** {roadmap['estimated_total_time']}")
            
            with col_head2:
                # Mini stats if helpful, or just clean space
                pass
                
            # --- MERMAID TIMELINE ---
            # "Create a Top-Down graph (graph TD) where every node is a Phase and the label includes the Duration."
            mermaid_code = "graph TD\n"
            for i, phase in enumerate(roadmap['phases']):
                clean_name = phase['phase_name'].replace(":", "")
                mermaid_code += f'    p{i}["{phase["phase_name"]}<br/>⏱️ {phase["duration"]}"]\n'
                if i < len(roadmap['phases']) - 1:
                    mermaid_code += f"    p{i} --> p{i+1}\n"
            
            st.components.v1.html(f"""
            <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
            <script>mermaid.initialize({{startOnLoad:true, theme:'base'}});</script>
            <div class="mermaid" style="text-align: center;">
            {mermaid_code}
            </div>
            """, height=300, scrolling=True)
            
            # --- PHASES (EXPANDERS) ---
            st.subheader("📚 Learning Phases")
            for phase in roadmap['phases']:
                with st.expander(f"📍 {phase['phase_name']} ({phase['duration']})", expanded=False):
                    st.markdown("#### Topics:")
                    for t in phase['topics']:
                        st.markdown(f"- {t}")
                    
                    st.markdown("#### Best Resources:")
                    for r in phase['best_resources']:
                        st.markdown(f"- [{r['name']}]({r['url']}) _({r['type']})_")
                        
                    st.divider()
                    st.markdown(f"**✅ Checkpoint Project:** {phase['checkpoint_project']}")

            # --- PROJECTS ---
            st.subheader("🛠️ Projects Portfolio")
            col_p1, col_p2 = st.columns(2)
            
            # Distribute projects across columns
            for i, proj in enumerate(roadmap['projects']):
                target_col = col_p1 if i % 2 == 0 else col_p2
                with target_col:
                    st.markdown(f"""
                    <div class="project-card">
                        <div class="project-title">{proj['title']} ({proj['level']})</div>
                        <div class="project-stack">Stack: {proj['tech_stack']}</div>
                        <p>{proj['description']}</p>
                    </div>
                    """, unsafe_allow_html=True)
            
            # --- OUTLOOK & STRATEGY ---
            st.markdown("---")
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("🔮 Career Reality")
                st.markdown(f"**Salary Range:** {roadmap['career_outlook']['salary_range']}")
                st.markdown(f"**Growth:** {roadmap['career_outlook']['growth_path']}")
                if 'hard_truth' in roadmap['career_outlook']:
                    st.warning(f"**💡 Insider Advice:** {roadmap['career_outlook']['hard_truth']}")
                
            with col2:
                st.subheader("💼 The \"Get Hired\" Strategy")
                
                if 'application_strategy' in roadmap:
                    strat = roadmap['application_strategy']
                    st.markdown("**Resume Keywords:** " + ", ".join(strat.get('resume_keywords', [])))
                    st.markdown("**Where to Apply:** " + ", ".join(strat.get('hiring_platforms', [])))
                    
                    if 'outreach_template' in strat:
                        with st.expander("📨 View Outreach Template"):
                            st.code(strat['outreach_template'], language="text")
