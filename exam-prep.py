
import pandas as pd
import sys
import argparse
import os

# Enable or disable logging
logging_enabled = False


def clean_data(df:pd.DataFrame,col_head=1,col_tail=5)->pd.DataFrame:
    """_summary_

    Args:
        arr (list): _description_

    Returns:
        pd.DataFrame: _description_
    """
    df = df.map(lambda x: x.replace('\xa0', '').strip() if isinstance(x, str) else x)

    # region logging
    if logging_enabled:
        df.to_csv("log1.csv", mode='a', index=False, header=False)
        # endregion
    
    #remove col_head first columns
    df = df.iloc[:, col_head:]

    # Remove the col_tail last columns
    df = df.iloc[:, :-col_tail]
    
    # region logging
    if logging_enabled:
        df.to_csv("log2.csv", mode='a', index=False, header=False)
    # endregion
    
    # Row mask: remove rows containing "1st day", "instructor", or "48 hours"
    row_mask = ~df.apply(lambda row: row.astype(str).str.lower().str.contains("1st day|instructor|48 hours").any(), axis=1)
    df = df[row_mask]

    # Column mask: remove columns containing "1st day", "instructor", "48 hours", or "Registration"
    col_mask = ~df.apply(lambda col: col.astype(str).str.lower().str.contains("1st day|48 hours|Registration|instructor|During|business").any(), axis=0)
    df = df.loc[:, col_mask]
    
    # region logging
    if logging_enabled:
        df.to_csv("log3.csv", mode='a', index=False, header=False)
    # endregion
    
    # Drop rows and columns where all values are NaN
    df = df.dropna(axis=0, how='all')
    df = df.dropna(axis=1, how='all')
    
    # region logging
    if logging_enabled:
        df.to_csv("log4.csv", mode='a', index=False, header=False)
        # endregion
    
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

def clean_columns(df):
    df.columns = df.columns.str.strip()
    df.columns = ['col_' + str(i) for i in range(len(df.columns))]
    return df

# Function Does not work yet
def filter_data(df,keyword,pd):
    data = pd.read_csv("prefix.csv")
    filtered_data = data[data.apply(lambda row: row.astype(str).str.contains(keyword, case=False).any(), axis=1)]

    # Step 1: Find the row in df_lookup that matches the keyword
    match_row = df[df[1].str.lower() == keyword]

    if match_row.empty:
        print(f"No associations found for keyword '{keyword}'")
        return pd.DataFrame()  # return empty DataFrame

    # Step 2: Get the associated list from the 'Associated' column
    associated_values = match_row.iloc[0]['Associated']
    df = df.loc[filtered_data]
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
    parser.add_argument(
        '--verbose','-v', 
        action='store_true', 
        help="Enable logging to file"
    )
    parser.add_argument(
        '--school','-s', 
        type=str, 
        help="School name to filter by (optional)"
    )

    args = parser.parse_args()
    
    logging_enabled = args.verbose
    
    # Read all input files into a list of DataFrames
    dataframes = [pd.read_excel(file) for file in args.input_files]
    for df in dataframes:
        clean_columns(df)
        #df.to_csv("data.csv", mode='a', index=False, header=False)
    
    # Combine them
    df = pd.concat(dataframes, ignore_index=True)
    
    # region logging
    if logging_enabled:
        df.to_csv("log0.csv", mode='a', index=False, header=False)
        # endregion
    
    # Clean and sort the data
    df= clean_data(df)
    if args.school:
        df = filter_data(df,args.school,pd)
    df= sort_data(df)

    # Append to the output file (no header, no index)
    df.to_csv(args.output, mode='w', index=False, header=False)

if __name__ == "__main__":
    main()