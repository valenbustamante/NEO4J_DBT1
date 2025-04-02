import streamlit as st
from my_modules import crear_nodo, actualizar_nodo,  eliminar_nodo, actualizar_relacion, eliminar_relacion, crear_relacion, visualize_database, get_list_of, consulta_1_taller
from PIL import Image

# constrains = [
#     "CREATE CONSTRAINT unique_usuario FOR (u:USUARIO) REQUIRE u.idu IS UNIQUE;",
#     "CREATE CONSTRAINT unique_post FOR (p:POST) REQUIRE p.idp IS UNIQUE;",
#     "CREATE CONSTRAINT unique_comentario FOR (c:COMENTARIO) REQUIRE c.consec IS UNIQUE;"
# ]


# for constrain in constrains:
#     crear_nodo(query = constrain)

# # Nodos de prueba (CREATE ya está automatizado)
# usuarios = [{"idu": 1, "nombre": "Juan"}, {"idu": 2, "nombre": "María"}]
# posts = [{"idp": 101, "contenido": "Mi primer post"}, {"idp": 102, "contenido": "Hola a todos"}]
# comentarios = [
#     {"consec": 1, "contenidoCom": "Buen post", "fechorCom": "2024-03-29", "likeNotLike": True, "fechorAut": "2024-03-29"},
#     {"consec": 2, "contenidoCom": "Interesante", "fechorCom": "2024-03-29", "likeNotLike": False, "fechorAut": "2024-03-29"}
# ]

# for usuario in usuarios:
#     crear_nodo(type = 'user', parametros= usuario)

# for post in posts:
#     crear_nodo(type = 'post', parametros = post)

# for comentario in comentarios:
#     crear_nodo(type = 'comment', parametros = comentario)

# relaciones = [
#     ("USUARIO", "idu", 1, "PUBLICA", "POST", "idp", 101),
#     ("USUARIO", "idu", 2, "PUBLICA", "POST", "idp", 102),
#     ("POST", "idp", 101, "TIENE", "COMENTARIO", "consec", 1),
#     ("POST", "idp", 102, "TIENE", "COMENTARIO", "consec", 2),
#     ("USUARIO", "idu", 2, "HACE", "COMENTARIO", "consec", 1),
#     ("USUARIO", "idu", 1, "HACE", "COMENTARIO", "consec", 2),
#     ("USUARIO", "idu", 1, "AUTORIZA", "COMENTARIO", "consec", 1),
#     ("USUARIO", "idu", 2, "AUTORIZA", "COMENTARIO", "consec", 2)
# ]

# for relacion in relaciones:
#    crear_relacion(*relacion)

# actualizar_nodo("USUARIO", "idu", 1, {"nombre": "Juan Pérez"})
# eliminar_nodo("POST", "idp", 102)

# actualizar_relacion("USUARIO", "idu", 1, "PUBLICA", "POST", "idp", 101, {"fecha": "2024-03-29"})
# eliminar_relacion("USUARIO", "idu", 1, "PUBLICA", "POST", "idp", 101)


st.sidebar.image("logo.png", caption="----------", use_container_width=True)

opcion = st.sidebar.radio("", ["Manejo de datos", "Visualización", "Consultas"])

