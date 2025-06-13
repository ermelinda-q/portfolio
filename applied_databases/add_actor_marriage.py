from db_connections import connection_neo4j
from functions_neo4j import *
from functions_sql import exists_in_table

############################################################
##########   Menu Choice 5 - Add Actor Marriage  ###########
############################################################

# Main function to add actor marriage
def add_actor_marriage():
    neo4j_driver = connection_neo4j()

    while True:
    
        actor1_input = input("\nEnter Actor 1 ID: ")
        actor2_input = input("Enter Actor 2 ID: ")
            
        try:
            actor1_id = int(actor1_input)
            actor2_id = int(actor2_input)
        except ValueError:
            continue

        if actor1_id == actor2_id:
            print("An actor cannot marry themselves\n")
            continue

        # Check if both actors exist in SQL
        if not exists_in_table("actor","ActorID", actor1_id):
            print(f"Actor {actor1_id} does not exist")
            continue
        if not exists_in_table("actor","ActorID", actor2_id):
            print(f"Actor {actor2_id} does not exist")
            continue

        with neo4j_driver.session() as session:
            # Check if either actor is already married in Neo4j
            actor1_married = session.execute_read(is_actor_married, actor1_id)
            actor2_married = session.execute_read(is_actor_married, actor2_id)

            if actor1_married or actor2_married:
                if actor1_married:
                    print(f"Actor {actor1_id} is already married")
                if actor2_married:
                    print(f"Actor {actor2_id} is already married")
                print("")
                break

            # Ensure actors exist in Neo4j
            actor1_exists = session.execute_read(check_actor_in_neo4j, actor1_id)
            actor2_exists = session.execute_read(check_actor_in_neo4j, actor2_id)

            if not actor1_exists:
                session.execute_write(create_actor_in_neo4j, actor1_id)
            if not actor2_exists:
                session.execute_write(create_actor_in_neo4j, actor2_id)

            # Create the marriage relationship
            session.execute_write(create_marriage_in_neo4j, actor1_id, actor2_id)
        print(f"Actor {actor1_id} is now married to Actor {actor2_id}.\n")
        break

    neo4j_driver.close()

