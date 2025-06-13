# Programming and Scripting
# Task - Project
# This program is based on the well-known Fisher’s Iris data set.
# This program should:
# 1. Output a summary of each variable to a single text file,
# 2. Save a histogram of each variable to png files, and
# 3. Output a scatter plot of each pair of variables.
# 4. Perform any other analysis you think is appropriate.

# Author: Ermelinda Qejvani

# First I'm importing all libraries that I can use to work/manipulate data files
import pandas as pd                         # Data Frame.
import numpy as np                          # Numerical arrays.
import matplotlib.pyplot as plt             # Plotting.
import seaborn as sns                       # Subplotting.
# from skimpy import skim                     # Generating quick summaries.
from scipy.stats import pearsonr            # Pearson's correlation coefficient.
from analysisFunctions import *             # Functions created to use running this program.
from bestFitLineMenu import *               # Best Fit Line function and submenu.   
from correlation import *                   # Correlation function and submenu.
import warnings                             # importing warning to deal with warning messages.
warnings.filterwarnings("ignore", message="The figure layout has changed to tight")

# Start the program.
def main():
    # Loading dataset into DataFrame (df). Defining variables to use in the program.
    df = pd.read_csv("iris.csv", skip_blank_lines=True)         
    df_describe = df.describe(include="all")                # variable df_describes stores output of .describe command.
    df_types = df.dtypes                                    # variable df_types stores output of .dtypes(data type) command.
    df_species = df["species"].value_counts()               # variable df_species stores number of each flower in the DataSet.

    # Creating subset for each dataset by species to use later in the program.
    df_setosa = df[df["species"] == "setosa"]           
    df_versicolor = df[df["species"] == "versicolor"]
    df_virginica = df[df["species"] == "virginica"]
    
    while True:
        print("\n*** Iris Dataset Main Menu ***")
        print("1. Display a description of Dataset using Skimpy")
        print("2. Generate a text file with information about Dataset")
        print("3. Generate Histogram of all Variables")
        print("4. Generate Pairplots of all Variables")
        print("5. Generate Pairplots for Variables of each Species")
        print("6. Generate Scatterplots for Petals and Sepals of each Species")
        print("7. Generate Best Fit Line of Variables(Submenu)")
        print("8. Calculate and write to file Correlation between variables")
        print("9. Exit the program")
        
        user_choice = input("Enter your choice: ")
        
        if user_choice == '1':
            print("\nIris Dataset Summary using Skimpy package")
            skim(df)
        elif user_choice == '2':
            # Creating 'analysis.txt' file and calling the function create_empty_file to start writing in the file.
            my_file = "analysis.txt"  
            create_empty_file(my_file)
            print(f"File '{my_file}' contains information about Iris DataSet and its variables.")   # Message output.


            # Generating info from the dataset and writing in our file: analysis.txt
            with open(my_file, 'a') as file:
                file.write("\nUsing command 'df.columns' we can get the Column labels of the DataSet which are:\n"
                        "---------------------------------------------------------------------------------\n")
                for i, label in enumerate(df.columns):
                    file.write(f"{i+1}. {label}\n")
                
                file.write("\n\nFinding out data types in the Dataset using 'df.dtypes' command:\n"
                        "----------------------------------------------------------------\n" + df_types.to_string()) 
                file.write("\n\nMain species in the dataset using 'df['species'].value_count' command:\n"
                        "----------------------------------------------------------------------\n"+ df_species.to_string())  
                file.write("\n\nSummary of the Iris dataset using 'df.describe()' command:\n"
                    "----------------------------------------------------------\n")
                file.write(df_describe.to_string())
                file.write("\n\nPlease note that 'df.describe()' command gives us information about the whole dataset."
                        "\nTo get a more accurate information about the different flower species I created subsets for each flower.\n") 
                file.write("\n\nThe next section shows the mean values of each variable in the dataset for each species.\n"
                        "----------------------------------------------------------------------------------------"
                        "\nI am using 'df.groupby('species')' command:\n"
                        "-------------------------------------------\n")
                file.write((df.groupby("species").mean()).to_string())
                
                file.write("\n\nIn the next section I will use 'df_specie.describe()' command to get information about each of species.\n"
                        "*******************************************************************************************************\n")
                file.write("\nSummary of Iris Setosa:\n-----------------------\n" + df_setosa.describe(include="all").to_string())
                file.write("\n\nSummary of Iris Versicolor:\n---------------------------\n" +df_versicolor.describe(include="all").to_string())
                file.write("\n\nSummary of Iris Virginica:\n--------------------------\n" + df_virginica.describe(include="all").to_string())
        elif user_choice == '3':
            create_iris_histograms(df)                                   # Calling function from analysisFunctions file to created a histogram.
        elif user_choice == '4':
            save_iris_pairplot(df)                                        # function to create a pairplot graph of all variables in dataset.
        elif user_choice == '5':
            species_pairplot_to_folder(df_setosa, "Setosa")               # Relationship of variables in Iris Setosa.
            species_pairplot_to_folder(df_versicolor, "Versicolor")       # Relationship of variables in Iris Versicolor.
            species_pairplot_to_folder(df_virginica, "Virginica")         # Relationship of variables in Iris Virginica.
        elif user_choice == '6':
            # Pairplot to show relationship between variables petal_length and petal_width/sepal_length and sepal_width.
            plot_iris_petal_or_sepal(df, 'petal_length', 'petal_width', "Iris Petals", "./IrisGraphs/", "IrisPetals.png")
            plot_iris_petal_or_sepal(df, 'sepal_length', 'sepal_width', "Iris Sepals", "./IrisGraphs/", "IrisSepals.png")
        elif user_choice == '7':
            best_fit_line_menu()                                          # call function from bestFitLineMenu.py
        elif user_choice == '8':
            write_correlations_to_file(df, 'correlation_results.txt')     # call functions in correlation.py file.
        elif user_choice == '9':
            print("Exiting the program.")                                 # Exit the program and end the program.
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 9.") # Print error message.

if __name__ == "__main__":
    main()