if opcion == "Manejo de datos":
    st.title("Menú")
    opcion = st.selectbox("Elige una categoría:", ["USUARIO", "POST", "COMENTARIO"])
    st.write(f"{opcion}S existentes")
    if opcion == "USUARIO":
        dx = {'id':[], 'nombre':[]} 
        list_of = get_list_of(opcion)
        for usuario in list_of:
            dx['id'].append(usuario["idu"])
            dx['nombre'].append(usuario["nombre"])
        st.dataframe(dx)
    elif opcion == "POST":
        list_of = get_list_of(opcion)
        dx = {'idp':[], 'contenido':[]} 
        for post in list_of:
            dx['idp'].append(post["idp"])
            dx['contenido'].append(post["contenido"])
        st.dataframe(dx)
    else :
        list_of = get_list_of(opcion)
        dx = {"consec":[], "likeNotLike":[], "fechorAut":[], "fechorCom":[],"contenidoCom":[]}
        for comentario in list_of:
            dx["consec"].append(comentario["consec"])
            dx["likeNotLike"].append("FALSE" if comentario["likeNotLike"] == False else "TRUE")

            dx["fechorAut"].append(comentario["fechorAut"])
            dx["fechorCom"].append(comentario["fechorCom"])
            dx["contenidoCom"].append(comentario["contenidoCom"])
        st.dataframe(dx)



    st.title("Gestión")
    if opcion == "USUARIO":
        accion = st.selectbox("Acción:", ["Crear", "Actualizar", "Eliminar"])
        if accion == "Crear":
            idu = st.number_input("ID Usuario", min_value=1, step=1)
            nombre = st.text_input("Nombre del Usuario")
            if st.button("Crea  r Usuario"):
                crear_nodo(type='user', parametros={"idu": idu, "nombre": nombre})

        elif accion == "Actualizar":
            idu = st.number_input("ID Usuario a actualizar", min_value=1, step=1)
            nuevo_nombre = st.text_input("Nuevo Nombre")
            if st.button("Actualizar Usuario"):
                actualizar_nodo("USUARIO", "idu", idu, {"nombre": nuevo_nombre})

        elif accion == "Eliminar":

            idu = st.number_input("ID Usuario a eliminar", min_value=1, step=1)
            if st.button("Eliminar Usuario"):
                eliminar_nodo("USUARIO", "idu", idu)

    elif opcion == "POST":
        
        
        accion = st.selectbox("Acción:", ["Crear", "Actualizar", "Eliminar"])

        if accion == "Crear":
            idp = st.number_input("ID Post", min_value=100, step=1)
            contenido = st.text_area("Contenido del Post")
            if st.button("Crear Post"):
                crear_nodo(type='post', parametros={"idp": idp, "contenido": contenido})

        elif accion == "Actualizar":
            idp = st.number_input("ID Post a actualizar", min_value=100, step=1)
            nuevo_contenido = st.text_area("Nuevo Contenido")
            if st.button("Actualizar Post"):
                actualizar_nodo("POST", "idp", idp, {"contenido": nuevo_contenido})

        elif accion == "Eliminar":
            
            idp = st.number_input("ID Post a eliminar", min_value=100, step=1)
            if st.button("Eliminar Post"):
                eliminar_nodo("POST", "idp", idp)

    elif opcion == "COMENTARIO":
        
        accion = st.selectbox("Acción:", ["Crear", "Actualizar", "Eliminar"])

        if accion == "Crear":
            consec = st.number_input("ID Comentario", min_value=1, step=1)
            contenidoCom = st.text_area("Contenido del Comentario")
            likeNotLike = st.checkbox("¿Le gusta?")
            if st.button("Crear Comentario"):
                crear_nodo(type='comment', parametros={"consec": consec, "contenidoCom": contenidoCom, "likeNotLike": likeNotLike})

        elif accion == "Actualizar":
            consec = st.number_input("ID Comentario a actualizar", min_value=1, step=1)
            nuevo_contenidoCom = st.text_area("Nuevo Contenido")
            if st.button("Actualizar Comentario"):
                actualizar_nodo("COMENTARIO", "consec", consec, {"contenidoCom": nuevo_contenidoCom})

        elif accion == "Eliminar":
            consec = st.number_input("ID Comentario a eliminar", min_value=1, step=1)
            if st.button("Eliminar Comentario"):
                eliminar_nodo("COMENTARIO", "consec", consec)
elif opcion == "Visualización":
    visualize_database()
    imagen = Image.open("neo4j_database_visualization.png")
    imagen_resized = imagen.resize((4000, 3000))  
    st.image(imagen_resized, caption="")
elif opcion == "Consultas":
    st.title("Consultas")
    consulta = st.selectbox("Consultas:", ["Consulta 1", "Consulta 2"])
    if consulta == "Consulta 1":
        st.subheader("Consulta 1")
        st.write("Elija un Usario")
        dx = {'id':[], 'nombre':[]} 
        list_of = get_list_of("USUARIO")
        for usuario in list_of:
                    dx['id'].append(usuario["idu"])
                    dx['nombre'].append(usuario["nombre"])
        idu = st.selectbox("idu:",list(dx['id']))
        result = consulta_1_taller(idu)
        st.write(result)



