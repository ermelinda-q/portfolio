# libraries and functions needed.
from db_connections import connection_sql
from mysql.connector.errors import Error

# This function can be called to run two query types:
# 1. Get directors and films
# 2. Get Actors by month
# In both cases the return values are as a list.
def query_sql_data(query_type, param):
    conn = connection_sql()
    try:
        with conn.cursor(dictionary=True) as cursor:
            if query_type == "directors_films":
                query = """
                    SELECT d.directorname, f.filmname, s.studioname
                    FROM film f
                    JOIN director d ON f.filmdirectorid = d.directorid
                    JOIN studio s ON f.filmstudioid = s.studioid
                    WHERE LOWER(d.directorname) LIKE %s;
                """
                search_pattern = "%" + param.lower() + "%"
                cursor.execute(query, (search_pattern,))
                return cursor.fetchall()

            elif query_type == "actors_by_month":
                query = """
                    SELECT actorName, actorDOB, actorGender
                    FROM actor
                    WHERE MONTH(actorDOB) = %s
                """
                cursor.execute(query, (param,))
                return cursor.fetchall()

            return []  # Unknown query_type — safely return empty list

    except Exception as e:
        return handle_db_error(e)
    finally:
        conn.close()

# BOOLEAN VALUE RETURN FUNCTION
# 1. Checks if an actor exists.
# 2. Checks if a country exists.

def exists_in_table(table_name, column_name, value):
    conn = connection_sql()
    try:
        with conn.cursor() as cursor:
            query = f"SELECT 1 FROM {table_name} WHERE {column_name} = %s"
            cursor.execute(query, (value,))
            return cursor.fetchone() is not None
    except Exception as e:
        return handle_db_error(e)
    finally:
        conn.close()

# Function to Insert a new actor in the database
# passing actor's id, name, dob, gender and country id as parameters.
# This function is called by add_actor function.
def insert_actor(actor_id, name, dob, gender, country_id):
    conn = connection_sql()
    try:
        with conn.cursor() as cursor:
            query = """
                INSERT INTO actor (ActorId, ActorName, ActorDOB, ActorGender, ActorCountryID)
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(query, (actor_id, name, dob, gender, country_id))
            conn.commit()
            return "\nActor successfully added\n"
    except Error as e:
        return handle_db_error(e)
    finally:
        conn.close()


# This function is used to get and format error messages from exceptions raised during database operations.
# It accepts 'e'(exception returned from functions) as an argument.
# Returns the exception as a message as required by the project.
def handle_db_error(e):
    if hasattr(e, 'args') and len(e.args) >= 2:
        error_code = e.args[0]
        full_message = e.args[1]

        if full_message.startswith(str(error_code)):
            parts = full_message.split(': ', 1)
            if len(parts) == 2:
                full_message = parts[1]

        return f'*** ERROR *** ({error_code}, "{full_message}")\n'
    else:
        return f'*** ERROR *** ("{str(e)}")'
