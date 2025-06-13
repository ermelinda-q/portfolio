# This file contains functions to use with Neo4j database.
# Check if actor exists in Neo4j
def check_actor_in_neo4j(tx, actor_id):
    query = "MATCH (a:Actor) WHERE a.ActorID = $actor_id RETURN COUNT(a) > 0 AS existsInNeo4j"
    result = tx.run(query, actor_id=actor_id)
    return 1 if result.single()["existsInNeo4j"] else 0


# Check if actor is already married in Neo4j
def is_actor_married(tx, actor_id):
    query = """
    MATCH (a:Actor {ActorID: $actor_id})-[:MARRIED_TO]-(:Actor)
    RETURN COUNT(*) > 0 AS isMarried
    """
    result = tx.run(query, actor_id=actor_id)
    record = result.single()
    return record["isMarried"] if record else False



# Create a marriage relationship between two actors in Neo4j
def create_marriage_in_neo4j(tx, actor1_id, actor2_id):
    query = """
    MATCH (a1:Actor {ActorID: $actor1_id})
    MATCH (a2:Actor {ActorID: $actor2_id})
    MERGE (a1)-[:MARRIED_TO]->(a2)
    """
    tx.run(query, actor1_id=actor1_id, actor2_id=actor2_id)


# Create Actor node in Neo4j (if needed)
def create_actor_in_neo4j(tx, actor_id):
    query = "CREATE (a:Actor {ActorID: $actor_id})"
    tx.run(query, actor_id=actor_id)
