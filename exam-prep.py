
import pandas as pd
import sys
import os

if len(sys.argv) < 2:
    print("Usage: python exam-prep.py <excel_file1> <excel_file2> ...")
    sys.exit(1)

output_file = "output.csv"
# Remove output file if it exists to avoid duplicate appends
if os.path.exists(output_file):
    os.remove(output_file)

for file in sys.argv[1:]:
    df = pd.read_excel(file)

    # Remove the first column ONLY
    df = df.iloc[:, 1:]

    # Remove the last 5 columns
    df = df.iloc[:, :-5]

    # Row mask: remove rows containing "1st day", "instructor", or "48 hours"
    row_mask = ~df.apply(lambda row: row.astype(str).str.lower().str.contains("1st day|instructor|48 hours").any(), axis=1)
    df = df[row_mask]

    # Column mask: remove columns containing "1st day", "instructor", "48 hours", or "Registration"
    col_mask = ~df.apply(lambda col: col.astype(str).str.lower().str.contains("1st day|48 hours|registration|instructor").any(), axis=0)
    df = df.loc[:, col_mask]

    # Drop rows and columns where all values are NaN
    df = df.dropna(axis=0, how='all')
    df = df.dropna(axis=1, how='all')

    # Replace remaining NaN with the value from the row above in the same column
    df = df.ffill().infer_objects(copy=False)

    # Find the first column containing "00:00:00"
    search_str = "00:00:00"
    date_col = None
    for col in df.columns:
        if df[col].astype(str).str.contains(search_str).any():
            date_col = col
            break

    # If a date column is found, sort by it
    if date_col is not None:
        df[date_col] = pd.to_datetime(df[date_col], errors='coerce')
        df = df.sort_values(by=date_col)

    # Append to the output file (no header, no index)
    df.to_csv(output_file, mode='a', index=False, header=False)