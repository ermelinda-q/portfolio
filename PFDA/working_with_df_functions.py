###########################################
### PFDA - BIG PROJECT - functions file ###
###########################################

# This file contains all functions that deal with working with the DataFrame.

# Author: E. Qejvani

import pandas as pd
import math 
from calculation_functions import *

################## Function 1 ########################

# This function counts the rows with empty cells or a single space as a value.
def count_rows_with_empty_or_space_cells_detail(df):  
    # Create a Boolean DataFrame where cells equal ' ' or NaN are True
    df_boolean = (df == ' ') | (df.isnull())  # Checks for both empty space ' ' and NaN values

    # Count the number of missing values (spaces or NaN) in each row
    row_counts = df_boolean.sum(axis=1)

    # Create a dictionary to store how many rows have missing cells
    missing_counts = row_counts.value_counts().sort_index()
    # Variable to hold the rows with at least one empty cell
    total_rows_with_no_value = 0
    # Print the detailed count of rows with empty cells and add the total
    for count, rows in missing_counts.items():
        print(f"Rows with {count} empty cells: {rows}")
        if count > 0:  # Only add rows with at least one empty cell
            total_rows_with_no_value += rows
    
    print(f"Total rows with at least one empty values: {total_rows_with_no_value}")

    # Return the total rows with all values
    return total_rows_with_no_value


################### Function 2 ##########################

# This function cleans/removes all the rows that contain missing data in the DataFrame.
def remove_rows_with_missing_data(df):
   
    # Replace empty strings and single spaces with NaN for consistent handling
    df = df.replace(['', ' '], pd.NA)
    
    # Drop rows where any value is NaN
    df_cleaned = df.dropna()
    
    return df_cleaned


##################### Function 3 ############################

# This function groups a given dataset by the time entered as a parameter.
def group_by_dataset(df, time='D'):
    if time == 'decade':
        # Create a temporary DataFrame with the 'decade' column
        df_temp = df.copy()  # Avoid modifying the original DataFrame
        df_temp['decade'] = (df_temp.index.year // 10) * 10
        # Group by decade.
        grouped_df = df_temp.groupby('decade').size()
    else:
        # For daily, weekly, monthly, or yearly grouping
        grouped_df = df.resample(time).size()
    
    return grouped_df


##################### Function 4 ############################


# Define a function to label seasons more clearly based on the Irish Season.
def get_season(month):
    
    if month in [11, 12, 1]:
        return 'Winter'
    elif month in [2, 3, 4]:
        return 'Spring'
    elif month in [5, 6, 7]:
        return 'Summer'
    else:
        return 'Autumn'


##################### Function 5 ############################   
    
def add_new_column(df, column):
    if column == 'power_kw':
        # Add power output column
        df['power_kw'] = df.apply(
            lambda row: calculate_power_for_row(row['wdsp_m/s'], row['air_density']), axis=1
        )
        df = df.drop(columns=['wddir'])
    elif column == 'air_density':
        # Add air density column
        df['air_density'] = df.apply(
            lambda row: calculate_air_density(row['temp'], row['vappr'], row['msl']), axis=1
        )
        # Remove the columns that are no longer needed for air density calculation
        df = df.drop(columns=['temp', 'vappr', 'msl'])
    elif column == 'in_range':
        # Add in_range column to check if wind speed is in range [4, 25]
        df['in_range'] = (df['wdsp_m/s'] >= 4) & (df['wdsp_m/s'] <= 25)
    elif column == 'hours_in_range':
        # Add hours_in_range column to count hours with wind speed in range [4, 25]
        df['in_range'] = (df['wdsp_m/s'] >= 4) & (df['wdsp_m/s'] <= 25)
        df['hours_in_range'] = df['in_range'].astype(int)
    
    return df