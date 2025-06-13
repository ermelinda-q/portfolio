# Importing the libraries and functions needed for the project.
from db_connections import connection_sql, connection_neo4j
from view_add_sql import *

############################################################
##########   Menu Choice 4 - Find Actor Spouse   ###########
############################################################

# This function checks the neo4j actorsMarried database.
# If the actor_id is present and is married.Returns both actor's IDs.
def get_partners_ids(tx, actor_id):
    neo4j_query = """
    MATCH (a:Actor {ActorID: $actor_id})-[:MARRIED_TO]-(b:Actor)
    RETURN a.ActorID AS actor1_id, b.ActorID AS actor2_id
    """
    result = tx.run(neo4j_query, actor_id=actor_id)
    return result.single()

# Function to get names from sql database using results from previous function.
def get_actor_names(sql_cursor, actor_ids):
    sql_query = """
    SELECT ActorID, ActorName FROM actor WHERE ActorID IN (%s, %s)
    """
    sql_cursor.execute(sql_query, actor_ids)
    return sql_cursor.fetchall()

# Main function to find the actor and partner if existent. 
def find_actor_partner():
    # Initializing neo4j and SQL connections
    driver = connection_neo4j()
    sql_conn = connection_sql()
    sql_cursor = sql_conn.cursor()

    try:
        print("")
        actor_id_input = int(input("Enter ActorID : ").strip())

        # checking neo4j function to return id/s.
        with driver.session() as neo4j_session:
            record = neo4j_session.execute_read(get_partners_ids, actor_id_input)
        # if no record or one of actors not in neo4j stop, return message.
        if not record or not record["actor1_id"] or not record["actor2_id"]:
            print("\n-----------")
            print("This actor is not married\n")
            return

        actor1_id = record["actor1_id"]
        actor2_id = record["actor2_id"]

        # Return actor names from SQL database.
        results = get_actor_names(sql_cursor, (actor1_id, actor2_id))

        # Organize names by ActorID
        names = {row[0]: row[1] for row in results}
        actors = [(actor1_id, names[actor1_id]), (actor2_id, names[actor2_id])]
        actors_sorted = sorted(actors, key=lambda x: x[0])

        # Display results
        print("\n-----------")
        print("These Actors are married:")
        for actor_id, name in actors_sorted:
            print(actor_id, "|", name)
        print("")

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        sql_cursor.close()
        sql_conn.close()

