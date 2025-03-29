from neo4j import GraphDatabase
import os
from dotenv import load_dotenv

'''NO DESCOMENTEN
NADA POR FA QUE SE
PETATEA PORQUE YA
ESTÁ EN LA BASE!!!!!!'''

load_dotenv()
URI = os.getenv("NEO4J_URI") 
AUTH = (os.getenv("NEO4J_USER"), os.getenv("NEO4J_PASSWORD"))

driver = GraphDatabase.driver(URI, auth=AUTH)

def ejecutar_create(query = '', type = '', parametros={}):
    with driver.session() as session:
        if type == 'user':
            query = "MERGE (:USUARIO {idu: $idu, nombre: $nombre})"
        elif type == 'post':
            query = "MERGE (:POST {idp: $idp, contenido: $contenido})"
        elif type == 'comment':
            query = "MERGE (:COMENTARIO {consec: $consec, contenidoCom: $contenidoCom, fechorCom: $fechorCom, likeNotLike: $likeNotLike, fechorAut: $fechorAut})"

        session.execute_write(lambda tx: tx.run(query, **parametros))

def ejecutar_relacion(nodo1, clave1, valor1, relacion, nodo2, clave2, valor2):
    query = f"""
        MATCH (a:{nodo1} {{{clave1}: $valor1}}), (b:{nodo2} {{{clave2}: $valor2}})
        MERGE (a)-[:{relacion}]->(b)
    """
    with driver.session() as session:
        session.execute_write(lambda tx: tx.run(query, valor1=valor1, valor2=valor2))

# Restricciones (PKs)
constrains = [
    "CREATE CONSTRAINT unique_usuario FOR (u:USUARIO) REQUIRE u.idu IS UNIQUE;",
    "CREATE CONSTRAINT unique_post FOR (p:POST) REQUIRE p.idp IS UNIQUE;",
    "CREATE CONSTRAINT unique_comentario FOR (c:COMENTARIO) REQUIRE c.consec IS UNIQUE;"
]

#for constrain in constrains:
#    ejecutar_create(query = constrain)

# Nodos de prueba (CREATE ya está automatizado)
usuarios = [{"idu": 1, "nombre": "Juan"}, {"idu": 2, "nombre": "María"}]
posts = [{"idp": 101, "contenido": "Mi primer post"}, {"idp": 102, "contenido": "Hola a todos"}]
comentarios = [
    {"consec": 1, "contenidoCom": "Buen post", "fechorCom": "2024-03-29", "likeNotLike": True, "fechorAut": "2024-03-29"},
    {"consec": 2, "contenidoCom": "Interesante", "fechorCom": "2024-03-29", "likeNotLike": False, "fechorAut": "2024-03-29"}
]

'''
for usuario in usuarios:
    ejecutar_create(type = 'user', parametros= usuario)

for post in posts:
    ejecutar_create(type = 'post', parametros = post)

for comentario in comentarios:
    ejecutar_create(type = 'comment', parametros = comentario)
'''

# Relaciones de prueba (ya está automatizado tmb)
relaciones = [
    ("USUARIO", "idu", 1, "PUBLICA", "POST", "idp", 101),
    ("USUARIO", "idu", 2, "PUBLICA", "POST", "idp", 102),
    ("POST", "idp", 101, "TIENE", "COMENTARIO", "consec", 1),
    ("POST", "idp", 102, "TIENE", "COMENTARIO", "consec", 2),
    ("USUARIO", "idu", 2, "HACE", "COMENTARIO", "consec", 1),
    ("USUARIO", "idu", 1, "HACE", "COMENTARIO", "consec", 2),
    ("USUARIO", "idu", 1, "AUTORIZA", "COMENTARIO", "consec", 1),
    ("USUARIO", "idu", 2, "AUTORIZA", "COMENTARIO", "consec", 2)
]

for relacion in relaciones:
    ejecutar_relacion(*relacion)

driver.close()
