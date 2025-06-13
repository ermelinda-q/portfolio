###########################################
### PFDA - BIG PROJECT - functions file ###
###########################################

# This file contains all functions that deal with working with the DataFrame.

# Author: E. Qejvani

import pandas as pd
import math 
from scipy.stats import linregress
from working_with_df_functions import *

##################### Function 1 ########################

# This function converts the data type of a column/columns to numeric data.
# I'm converting the data type to float32 to use less memory because of the large amount of data in my dataset.
def convert_columns_to_float(df, columns):
   
    # loop to convert more than one set/column of data to numeric.
    for column in columns:
        df[column] = pd.to_numeric(df[column], errors='coerce').astype('float32') 
    return df


#################### Function 2 #########################

# This function calculate air density(kg/m³) from data available in the dataset: temperature, vapor pressure and mean sea level pressure.
def calculate_air_density(temp, vappr, msl):
    
    # Constants needed for our formula
    R_dry = 287.05  # Specific gas constant for dry air in J/(kg·K)
    R_vapor = 461.5  # Specific gas constant for water vapor in J/(kg·K)
    
    # Convert temperature to Kelvin
    T = temp + 273.15
    
    # Convert vapor pressure and mean sea level pressure from hectoPascals(hPa) to Pascals(Pa)
    P_vapor = vappr * 100  # Vapour pressure in Pa
    P_msl = msl * 100  # Mean sea level pressure in Pa
    
    # Calculate the partial pressure of dry air
    P_dry = P_msl - P_vapor  # Dry air pressure in Pa
    
    # Calculate air density using the formula
    air_density = (P_dry / (R_dry * T)) + (P_vapor / (R_vapor * T))
    
    return air_density

#################### Function 3 #########################

def calculate_power_for_row(windspeed, air_density):
    # Check if the wind turbine is operational
    if windspeed < 3 or windspeed > 22:
        return 0  # No power generated outside the operational range
    
    # Calculate the swept area
    diameter = 100
    radius = diameter / 2
    swept_area = math.pi * radius**2  # in square meters
    
    # Calculate the power output
    efficiency = 0.4
    power = 0.5 * air_density * swept_area * windspeed**3 * efficiency
    
    # Convert watts to kilowatts
    power_kw = round(power / 1000, 2)  # divide by 1000 to get kW
    
    return power_kw


#################### Function 4 #########################

# This function analyzes the trend of a given column over the last 20 years(or specified range)
# Parameters used: df, column name, start year, end year.

def analyze_column_trend(df, column_name, start_year=2004, end_year=2024):
   
    # Extract year for grouping
    df['year'] = df.index.year

    # Define date range
    start_date = f'{start_year}-01-01'
    end_date = f'{end_year}-12-31'

    # Filter data for the specified range
    df_filtered = df.loc[start_date:end_date]

    # Group by year and calculate yearly sums for the specified column
    yearly_data = df_filtered.groupby('year')[column_name].sum()

    # Perform linear regression
    years = yearly_data.index
    slope, intercept, r_value, p_value, std_err = linregress(years, yearly_data.values)

    # Determine the type of data being analyzed (Wind or Power)
    if column_name == 'hours_in_range':
        data_type = 'Wind'
    elif column_name == 'power_kw':
        data_type = 'Power'
    else:
        data_type = 'Unknown'

    # Print regression details
    print(f"Analysis for '{column_name}' ({data_type} Data) from {start_year} to {end_year}:")
    print(f"Linear Trend: Slope = {slope:.2f} units/year, Intercept = {intercept:.2f}")
    print(f"R-squared = {r_value**2:.2f}, p-value = {p_value:.2e}")
    print(f"Minimum {column_name} per Year: {yearly_data.min()}")
    print(f"Maximum {column_name} per Year: {yearly_data.max()}")

    return yearly_data, slope, intercept, r_value, p_value, std_err, data_type

