import pandas as pd

base_path = r'c:\Users\ASUS\Downloads\career_data.csv'

try:
    print("--- Skills ---")
    df_skills = pd.read_csv(f'{base_path}\\job_skills.csv', nrows=5)
    print(df_skills.columns.tolist())
    print(df_skills.head(2))

    print("\n--- Postings ---")
    df_jobs = pd.read_csv(f'{base_path}\\linkedin_job_postings.csv', nrows=5)
    print(df_jobs.columns.tolist())
    print(df_jobs.head(2))
except Exception as e:
    print(e)
