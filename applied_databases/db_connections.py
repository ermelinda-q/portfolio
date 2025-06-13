# This file contains the two functions to make connection with databases used in this project(MySQL & Neo4j)
from neo4j import GraphDatabase
import mysql.connector

def connection_sql():
    try:
        sql_conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="PabloTralee2003!",
            database="appdbproj"
        )
        return sql_conn
    except mysql.connector.Error as e:
        print(f"Connection error: {e}")
        return None



def connection_neo4j():

    uri = "neo4j://localhost:7687"
    driver = GraphDatabase.driver(uri, auth=("", ""), max_connection_lifetime=1000)
    return driver
    