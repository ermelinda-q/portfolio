# This file contains functions for main file analysis.txt
# Author: Ermelinda Qejvani

import numpy as np                  
import seaborn as sns 
import matplotlib.pyplot as plt 
import numpy as np 
import os                               # Working with file and folder paths.

################################################################################
####################        Text file function              ####################
################################################################################
# Creating a text file to write the data from running the program
# Using 'w' parameter we make sure that if the file doesn't exist it is created. 
# It will also empty the content of the file every time the program is run.

def create_empty_file(my_file):
    # Open the file in 'write' mode ('w'). If the file doesn't exist, it will be created.
    # If the file already exists, its contents will be overwritten.
    try:
        with open(my_file, 'w') as file:
        # Write a message as the First line of the text file and a short introduction.
            file.write("This is my analysis of Iris DataSet.\n\nIris data set is a collection of measurements taken from three species of Iris flowers: "
                   "\na. Iris Setoza.\nb. Iris Versicolor.\nc. Iris Virginica.\n"
                   "\nThe dataset is widely used in the field of data science, making it an excellent resource for teaching and learning."
                   "\nEach species studied in the dataset has 50 samples, and four measurements:\na. sepal length.\nb. sepal width.\nc. petal length.\nd. petal width.\n"
                   "\nThe aim of this program is to show what information we can get from the dataset using Python programming language and its libraries."
                   "\n************************************************************************************************************************************\n") 
        print(f"File '{my_file}' successfully created.")            # message that file is created.
    except Exception as e:
        print("Error saving information to file:", str(e))          # print error message.
        
################################################################################
####################           Histogram Function           ####################
################################################################################

# Function to generate a histogram file of all variables.
def create_iris_histograms(df, save_dir="./IrisGraphs/"):                                 # Name of Function using df(DataFrame).
    os.makedirs(save_dir, exist_ok=True)                        # Check the directory exists, if not create it.
    try:
        fig1, axes = plt.subplots(2, 2, figsize=(12, 12))       # Create a 2x2 grid of subplots and set figure size.

        # Plot histograms for each feature with hue based on species.
        sns.histplot(data=df, x="sepal_length", hue="species", ax=axes[0, 0]).set_title("Sepal Length")
        sns.histplot(data=df, x="sepal_width", hue="species", ax=axes[0, 1]).set_title("Sepal Width")
        sns.histplot(data=df, x="petal_length", hue="species", ax=axes[1, 0]).set_title("Petal Length")
        sns.histplot(data=df, x="petal_width", hue="species", ax=axes[1, 1]).set_title("Petal Width")

        plt.suptitle("Histogram of Iris flowers")                   # Set the main title for the figure.

        plt.savefig("./IrisGraphs/VariablesHistogram.png")          # Save figure to file.
        print("Histogram of Iris DataSet successfully saved as VariablesHistogram in ./IrisGraphs/ directory.")     # Print message.
    except Exception as e:
        print("Error generating histogram:", str(e))                # Print error message.


#################################################################################
####################           Pairplots Functions          #####################
#################################################################################

# Function 1 to generate and save pairplot of variables for a given species.
# df = DataFrame, species = name of species as string, save_dir = Directory to save the plots.
def species_pairplot_to_folder(df, species_name, save_dir="./IrisGraphs/"):
    os.makedirs(save_dir, exist_ok=True)                              # Check the directory exists, if not create it.
    try:
        sns.pairplot(df, height=1.5)                                  # Create pairplot for the given dataframe with the given height.
        plt.suptitle(f"Iris {species_name} variables")                # Set title for the pairplot.
        save_path = f"{save_dir}/Iris{species_name}Variables.png"     # Create path and file name of pairplot.
        plt.savefig(save_path)                                        # Save the plot.
        plt.close()                                                   # Close the plot to free up memory
        print(f"Iris {species_name} pairplot successfully saved in {save_dir} directory.")      # Print message with the file name and directory.
    except Exception as e:
        print("Error generating pairplot:", str(e))                   # Print error message if something goes wrong.
        
        
# Function 2 to generate a pairplot graph of all variables in the DataFrame.
# df = DataFrame, save_dir = Directory to save the plots, filename = pairplot's filename.
def save_iris_pairplot(df, save_dir="./IrisGraphs/", filename="PairPlotOfVariables.png"):
    os.makedirs(save_dir, exist_ok=True)                                # Check the directory exists, if not create it.
    try:
        sns.pairplot(df, hue='species', height=1.5)                     # Create the pairplot.
        plt.suptitle("Relationship between Iris dataset variables", fontsize=10)        # Add a title to the figure.
        filepath = os.path.join(save_dir, filename)                     # Set the filepath where to save the file.
        plt.savefig(filepath)                                           # Save the plot to the specified directory.
        plt.close()                                                     # Close the plot to free up memory
        # Print message that file is created.
        print(f"Pairplot of Iris DataSet variables successfully saved as {filename} in {save_dir} directory.")
    except Exception as e:                  
        print(f"An error occurred while creating or saving the pairplot: {e}")  # print error message.


# This function will generate plots to compare any two variables of all three species.
# df = DataFrame, x_var = specified variable, y_variable, plot_title = title of graph, save_dir = Directory to save the plots, filename = pairplot's filename.
def plot_iris_petal_or_sepal(df, x_var, y_var, plot_title, save_dir="./IrisGraphs/", filename="IrisScatterPlot.png"):
    os.makedirs(save_dir, exist_ok=True)                                  # Check the directory exists, if not create it.
    try:
        df_setosa = df[df['species'] == 'setosa']                         # Create subsets of each species from the DataFrame(df).
        df_versicolor = df[df['species'] == 'versicolor']
        df_virginica = df[df['species'] == 'virginica']

        fig, ax = plt.subplots()                                          # Create the scatter plot figure.
        fig.set_size_inches(10, 5)                                        # Set the length and width of the plot.
        # Plot scatter points.
        ax.scatter(df_setosa[x_var], df_setosa[y_var], label="Setosa", facecolor="blue")
        ax.scatter(df_versicolor[x_var], df_versicolor[y_var], label="Versicolor", facecolor="green")
        ax.scatter(df_virginica[x_var], df_virginica[y_var], label="Virginica", facecolor="red")

        # Using the x and y variables passed in the function, set labels of the graph by removing '_' and add space between words.
        ax.set_xlabel(x_var.replace('_', ' ').title())
        ax.set_ylabel(y_var.replace('_', ' ').title())
        ax.grid()                                               # Set grid to visible for easy reading.
        ax.set_title(plot_title)                                # Set title of the graph.
        ax.legend()                                             # Show legend (use default values).

        filepath = os.path.join(save_dir, filename)             # Set the filepath where to save the file.
        plt.savefig(filepath)                                   # Save the plot to the specified directory
        plt.close()                                             # Close the plot to free up memory.

        print(f"Scatter plot of {x_var} vs {y_var} for Iris species successfully saved in {filepath}")  # Print output message with info about the file.
    except Exception as e:
        print(f"An error occurred while creating or saving the scatter plot: {e}")                      # Print error message.
        

        
        
        