# In this file it is stored the code for creating or running a given procedure.
# The procedure get year and film number to show from the user and displays
# a table: number of record, film title, release date, budget, earnings.
# The last column displays the calculated profit(earnings - budget).
from db_connections import connection_sql

# Create/Run Procedure function.
def create_run_procedure():
    conn = connection_sql()
    cursor = conn.cursor()

    # Check if the procedure already exists
    cursor.execute("SHOW PROCEDURE STATUS WHERE Name = 'GetFilmsByYear';")
    procedure_exists = cursor.fetchone()

    # Displaying information about the procedure.
    print("""
    -----------------------------------------------------------------------------------
    PROCEDURE INFO:
    The 'GetFilmsByYear' procedure gives you a list of films released in a certain year. 
    You need to enter two things: the year and how many records you want to see. 
    It shows the film's name, release date, budget, box office earnings, and calculates 
    profit. The list is sorted by profit from highest to lowest, and only the number of 
    records you choose will be shown
    -----------------------------------------------------------------------------------
    """)

    if not procedure_exists:
        # Drop the procedure if it exists.
        cursor.execute("DROP PROCEDURE IF EXISTS GetFilmsByYear")

        # Create the procedure
        cursor.execute("""
        CREATE PROCEDURE GetFilmsByYear(
        IN inputYear INT,
        IN recordLimit INT
        )
        BEGIN
        SELECT 
            Filmid AS `ID`,
            filmname AS `Film Name`,
            filmreleasedate AS `Release Date`,
            filmbudgetdollars AS `Total Cost`,
            filmboxofficedollars AS `Total Earned`,
            (filmboxofficedollars - filmbudgetdollars) AS `Profit`
        FROM film
        WHERE 
            YEAR(filmreleasedate) = inputYear
        ORDER BY Profit DESC
        LIMIT recordLimit;
        END
        """)

        print("Procedure 'GetFilmsByYear' successfully created.")
    else:
        print("Procedure 'GetFilmsByYear' already exists.")

    # Validate user input for year
    while True:
        try:
            year = int(input("Enter Year: "))
            if year > 1900 and year < 2025:
                break
        except Exception as e:
            continue

    # Validate user input for number of records
    while True:
        try:
            number_of_records = int(input("Enter Number of Films to Display: "))
            if number_of_records > 0:
                break
        except Exception as e:
            continue

    # Call the procedure
    cursor.callproc('GetFilmsByYear', (year, number_of_records))

    # Store records from sql database in a list.
    results = []
    for result in cursor.stored_results():
        results.extend(result.fetchall())

    # Display results in a table format using string formatting
    print(f"\nFilms from {year} (Top {number_of_records} by Profit):")
    columns = ['No', 'Film Name', 'Release Date', 'Total Cost', 'Total Earned', 'Profit']
    header = "| {:<5} | {:<30} | {:<15} | {:<15} | {:<15} | {:<15} |".format(*columns)
    print("-" * len(header))
    print(header)
    print("-" * len(header))

    for idx, row in enumerate(results, 1):
        truncated_row = list(row)

        # Truncate the film name if it's too long
        film_name = str(truncated_row[1])
        if len(film_name) > 30:
            film_name = film_name[:27] + "..."

        # Formatting the release date, getting only date.
        release_date = str(truncated_row[2])[:10] 

        # Formatting the numeric values for better readability
        total_cost = f"{truncated_row[3]:,.0f}"
        total_earned = f"{truncated_row[4]:,.0f}"
        profit = f"{truncated_row[5]:,.0f}"

        print("| {:<5} | {:<30} | {:<15} | {:<15} | {:<15} | {:<15} |".format(
            idx, film_name, release_date, total_cost, total_earned, profit
        ))

    print("-" * len(header))
    print("")

    # Close the connection
    cursor.close()
    conn.close()
