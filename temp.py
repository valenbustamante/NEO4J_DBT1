import os
from neo4j import GraphDatabase

# Cargar credenciales desde variables de entorno
NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USER = os.getenv("NEO4J_USER")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")


driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

def check_connection():
    with driver.session() as session:
        result = session.run("RETURN 'Conexión exitosa' AS mensaje")
        for record in result:
            print(record["mensaje"])

check_connection()
