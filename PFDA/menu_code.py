###########################################
### PFDA - BIG PROJECT - functions file ###
###########################################

# This file contains all functions that deal with working with the DataFrame.

# Author: E. Qejvani

import pandas as pd
import os

# This functions displays a user input box for the user to choose which dataset they want to upload.
# The datasets: valentia.csv * johnsTC.csv(Johnstown Castle)
# It loads the dataset and the required columns. Returns the dataset uploaded to the DataFrame.
def load_wind_dataset():
   
    # Define the two dataset options
    datasets = {
        "1": {"name": "Valentia", "path": "./data/valentia.csv", "skiprows": 23},
        "2": {"name": "Johnstown Castle", "path": "./data/johnsTC.csv", "skiprows": 17},
    }

    # Display the menu
    print("Choose a dataset to analyze:")
    print("1. Valentia dataset")
    print("2. Johnstown Castle dataset")
    choice = input("Enter your choice (1 or 2): ").strip()

    # Making sure the choice is valid
    if choice not in datasets:
        print("Invalid choice. Please run the program again and select 1 or 2.")
        return None

    # Get the selected dataset configuration
    dataset = datasets[choice]
    input_file_path = dataset["path"]
    rows_to_skip = dataset["skiprows"]

    print(f"Loading the {dataset['name']} dataset...")
    
    # Check if the file exists
    if not os.path.exists(input_file_path):
        print(f"File not found: {input_file_path}")
        return None

    # Load the dataset and select only the required columns
    try:
        df = pd.read_csv(input_file_path, skiprows=rows_to_skip, low_memory=False)
        # Select only the required columns
        required_columns = ['date', 'rain', 'temp', 'vappr', 'msl', 'wdsp', 'wddir']
        df_wind_project = df[required_columns].copy()
        print("Dataset loaded successfully!")
        return df_wind_project
    except KeyError as e:
        print(f"Error: One or more required columns are missing in the dataset: {e}")
        return None
    except Exception as e:
        print(f"Error loading the dataset: {e}")
        return None
