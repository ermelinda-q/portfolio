# This file contain calculate_correlation function &
# write_correlation_to_file function to use for choice 8 on the main analysis.py file.
# The function writes a general information about the correlation in correlation_results file.
# The function writes the correlation values and P-values sorted from the strongest to the weakest.

# Author: Ermelinda Qejvani

import pandas as pd
from scipy.stats import pearsonr                # Calculating Pearson correlation.

df = pd.read_csv("iris.csv") 

# Function to calculate correlation between two variables
def calculate_correlation(df, variable1, variable2):
    correlation, p_value = pearsonr(df[variable1], df[variable2])
    return correlation, p_value

# Function to write correlations to a file in a neat table format, sorted by correlation values
def write_correlations_to_file(df, my_file):
    correlations = [
        ('sepal_length', 'sepal_width'),
        ('sepal_length', 'petal_length'),
        ('sepal_length', 'petal_width'),
        ('sepal_width', 'petal_length'),
        ('sepal_width', 'petal_width'),
        ('petal_length', 'petal_width')
    ]
    
    # Calculate all correlations and store them in a list of tuples
    correlation_results = []
    for variable1, variable2 in correlations:
        correlation, p_value = calculate_correlation(df, variable1, variable2)
        correlation_results.append((variable1, variable2, correlation, p_value))
    
    # Sort the list of tuples by the correlation values (3rd element in each tuple)
    correlation_results.sort(key=lambda x: abs(x[2]), reverse=True)
    
    # Open the file in write mode to ensure it is empty before writing
    with open(my_file, 'w') as file:
        file.write("Correlation between Variables of Iris Dataset using 'pearsonr' from 'scipy.stats' library\n"
                   "__________________________________________________________________________________________"
                   "\n\n1. A correlation value (or correlation coefficient) measures the strength and direction of the relationship between two variables."
                   "\n2. It ranges from -1 to +1."
                   "\n\nUnderstanding the Correlation Coefficient:\n"
                   "---------------------------------------------"
                   "\n- Correlation Coefficient: +1/-1 - Perfect positive/negative correlation."
                   "\n- Correlation Coefficient: 0.7 to 0.9/-0.7 to -0.9 - Strong positive/negative correlation."
                   "\n- Correlation Coefficient: 0.4 to 0.6/-0.4 to -0.6 - Moderate positive/negative correlation."
                   "\n- Correlation Coefficient: 0.1 to 0.3/-0.1 to -0.3 - Weak positive/negative correlation"
                   "\n- Correlation Coefficient: 0   -   No correlation\n\n"
                   "The P-Value:\n"
                   "-------------\n\n"
                   "The P-Value helps us figure out if a correlation we see is actually meaningful or just by chance."
                   "\nIf the p-value is less than 0.05, it usually means the correlation is important and not just random.\n\n"
                   "The results below show the correlation between variables in the Iris Dataset sorted in order from the strongest to the weakest.\n\n")
        file.write(f"{'Variable 1':<20}{'Variable 2':<20}{'Correlation':<15}{'P-value':<15}\n")
        file.write(f"{'-'*70}\n")
        
        # Write the sorted correlations to the file
        for variable1, variable2, correlation, p_value in correlation_results:
            file.write(f"{variable1:<20}{variable2:<20}{correlation:<15.2f}{p_value:<15.4f}\n")
    
    print(f"Correlations of variables in Iris Dataset have been written to {my_file}")


