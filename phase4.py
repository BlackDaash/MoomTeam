import os
import csv
from PIL import Image

directorio_imagenes = "C:/Users/Guill/Desktop/Proyects/Astro pi 22-23/Solo_imagenes_ap"  # Ruta del directorio de imágenes
ruta_salida = "resultados.txt"  # Ruta del archivo de salida
ruta_datos = "C:/Users/Guill/Desktop/Proyects/Astro pi 22-23/data.csv"  # Ruta del archivo CSV de datos

def es_noche(imagen):
    umbral_brillo = 50  # Ajusta este valor según tu criterio

    imagen_gris = imagen.convert("L")
    histograma = imagen_gris.histogram()

    # Calcula el brillo promedio de la imagen
    total_pixeles = sum(histograma)
    brillo_promedio = sum(i * valor for i, valor in enumerate(histograma)) / total_pixeles

    return brillo_promedio < umbral_brillo

def analizar_imagen(imagen_path, datos, numero_imagen):
    # Convertir la imagen a escala de grises
    imagen = Image.open(imagen_path)
    imagen_gris = imagen.convert("L")

    # Realizar segmentación y extracción de características
    # Aquí debes implementar tus propios algoritmos y técnicas de segmentación y extracción de características

    # Ejemplo de clasificación de regiones en base a un umbral de color
    umbral = 100
    regiones_vegetacion = imagen_gris.point(lambda x: x > umbral and 255)

    # Ejemplo de cálculo de promedio de valores de píxeles
    promedio_vegetacion = sum(regiones_vegetacion.getdata()) / len(regiones_vegetacion.getdata())

    # Obtener los datos correspondientes a la imagen actual
    counter = datos["Counter"]
    fecha_hora = datos["Date/time"]
    latitud = datos["Latitude"]
    longitud = datos["Longitude"]
    temperatura = datos["Temperature"]
    humedad = datos["Humidity"]

    # Determinar si es noche o día
    estado_tiempo = "noche" if es_noche(imagen_gris) else "día"

    # Guardar resultados en el archivo de salida
    with open(ruta_salida, "a") as archivo_salida:
        archivo_salida.write(f"Imagen {numero_imagen} ({counter}):\n")
        archivo_salida.write(f"Fecha/hora: {fecha_hora}\n")
        archivo_salida.write(f"Latitud: {latitud}\n")
        archivo_salida.write(f"Longitud: {longitud}\n")
        archivo_salida.write(f"Temperatura: {temperatura}\n")
        archivo_salida.write(f"Humedad: {humedad}\n")
        archivo_salida.write(f"Promedio de vegetación: {promedio_vegetacion}\n")
        archivo_salida.write(f"Estado del tiempo: {estado_tiempo}\n")
        archivo_salida.write("------------------------\n")

    # Retornar los resultados del análisis
    return promedio_vegetacion

# Obtener la lista de imágenes en el directorio
lista_imagenes = os.listdir(directorio_imagenes)

# Leer los datos del archivo CSV
datos_csv = []
with open(ruta_datos, "r") as archivo_csv:
    lector_csv = csv.DictReader(archivo_csv)
    for fila in lector_csv:
        datos_csv.append(fila)

# Procesar cada imagen en la lista
for i, nombre_imagen in enumerate(lista_imagenes):
    ruta_imagen = os.path.join(directorio_imagenes, nombre_imagen)

    # Obtener los datos correspondientes a la imagen actual
    datos_imagen = datos_csv[i]

    # Realizar análisis de la imagen
    resultado_analisis = analizar_imagen(ruta_imagen, datos_imagen, i+1)

    print(f"Imagen {i+1} analizada. Resultado: {resultado_analisis}")
