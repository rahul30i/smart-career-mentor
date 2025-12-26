import backend.data_engine as de
import time

print("Loading data...")
start = time.time()
df = de.load_data()
end = time.time()
print(f"Data loaded in {end - start:.2f} seconds. Rows: {len(df)}")

if not df.empty:
    print("Testing search for 'Data Analyst'...")
    skills, count = de.get_top_skills(df, "Data Analyst")
    print(f"Found {count} jobs.")
    print("Top Skills:", skills)
else:
    print("Data load returned empty DataFrame.")
