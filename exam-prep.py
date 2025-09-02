
import pandas as pd
import sys
import argparse
import os

def clean_data(df:pd.DataFrame,col_head=1,col_tail=5)->pd.DataFrame:
    """_summary_

    Args:
        arr (list): _description_

    Returns:
        pd.DataFrame: _description_
    """
    # Remove the first column ONLY
    df.to_csv("log2.csv", mode='a', index=False, header=False)
    df = df.iloc[:, col_head:]

    # Remove the last 5 columns
    df = df.iloc[:, :-col_tail]
    df.to_csv("log3.csv", mode='a', index=False, header=False)
    # Row mask: remove rows containing "1st day", "instructor", or "48 hours"
    row_mask = ~df.apply(lambda row: row.astype(str).str.lower().str.contains("1st day|instructor|48 hours").any(), axis=1)
    df = df[row_mask]

    # Column mask: remove columns containing "1st day", "instructor", "48 hours", or "Registration"
    col_mask = ~df.apply(lambda col: col.astype(str).str.lower().str.contains("1st day|48 hours|Registration|instructor").any(), axis=0)
    df = df.loc[:, col_mask]

    # Drop rows and columns where all values are NaN
    df = df.dropna(axis=0, how='all')
    df = df.dropna(axis=1, how='all')
    df.to_csv("log.csv", mode='a', index=False, header=False)
    # Replace remaining NaN with the value from the row above in the same column
    df = df.ffill().infer_objects(copy=False)
    
    return df
def sort_data(df:pd.DataFrame,search_str="00:00:00")->pd.DataFrame:
    """_summary_

    Args:
        df (pd.DataFrame): _description_
        search_str (str, optional): _description_. Defaults to "00:00:00".

    Returns:
        pd.DataFrame: _description_
    """
    
    # Find the first column containing search_str
    date_col = None
    for col in df.columns:
        if df[col].astype(str).str.contains(search_str).any():
            date_col = col
            break

    # if a column is found, sort by it (currently assumes date format)
    if date_col is not None:
        df[date_col] = pd.to_datetime(df[date_col], errors='coerce')
        df = df.sort_values(by=date_col)
    
    return df

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Combine multiple CSV/XLS files into one.")
    
    parser.add_argument(
        "input_files", 
        nargs="+", 
        help="List of input CSV files to combine."
    )

    parser.add_argument(
        "--output", "-o",
        default="output.csv",
        help="Output filename (default: output.csv)"
    )

    args = parser.parse_args()
    
    # Read all input files into a list of DataFrames
    dataframes = [pd.read_excel(file) for file in args.input_files]

    # Combine them
    df = pd.concat(dataframes, ignore_index=True)
    # Clean and sort the data
    df= clean_data(df)
    
    df= sort_data(df)

    # Append to the output file (no header, no index)
    df.to_csv(args.output, mode='w', index=False, header=False)

if __name__ == "__main__":
    main()