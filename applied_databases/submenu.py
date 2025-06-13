# This file contains the extra menu(6) and the submenu added to the project.
# All reports are saved as a text file into the reports folder created by the program if doesn't exist.
# If an error occurs the error message is saved into the files.
import os
from db_connections import connection_sql, connection_neo4j

def generate_reports_menu():
    while True:
        print("\n--- Generate Reports Menu ---")
        print("1 - Database Information")
        print("2 - Actors Table Report")
        print("3 - List of Married Actors")
        print("4 - Studio Statistics")
        print("5 - Top Films by Shared Actors")
        print("b - Back to Main Menu")
        choice = input("Choice: ")

        if choice == "1":
            report_database_info()
        elif choice == "2":
            report_actors_info()
        elif choice == "3":
            report_married_actors()
        elif choice == "4":
            report_studios_info()
        elif choice == "5":
            report_top_films_by_shared_actors()
        elif choice.lower() == "b":
            break
        else:
            print("Invalid option.")

# Creating the 'reports' folder if it doesn't exist
def ensure_reports_folder():
    if not os.path.exists("reports"):
        os.makedirs("reports")


############### SubMenu 1 - Database information ################

def report_database_info():
    ensure_reports_folder()
    conn = connection_sql()
    cursor = conn.cursor()

    with open("reports/database_info.txt", "w", encoding="utf-8") as f:      # file: database_info.txt
        f.write("--- SQL Database Info ---\n")
        cursor.execute("SELECT DATABASE()") # using the current working database
        db_name = cursor.fetchone()[0]
        f.write(f"Database Name: {db_name}\n")  # db_name returns the name of the database
        f.write("-" * 20)

        # Show tables and loop through them to get for each of them: total records, and describe command output.
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        for (table,) in tables:
            f.write(f"\nTable: {table}\n")
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = cursor.fetchone()[0]
            f.write(f" - Records: {count}\n")
            cursor.execute(f"DESCRIBE {table}")
            structure = cursor.fetchall()
            for col in structure:
                col_name, col_type, _, key, default, extra = col
                key_label = "[PK]" if key == "PRI" else "[FK]" if key == "MUL" else ""
                f.write(f"   > {col_name} ({col_type}) {key_label}\n")

        try:
            driver = connection_neo4j()     # connects to neo4j and get the labels and nodes(counts)
            with driver.session(database="actorsMarried") as session:
                f.write("\n--- Neo4j Database Info ---\n")
                node_labels = session.run("CALL db.labels()")
                for label in node_labels:
                    label_name = label["label"]
                    count = session.run(f"MATCH (n:{label_name}) RETURN count(n) AS c").single()["c"]
                    f.write(f"Node Label: {label_name} - {count} node(s)\n")
        except Exception as e:
            f.write(f"\nNeo4j Error: {e}\n")

############### SubMenu 2 - Actors Table ################

def report_actors_info():
    ensure_reports_folder()
    conn = connection_sql()
    cursor = conn.cursor()

    with open("reports/actors_info.txt", "w", encoding="utf-8") as f:   # filename: actors_info.txt
        f.write("--- Actors Report ---\n")
        cursor.execute("SELECT COUNT(*) FROM actor")        # get total number of records in actor's table
        total = cursor.fetchone()[0]
        f.write(f"Total actors: {total}\n")

        cursor.execute("SELECT ActorGender, COUNT(*) FROM actor GROUP BY ActorGender")  # query returns number of male and female actors
        for gender, count in cursor.fetchall():
            f.write(f"{gender}: {count}\n")

        f.write("\nTop 10 Male Actors by Film Count:\n")
        # This query returns the male actors with most films.
        cursor.execute("""   
            SELECT a.ActorName, COUNT(fc.CastFilmID) AS film_count 
            FROM actor a 
            JOIN filmcast fc ON a.ActorID = fc.CastActorID 
            WHERE a.ActorGender = 'Male'
            GROUP BY a.ActorID 
            ORDER BY film_count DESC 
            LIMIT 10
        """)
        for name, count in cursor.fetchall():
            f.write(f"{name}: {count} films\n")

        f.write("\nTop 10 Female Actors by Film Count:\n")
        # This query returns the female actors with most films.
        cursor.execute("""
            SELECT a.ActorName, COUNT(fc.CastFilmID) AS film_count 
            FROM actor a 
            JOIN filmcast fc ON a.ActorID = fc.CastActorID 
            WHERE a.ActorGender = 'Female'
            GROUP BY a.ActorID 
            ORDER BY film_count DESC 
            LIMIT 10
        """)
        for name, count in cursor.fetchall():
            f.write(f"{name}: {count} films\n")

        f.write("\nTop 10 Countries by Actor Count:\n")
        # query returns countries that most of actors are from(top 10)
        cursor.execute("""
            SELECT c.CountryName, COUNT(*) 
            FROM actor a
            JOIN country c ON a.ActorCountryID = c.CountryID
            GROUP BY c.CountryID 
            ORDER BY COUNT(*) DESC 
            LIMIT 10
        """)
        for country, count in cursor.fetchall():
            f.write(f"{country}: {count}\n")

