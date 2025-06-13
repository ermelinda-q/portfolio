# PROJECT

## Programming for Data Analytics (PFDA)

#### by E. Qejvani
***

This README has been written with [GitHub's documentation on READMEs](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes) in mind.
You should refer to that documentation for more information on writing an appropriate README for visitors to your repository.
You can find out more about [writing in MarkDown in GitHub's documentation](https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax).

***

## About this Repository

This Git sub-repository (PFDA/project) contains my project file `project.ipynb` along with all the necessary files required to run it. It is part of my Programming for Data Analytics module, which is a component of the [Higher Diploma in Computer Science in Data Analytics](https://www.atu.ie/courses/higher-diploma-in-science-data-analytics#:~:text=You%20are%20a%20Level%208,topics%20in%20your%20original%20degree) at [ATU](https://www.atu.ie/).

**Structure of this Sub-Repository**

```
./PFDA/                             # Main folder/this sub-directory.
├── data/                           # Folder containing the `.csv` files.
│   ├── johnsTC.csv                 # Johnstown Castle weather station dataset.
│   └── valentia.csv                # Valentia Island weather station dataset.
├── files                           # Folder containing PDF files used as guides for the project.
│   ├── Community-Toolkit-Onshore-Wind.pdf
│   ├── Energy-11-Wind-Energy.pdf
│   ├── rain-erosion-maps-for-wind-turbines.pdf
│   └── ProjectDescription.pdf
├── README.md                       # Main repository overview (this file).
├── calculation_functions.py        # Python file containing functions for various calculations.
├── menu_code.py                    # Python file with a menu function for selecting the dataset to explore.
├── project.ipynb                   # Main project file.
└── working_with_df_functions.py    # Python file with functions for manipulating the dataset.
```
***
## About the Project

The goal of my project was to create an interactive data analysis tool where users can choose between two different weather station datasets: Johnstown Castle and Valentia Island — to explore wind energy trends and evaluate some of the conditions for possibly building a wind farm, such as wind speed and the power it can generate. The project serves as a general guide to help users understand how weather data can be analyzed to assess different factors in wind farm development.

The datasets contain hourly measurements of key meteorological parameters such as temperature, wind speed, wind direction, and pressure, which are crucial for assessing wind energy potential. The user can select the dataset of their choice and view analysis results, including linear regression trends on wind speed and energy production.

 The notebook and Python functions are built to work with other weather datasets as long as they have the same columns (like wind speed, temperature, and other weather data). This makes the project a useful tool for analyzing many different weather datasets, not just the ones from Johnstown Castle and Valentia Island.

**Part 1 - Preparing the Dataset**
- Purpose: Clean and format the dataset for analysis. This step involves loading the data, converting the necessary columns into the appropriate data types, and preparing the time series for analysis. Missing data is handled, and wind speed is converted to meters per second for consistency.

  - _Some of the Functions used:_
    - `load_wind_dataset()`: Loads the dataset. Function found in `menu_code.py` file.
    - `convert_columns_to_float(columns to convert)`: Converts the data in the specified columns to float32(`.float32`). Function found in `calculation_functions.py` file.
    - `count_rows_with_empty_or_space_cells_detail(df)`: Counts all the rows containing Nan value, no value or single space value and returns a message how many rows contain 1, 2, etc.. invalid cells. Found in `working_with_df_functions.py` file.
    - `remove_rows_with_missing_data(df)`: Removed all the rows that hold invalid cells from above. File found in Found in `working_with_df_functions.py` file.
  - _References:_
    - [The problem with `float32`](https://pythonspeed.com/articles/float64-float32-precision/)
    - [Pandas: read .csv](https://pandas.pydata.org/docs/reference/api/pandas.read_csv.html)
    - [Convert temperature from `knot` to `metre per second`](https://www.inchcalculator.com/convert/knot-to-meter-per-second)

**Part 2 - Analyzing the Data**
- Purpose:Perform deeper analysis on the weather variables to assess their relationship with wind energy. By calculating air density and estimating power output based on wind speed and other factors, we can get insights into the wind turbine's potential for energy generation.
  - _Some of the Functions used:_ 
    - `add_new_column(df, column)`: This functions is found in `working_with_df_functions.py` file and call two functions inside based on the users choice:
        - `def calculate_air_density(temp, vappr, msl)`: Air density is calculated using the ideal gas law based on the data in the dataset.
        - `def calculate_power_for_row(windspeed, air_density)`: Power output is estimated with a formula that factors in wind speed, air density, and turbine size.
  - _References:_
    - [Understanding the Wind Power Equation](https://solidwize.com/wp-content/uploads/2013/07/7-Understanding-the-Wind-Power-Equation.pdf)
    - [Wind Turbine Model: Senvion MM100](https://en.wind-turbine-models.com/turbines/890-senvion-mm100)
    - [Density of Air Calculations](https://en.wikipedia.org/wiki/Density_of_air)

**Part 3 - Operational Range Analysis**
- Purpose: Analyze when the wind turbine is within its operational range. This is done by calculating how many hours the wind speed stays within the turbine’s operational limits (3 m/s to 22 m/s). The data is filtered to reflect this range, and power output is adjusted accordingly.
  - _Some of the Functions used:_
    - `add_new_column(df, column)`: This functions is found in `working_with_df_functions.py` file and call two functions inside based on the users choice:
        - Adds `in_range` column to check if wind speed is in range [4, 25]
        - Add `hours_in_range` column to count hours with wind speed in range [4, 25]
    - Descriptive statistics are applied to summarize key variables like wind speed, air density, and power output.
  - _References:_ 
    - [Community Toolkit Onshore Wind](./files/Community-Toolkit-Onshore-Wind.pdf)
    - [Select Rows Between Two Values](https://stackoverflow.com/questions/31617845/how-to-select-rows-in-a-dataframe-between-two-values)
    
**Part 4 - Seasonal Analysis**
- Purpose: Understand the variation in wind speed and power output across seasons. The analysis helps identify the best seasons for wind energy production by comparing seasonal averages of key metrics like wind speed and power output.
  - _Some of the Functions used:_ 
    - Data is grouped by season, and average values are calculated for each season.
    - Visualizations like stacked bar charts and pie charts are created to highlight seasonal contributions to wind energy generation.
  - _References:_ 
    - [Pandas - groupby](https://pandas.pydata.org/docs/reference/groupby.html)

**Part 5 - Trend Analysis**
- Purpose: Analyze wind speed and power output trends over the past 20 years (2004-2024) to detect long-term patterns. This analysis involves random sampling to study wind variations on selected days and applying linear regression to analyze yearly trends.
  - _Some of the Functions used:_ 
    - `.random.choice()`: Used for random sampling to explore daily variations.
    - `linregress()`: Applies linear regression to detect long-term trends in yearly data.
  - _References:_ 
    - [Random number as a subset](https://stackoverflow.com/questions/38085547/random-sample-of-a-subset-of-a-dataframe-in-pandas)
    - [Linear Regression in Python](https://realpython.com/linear-regression-in-python/)

**Last Part - Predictions**
- Purpose: Predict future wind energy performance. Linear regression is used to forecast power and wind speed trends for 2025-2029, while SARIMA models forecast wind conditions for spring 2025, capturing seasonal patterns.
  - _Some of the Functions used:_ 
    - `linregress()`: Used for predicting long-term trends based on historical data.
    - `SARIMAX()`: Used for SARIMA models to forecast seasonal wind speed and power output.
  - _References:_ 
    - [ChapGPT](https://chatgpt.com/)
    - [pandas.DataFrame.resample](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.resample.html)
    - [Linear Regression with Pandas DataFrame](https://saturncloud.io/blog/linear-regression-with-pandas-dataframe/)
    - [SARIMA](https://www.geeksforgeeks.org/sarima-seasonal-autoregressive-integrated-moving-average/)

## Get Started - How To run this files

To run the files stored in this repository you will need to download and install in your computer the following apps:

- [Anaconda](https://www.anaconda.com/) - open-source platform that allows you to write and execute code in Python. A guide how to install Anaconda in your computer can be found [here](https://docs.anaconda.com/free/anaconda/install/index.html).
- [Visual Studio Code](https://code.visualstudio.com/) - source code editor for developers. With Visual Studio Code you can open and run all python files(ending with .py). A guide how to install and setup Visual Studio Code in your computer can be found [here](https://code.visualstudio.com/learn/get-started/basics).
- [Git](https://git-scm.com/downloads) - will help you to download a copy of this repository in your local machine. Installation guide can be found [here](https://github.com/git-guides/install-git).

To make a copy of this repository in your computer/local machine run the following command:

```
git clone https://github.com/ermelinda-q/PFDA/tree/main/project
```

## Contributions

Feel free to contribute by submitting pull requests for improvements or additional work.

***