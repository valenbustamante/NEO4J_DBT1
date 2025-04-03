import streamlit as st
from funciones import crear_nodo, actualizar_nodo,  eliminar_nodo, crear_relacion, visualize_database, get_list_of, consulta_1_taller, consulta_2_taller
from PIL import Image
import os
from datetime import datetime

# constrains = [
#     "CREATE CONSTRAINT unique_usuario FOR (u:USUARIO) REQUIRE u.idu IS UNIQUE;",
#     "CREATE CONSTRAINT unique_post FOR (p:POST) REQUIRE p.idp IS UNIQUE;",
#     "CREATE CONSTRAINT unique_comentario FOR (c:COMENTARIO) REQUIRE c.consec IS UNIQUE;"
# ]


# for constrain in constrains:
#     crear_nodo(query = constrain)


base_path = os.path.dirname(os.path.abspath(__file__))
logo_path = os.path.join(base_path, "logo.png")

st.sidebar.image(logo_path, caption="----------", use_container_width=True)

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
    elif opcion == "COMENTARIO":
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
            if st.button("Crear Usuario"):
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
            idu = st.number_input("ID Usuario", min_value=1, step=1)
            idp = st.number_input("ID Post", min_value=100, step=1)
            contenido = st.text_area("Contenido del Post")
            if st.button("Crear Post"):
                crear_nodo(type='post', parametros={"idp": idp, "contenido": contenido})
                crear_relacion("USUARIO", "idu", idu, "PUBLICA", "POST", "idp", idp)

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
            idu = st.number_input("ID Usuario", min_value=1, step=1)
            idp = st.number_input("ID Post", min_value=100, step=1)
            consec = st.number_input("ID Comentario", min_value=1, step=1)
            contenidoCom = st.text_area("Contenido del Comentario")
            likeNotLike = st.checkbox("¿Le gusta?")
            fecha = datetime.today().strftime('%Y-%m-%d')
            if st.button("Crear Comentario"):
                crear_nodo(type='comment', parametros={"consec": consec, "contenidoCom": contenidoCom, "likeNotLike": likeNotLike, "fechorCom": fecha, "fechorAut": ''})
                crear_relacion("POST", "idp", idp, "TIENE", "COMENTARIO", "consec", consec)
                crear_relacion("USUARIO", "idu", idu, "HACE", "COMENTARIO", "consec", consec)
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
    consulta = st.selectbox("Consultas:", ["Consulta 1", "Consulta 2", "Autorización de comentarios"])
    if consulta == "Consulta 1":
        st.subheader("Consulta 1")
        st.write("Elija un usuario")
        dx = {'id':[], 'nombre':[]} 
        list_of = get_list_of("USUARIO")
        for usuario in list_of:
                    dx['id'].append(usuario["idu"])
                    dx['nombre'].append(usuario["nombre"])
        idu = st.selectbox("idu:",list(dx['id']))
        result = consulta_1_taller(idu)
        st.write(result)
    
    if consulta == "Consulta 2":
        st.subheader("Consulta 2")
        usuarios = get_list_of("USUARIO")
        user_dict = {usuario["idu"]: usuario["nombre"] for usuario in usuarios}
        idu = st.selectbox("Elija un usuario:", list(user_dict.keys()), format_func=lambda x: user_dict[x])
        if idu:
            posts = consulta_1_taller(idu)
            print(posts)
            post_dict = {post["idp"]: post["contenido"] for post in posts}
            if posts:
                idp = st.selectbox("Elija un post:", list(post_dict.keys()), format_func=lambda x: post_dict[x])
                if idp:
                    comentarios = consulta_2_taller(idp)
                    if comentarios:
                        st.subheader("Comentarios")
                        for comentario in comentarios:
                            with st.container():
                                st.markdown(f"**{comentario.get('comentado_por', 'Anónimo')}** dice:")
                                st.markdown(f"""    *{comentario.get('comentario', 'Sin contenido')}*""")
                                footerc = f"📅 {comentario.get('fecha_creacion_comentario', 'Fecha desconocida')}" + "      "
                                if comentario.get('megusta', False) is False:
                                    footerc= footerc + "👎 No le gusta"
                                else:
                                    footerc= footerc +  f"👍 Le gusta"
                                st.markdown(footerc)
                                if comentario.get('fecha_autorizacion', None) == '':
                                    st.markdown("📅❌ No autorizado")
                                else:
                                    st.markdown(f"📅☑️ {comentario.get('fecha_autorizacion', 'No autorizado')}")
                                st.markdown("---")
                    else:
                        st.info("No hay comentarios para este post.")
            else:
                st.warning("Este usuario no tiene posts.")


    if consulta == 'Autorización de comentarios':
        st.subheader("Autorización de comentarios")
        consec = st.number_input("ID Comentario a autorizar", min_value=1, step=1)
        idu = st.number_input("ID Usuario que autoriza", min_value=1, step=1)
        fecha = datetime.today().strftime('%Y-%m-%d')
        if st.button("Autorizar Comentario"):
            crear_relacion("USUARIO", "idu", idu, "AUTORIZA", "COMENTARIO", "consec", consec)
            actualizar_nodo("COMENTARIO", "consec", consec, {"fechorAut": fecha})



