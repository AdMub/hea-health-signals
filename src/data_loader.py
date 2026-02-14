import pandas as pd
import os

# FIX 1: Use raw string (r"...") or forward slashes to avoid the error
# Also, assuming you are running this from the 'src' folder based on your terminal prompt,
# we need to go up one level to find 'Datasets' if it's in the project root.
DATA_PATH = r"..\Datasets\randhrs1992_2022v1.dta" 

# If the folder is actually inside src, keep it as:
# DATA_PATH = r"Datasets\randhrs1992_2022v1.dta"

def load_rand_data(filepath):
    print(f"Loading from: {os.path.abspath(filepath)}")
    print("This takes memory! Please wait...")
    
    # Check if file exists first to avoid confusing errors
    if not os.path.exists(filepath):
        print(f"ERROR: File not found at {filepath}")
        print("Current working directory is:", os.getcwd())
        return None, None

    # Load Data
    df = pd.read_stata(filepath)
    
    # Get labels using an iterator to avoid re-reading the whole file
    reader = pd.io.stata.StataReader(filepath)
    variable_labels = reader.variable_labels()
    
    print(f"SUCCESS: Loaded {df.shape[0]} people and {df.shape[1]} variables.")
    return df, variable_labels

if __name__ == "__main__":
    df, labels = load_rand_data(DATA_PATH)
    
    if df is not None:
        print("\nSample Data (Self-Rated Health 1992):")
        # Check if column exists before printing to be safe
        if 'R1SHLT' in df.columns:
            print(df[['HHIDPN', 'R1SHLT']].head())
            print("\nVariable Meaning of 'R1SHLT':")
            print(labels.get('R1SHLT', 'Label not found'))
        else:
            print("Column 'R1SHLT' not found. Data loaded but sample column missing.")