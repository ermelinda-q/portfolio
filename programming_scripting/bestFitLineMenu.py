# This file contains Best fit line Submenu and function that will be used when user enters choice 7 from the main menu.
# Author: Ermelinda Qejvani.
import os 
import matplotlib.pyplot as plt 
import pandas as pd 
import numpy as np 

df = pd.read_csv("iris.csv", skip_blank_lines=True) 

def best_fit_line(x_var, y_var, plot_title, save_dir="IrisGraphs/BestFitLine/", x_label="X-axis", y_label="Y-axis"):
    
    os.makedirs(save_dir, exist_ok=True)            # Check the directory exists, if not create it.
    
    try:
        m, c = np.polyfit(x_var, y_var, 1)           # Fit a straight line between x and y.
        fig, ax = plt.subplots()                     # Create a new figure and set of axis.
        
        ax.plot(x_var, y_var, 'x', label='Data points')      # Assign x and y to the plot.

        # Use the formula for Best Fit Line with my variables.
        ax.plot(x_var, m * x_var + c, 'r-', label='Best fit line')

        ax.set_xlabel(x_label)                               # Setting axis labels.
        ax.set_ylabel(y_label)

        ax.set_title(plot_title)                             # Set title.
        ax.legend()                                          # Add legend.
        filename = f"{x_label} vs {y_label}.png"             # Setting filename as user input for axis labels.
       
        filepath = os.path.join(save_dir, filename)           # Set the filepath where to save the file.
        plt.savefig(filepath)  # Save the plot to the specified directory.
        plt.close()  # Close the plot to free up memory.

        print(f"Scatter plot of {x_label} vs {y_label} successfully saved in {filepath}")  # Print output message with info about the file.
    except Exception as e:
        print(f"An error occurred while creating or saving the scatter plot: {e}")  # Print error message.
        
def best_fit_line_menu():
    try:
        # Display submenu.
        print("\n*** Best Fit LIne - Choose the pair of Variables You want to compare.***")
        print("1. Sepal Length vs Sepal Width")
        print("2. Sepal Length vs Petal Length")
        print("3. Sepal Length vs Petal Width")
        print("4. Sepal Width vs Petal Length")
        print("5. Sepal Width vs Petal Width")
        print("6. Petal Length vs Petal Width")
        print("7. Generate all of above Best Fit Lines")
        print("8. Return to Main Menu")

        choice = input("Enter your choice: ")               # Choice is a user input.
        # Based on user input we call the function above with the variables we want to compare and build the best fit line.
        if choice == '1':
            best_fit_line(df['sepal_length'], df['sepal_width'], plot_title="Best Fit Line: Sepal Length - Sepal Width", save_dir="IrisGraphs/BestFitLine/", x_label="Sepal Length", y_label="Sepal Width")
        elif choice == '2':
            best_fit_line(df['sepal_length'], df['petal_length'], plot_title="Best Fit Line: Sepal Length - Petal Length", save_dir="IrisGraphs/BestFitLine/", x_label="Sepal Length", y_label="Petal Length")
        elif choice == '3':
            best_fit_line(df['sepal_length'], df['petal_width'], plot_title="Best Fit Line: Sepal Length - Petal Width", save_dir="IrisGraphs/BestFitLine/", x_label="Sepal Length", y_label="Petal Width")
        elif choice == '4':
            best_fit_line(df['sepal_width'], df['petal_length'], plot_title="Best Fit Line: Sepal Width - Petal Length", save_dir="IrisGraphs/BestFitLine/", x_label="Sepal Width", y_label="Petal Length")
        elif choice == '5':
            best_fit_line(df['sepal_width'], df['petal_width'], plot_title="Best Fit Line: Sepal Width - Petal Width", save_dir="IrisGraphs/BestFitLine/", x_label="Sepal Width", y_label="Petal Width")
        elif choice == '6':
            best_fit_line(df['petal_length'], df['petal_width'], plot_title="Best Fit Line: Petal Length - Petal Width", save_dir="IrisGraphs/BestFitLine/", x_label="Petal Length", y_label="Petal Width")
        elif choice == '7':
            best_fit_line(df['sepal_length'], df['sepal_width'], plot_title="Best Fit Line: Sepal Length - Sepal Width", save_dir="IrisGraphs/BestFitLine/", x_label="Sepal Length", y_label="Sepal Width")
            best_fit_line(df['sepal_length'], df['petal_length'], plot_title="Best Fit Line: Sepal Length - Petal Length", save_dir="IrisGraphs/BestFitLine/", x_label="Sepal Length", y_label="Petal Length")
            best_fit_line(df['sepal_length'], df['petal_width'], plot_title="Best Fit Line: Sepal Length - Petal Width", save_dir="IrisGraphs/BestFitLine/", x_label="Sepal Length", y_label="Petal Width")
            best_fit_line(df['sepal_width'], df['petal_length'], plot_title="Best Fit Line: Sepal Width - Petal Length", save_dir="IrisGraphs/BestFitLine/", x_label="Sepal Width", y_label="Petal Length")
            best_fit_line(df['sepal_width'], df['petal_width'], plot_title="Best Fit Line: Sepal Width - Petal Width", save_dir="IrisGraphs/BestFitLine/", x_label="Sepal Width", y_label="Petal Width")
            best_fit_line(df['petal_length'], df['petal_width'], plot_title="Best Fit Line: Petal Length - Petal Width", save_dir="IrisGraphs/BestFitLine/", x_label="Petal Length", y_label="Petal Width")       
        elif choice == '8':
            print("Returning to Main Menu.")
        else:
            print("Invalid choice. Please enter a number between 1 and 8.")
    except Exception as e:
        print("Error calculating correlation:", str(e))