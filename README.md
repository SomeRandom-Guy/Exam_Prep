# Exam_Prep_Script
Script to extract information from .xlsx file

Arguments:
    
    INPUT ~REQUIRED~
    "input_files" 
    List of input CSV files to combine.
    
    OUTPUT ~OPTIONAL~
    "--output", "-o",
    destination file after running, outputs a .csv file
    If no argument will default to "output.csv"
  
    VERBOSE ~OPTIONAL~
    '--verbose','-v', 
    enables logging
    off by default
    
    SCHOOL ~OPTIONAL~ 
    '--school','-s', 
    School name to filter by
    currently not implemented