# Managing Film and Actor Data - Applied Databases

_by E. Qejvani_
***

## Overview

This Python application interacts with two databases:
- **MySQL**: Stores film and actor-related information.
- **Neo4j**: Stores relationships between actors, their marital status.

The application provides a menu-driven interface to manage and display film and actor data. The user can perform various actions such as viewing directors and films, adding new actors, viewing married actors, and more.

***
## Databases

- **MySQL Database** (`appdbproj`)
- **Neo4j Database** (`actorsMarried`)
_The `actorsMarried.json` file is imported into this Neo4j database to represent actor relationships._

## Main Menu

The application displays a main menu with the following options:

1. **View Directors & Films**
2. **View Actors by Month of Birth**
3. **Add New Actor**
4. **View Married Actors**
5. **Add Actor Marriage**
6. **View Studios**
7. **Create/Run Procedure**
8. **Generate Reports**
x. **Exit Application**

***
## Features

### 1. **View Directors & Films**
- The user is asked to enter a director's name (or part of the name).
- For each director that matches the entered string, the following details are displayed:
  - Director’s name
  - Films they directed
  - Studio that produced the films

If no director matches the search, the user is informed and returned to the main menu.

### 2. **View Actors by Month of Birth**
- The user is prompted to enter a month (as a number or the first three letters).
- The application displays the following details for each actor born in that month:
  - Actor’s Name
  - Actor's DOB
  - Actor's Gender

If an invalid month is entered, the user is asked to enter a valid month again.

### 3. **Add New Actor**
- The user is asked to enter details for a new actor:
  - Actor ID
  - Actor Name
  - Actor DOB
  - Actor Gender
  - ID of country the actor is from
- If the actor is successfully added, a confirmation message is shown.
- Error handling for invalid actor IDs, existing IDs, and invalid country IDs is in place.

### 4. **View Married Actors**
- The user is prompted to enter an actor ID.
- The system checks the Neo4j database for any "MARRIED_TO" relationships.
- If the actor is married, their spouse's details are displayed.

If no marriage relationship exists, the user is informed, and if the actor ID doesn't exist, the user is also notified.

### 5. **Add Actor Marriage**
- The user is prompted to enter two actor IDs.
- If both actors exist in the MySQL database and are unmarried, a "MARRIED_TO" relationship is created between them in the Neo4j database.
- Several error conditions are handled, such as invalid IDs, actors marrying themselves, or already married actors.

### 6. **View Studios**
- Displays all studio IDs and names, sorted by studio ID.
- New studios added after the first time this option is chosen will not be displayed until the application is restarted.

### 7. **Create/Run Procedure**
- Creates or runs(if already saved) a procedure to display films released in a specified year, showing details like title, release date, budget, earnings, and profit.
- It allows the user to input the year and the number of records to display, with the results sorted by profit in descending order.

### 8. **Generate Reports**
- Displays a submenu to generate different reports such as database info, actors' data, and studio statistics.
- It saves these reports as text files in a "reports" folder.

### 7. **Exit Application**
- Terminates the program.

***
## Setup

### MySQL Setup
1. Ensure MySQL is installed and running.
2. Create the `appdbproj` database and import the necessary tables.
3. Update the connection details in the Python code to match your MySQL setup.

### Neo4j Setup
1. Install Neo4j and start the database.
2. Import the `actorsMarried.json` file into the Neo4j database.

### Running the Application
1. Clone or download the project files.
2. Install the required Python libraries using `pip`:
   ```bash
   pip install mysql-connector-python neo4j


***
## References

- Applied Databases Module - Lectures by Gerard Harrison
- [SELECT EXISTS](https://stackoverflow.com/questions/61533435/what-does-it-mean-select-exists-select-1-from-favoritelist-where-id-id)
- [Exeptions & Errors](https://www.mikusa.com/python-mysql-docs/exceptions.html)
- [Neo4j Python Driver Manual](https://neo4j.com/docs/python-manual/current/#session-context-manager)