# import csv
# from datetime import datetime
# from django.core.exceptions import ObjectDoesNotExist
# from .models import Usuario, Ocupacion, Categoria, Pelicula, Puntuacion

# def cargar_datos():
#     borrar_datos()
#     cargar_ocupaciones()
#     cargar_categorias()
#     cargar_usuarios()
#     cargar_peliculas()
#     cargar_puntuaciones()

# def borrar_datos():
#     Puntuacion.objects.all().delete()
#     Pelicula.objects.all().delete()
#     Categoria.objects.all().delete()
#     Ocupacion.objects.all().delete()
#     Usuario.objects.all().delete()

# def cargar_ocupaciones():
#     with open('datasets/occupation', 'r', encoding='latin-1') as file:
#         ocupaciones_reader = csv.reader(file)
#         for row in ocupaciones_reader:
#             nombre_ocupacion = row[0]
#             Ocupacion.objects.create(nombre=nombre_ocupacion)

# def cargar_categorias():
#     with open('datasets/u.genre', 'r', encoding='latin-1') as file:
#         categorias_reader = csv.reader(file, delimiter='|')
#         for row in categorias_reader:
#             nombre_categoria, id_categoria = row
#             Categoria.objects.create(nombre=nombre_categoria, id_categoria=id_categoria)


# def cargar_usuarios():
#     with open('datasets/u.user', 'r', encoding='latin-1') as file:
#         usuarios_reader = csv.reader(file, delimiter='|')
#         for row in usuarios_reader:
#             id_usuario, edad, sexo, ocupacion_nombre, codigo_postal = row
#             ocupacion = Ocupacion.objects.get(nombre=ocupacion_nombre)
#             Usuario.objects.create(
#                 id_usuario=id_usuario,
#                 edad=edad,
#                 sexo=sexo,
#                 ocupacion=ocupacion,
#                 codigo_postal=codigo_postal
#             )

# def cargar_peliculas():
#     with open('datasets/u.item', 'r', encoding='latin-1') as file:
#         peliculas_reader = csv.reader(file, delimiter='|')
#         for row in peliculas_reader:
#             if len(row) < 5:
#                 # Ignorar filas que no tengan suficientes atributos
#                 continue

#             id_pelicula, titulo, fecha_estreno, _, imdb_url, *categorias_ids = row

#             if not id_pelicula or not titulo or not fecha_estreno:
#                 # Ignorar filas con atributos faltantes o vacíos
#                 continue

#             fecha_estreno = datetime.strptime(fecha_estreno, "%d-%b-%Y").date() if fecha_estreno else None
#             imdb_url = imdb_url if imdb_url else None

#             categorias = [Categoria.objects.get(id_categoria=int(id_categoria)) for id_categoria in categorias_ids if id_categoria]

#             pelicula = Pelicula.objects.create(
#                 id_pelicula=id_pelicula,
#                 titulo=titulo,
#                 fecha_estreno=fecha_estreno,
#                 imdb_url=imdb_url
#             )

#             pelicula.categorias.set(categorias)


# def cargar_puntuaciones():
#     with open('datasets/u.data', 'r') as file:
#         puntuaciones_reader = csv.reader(file, delimiter='\t')
#         for row in puntuaciones_reader:
#             print(row)
#             id_usuario, id_pelicula, puntuacion, timestamp = row
#             try:
#                 usuario = Usuario.objects.get(id_usuario=id_usuario)
#                 pelicula = Pelicula.objects.get(id_pelicula=id_pelicula)

#                 Puntuacion.objects.create(
#                     id_usuario=usuario,
#                     id_pelicula=pelicula,
#                     puntuacion=puntuacion
#                 )
#             except ObjectDoesNotExist:
#                 print(f"Error: No se puede encontrar Usuario con ID {id_usuario} o Película con ID {id_pelicula}")