############## SubMenu 3 - List of Married Actors ###############

def report_married_actors():
    ensure_reports_folder()
    driver = connection_neo4j()
    conn = connection_sql()
    cursor = conn.cursor()

    with open("reports/married_actors.txt", "w", encoding="utf-8") as f:    # filename: married_actors.txt
        f.write("--- Married Actors ---\n")
        try:
            with driver.session(database="actorsMarried") as session:
                # the query returns the ids of married actors in neo4j(actorsMarried file)
                query = """
                    MATCH (a1:Actor)-[:MARRIED_TO]-(a2:Actor)
                    WHERE a1.ActorID < a2.ActorID
                    RETURN a1.ActorID AS id1, a2.ActorID AS id2
                """
                # searching the appdbproj.sql to get actor names from their id returned from above 
                results = session.run(query)
                for record in results:
                    id1 = record["id1"]
                    id2 = record["id2"]
                    cursor.execute("SELECT ActorName FROM actor WHERE ActorID = %s", (id1,))
                    name1 = cursor.fetchone()
                    cursor.execute("SELECT ActorName FROM actor WHERE ActorID = %s", (id2,))
                    name2 = cursor.fetchone()
                    if name1 and name2:
                        f.write(f"{name1[0]} is married to {name2[0]}\n")
        except Exception as e:
            f.write(f"Error: {e}\n")

############## SubMenu 4 - Studio Statistics ###############

def report_studios_info():
    ensure_reports_folder()
    conn = connection_sql()
    cursor = conn.cursor()

    with open("reports/studios_info.txt", "w", encoding="utf-8") as f:      # filename: studios_info.txt
        f.write("--- Studio Report ---\n")

        f.write("\nTop Studios by Number of Films:\n")
        # Query returns number of films by studio, orders by number of films(desc), returns top 10(most films)
        cursor.execute("""
            SELECT s.studioName, COUNT(f.FilmID) AS film_count
            FROM studio s
            JOIN film f ON s.studioID = f.FilmStudioID
            GROUP BY s.studioID
            ORDER BY film_count DESC
            LIMIT 10
        """)
        for name, count in cursor.fetchall():
            f.write(f"{name}: {count} films\n")

        f.write("\nStudios with Fewest Films:\n")
        # Query returns number of films by studio, orders by number of films(asc), returns top 10(less films)
        cursor.execute("""
            SELECT s.studioName, COUNT(f.FilmID) AS film_count
            FROM studio s
            LEFT JOIN film f ON s.studioID = f.FilmStudioID
            GROUP BY s.studioID
            ORDER BY film_count ASC
            LIMIT 10
        """)
        for name, count in cursor.fetchall():
            f.write(f"{name}: {count} films\n")

############## SubMenu 5 - Top Films By Shared Actors ###############
def report_top_films_by_shared_actors():
    ensure_reports_folder()
    conn = connection_sql()
    cursor = conn.cursor()

    with open("reports/films_shared_actors.txt", "w", encoding="utf-8") as f:        # filename: films_shared_actors.txt
        f.write("--- Top Films by Shared Actors ---\n")

        # Query for top 20 films with most shared actors
        cursor.execute("""
            SELECT 
                f1.FilmID, f1.FilmName, 
                f2.FilmID, f2.FilmName, 
                COUNT(*) AS shared_actors
            FROM filmcast fc1
            JOIN filmcast fc2 ON fc1.CastActorID = fc2.CastActorID AND fc1.CastFilmID < fc2.CastFilmID
            JOIN film f1 ON fc1.CastFilmID = f1.FilmID
            JOIN film f2 ON fc2.CastFilmID = f2.FilmID
            GROUP BY f1.FilmID, f2.FilmID
            ORDER BY shared_actors DESC
            LIMIT 20
        """)
        top_pairs = cursor.fetchall()

        for film1_id, film1_name, film2_id, film2_name, shared in top_pairs:
            f.write(f"\n{film1_name} & {film2_name} - {shared} shared actors\n")

            # Query shared actor names for each film 
            cursor.execute("""
                SELECT DISTINCT a.ActorName
                FROM filmcast fc1
                JOIN filmcast fc2 ON fc1.CastActorID = fc2.CastActorID
                JOIN actor a ON fc1.CastActorID = a.ActorID
                WHERE fc1.CastFilmID = %s AND fc2.CastFilmID = %s
            """, (film1_id, film2_id))
            actors = cursor.fetchall()

            for (actor_name,) in actors:
                f.write(f"   - {actor_name}\n")
