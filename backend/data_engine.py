import pandas as pd
import os

# Data Paths
DATA_DIR = r"c:\Users\ASUS\Downloads\career_data.csv"
POSTINGS_FILE = os.path.join(DATA_DIR, "linkedin_job_postings.csv")
SKILLS_FILE = os.path.join(DATA_DIR, "job_skills.csv")

def load_data():
    """
    Loads and merges job postings and skills.
    Returns a DataFrame with 'job_title' and 'job_skills'.
    """
    try:
        # Load Postings (Only need Link and Title)
        # Verify column names dynamically or assume standard
        # We read just the header first to be safe
        df_p_header = pd.read_csv(POSTINGS_FILE, nrows=0)
        p_cols = df_p_header.columns.tolist()
        
        # Look for title column
        title_col = 'job_title'
        if 'job_title' not in p_cols:
             # Fallback: find column with 'title' in it
             candidates = [c for c in p_cols if 'title' in c.lower()]
             if candidates:
                 title_col = candidates[0]
        
        df_postings = pd.read_csv(POSTINGS_FILE, usecols=['job_link', title_col])
        df_postings.rename(columns={title_col: 'job_title'}, inplace=True)

        # Load Skills
        df_skills = pd.read_csv(SKILLS_FILE, usecols=['job_link', 'job_skills'])

        # Merge
        merged_df = pd.merge(df_postings, df_skills, on='job_link', how='inner')
        return merged_df
    except Exception as e:
        print(f"Error loading data: {e}")
        return pd.DataFrame()

def get_top_skills(df, role_query):
    """
    Filters DF by role_query (fuzzy match) and returns top 10 skills.
    """
    # Simple case-insensitive contains match for speed
    # Advanced: Fuzzy match logic can be added here
    
    # Filter
    mask = df['job_title'].str.contains(role_query, case=False, na=False)
    filtered = df[mask]
    
    if filtered.empty:
        return [], 0
    
    # Extract skills
    # job_skills are often comma separate or pipe separate?
    # Inspecting "job_skills" column: usually "Analysis, Python, SQL"
    
    all_skills = []
    
    for skills_str in filtered['job_skills'].dropna():
        # Clean and split
        # Heuristic: split by comma, maybe pipe
        # We'll try comma first which is standard
        skills = [s.strip() for s in skills_str.split(',')]
        all_skills.extend(skills)
        
    from collections import Counter
    counts = Counter(all_skills)
    top_10 = counts.most_common(10)
    
    return top_10, len(filtered)
