import pandas as pd

source_path = r'c:\Users\ASUS\Downloads\career_data.csv'
print(f"Reading from: {source_path}")
try:
    df = pd.read_csv(source_path)
    print("Columns:", df.columns.tolist())
    print("First 3 rows:")
    print(df.head(3))
except Exception as e:
    print(f"Error reading CSV: {e}")
