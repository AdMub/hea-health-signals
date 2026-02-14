import pandas as pd
import os

# Adjust path as needed
DATA_PATH = r"..\Datasets\randhrs1992_2022v1.dta"

def inspect_columns():
    # Read just the header (fast)
    # The 'iterator=True' trick reads 0 rows just to get columns
    reader = pd.read_stata(DATA_PATH, iterator=True)
    columns = reader.variable_labels().keys() # Get all column names
    
    # Convert to list for searching
    col_list = list(columns)
    
    print(f"Total Columns: {len(col_list)}")
    print("First 10 Columns:", col_list[:10])
    
    # Search for key health variables
    search_terms = ['shlt', 'diab', 'bmi', 'hibp']
    
    print("\n--- Key Variable Search ---")
    for term in search_terms:
        # Find matches (case insensitive)
        matches = [c for c in col_list if term.lower() in c.lower()]
        print(f"Found {len(matches)} matches for '{term}': {matches[:5]}...")

if __name__ == "__main__":
    inspect_columns()