import folium
from folium.plugins import HeatMap
import sqlite3
import numpy as np
from selenium import webdriver
import pandas as pd 

# Leer datos del CSV (coordenadas del mapa)
with open('mapaloyola.csv', 'r') as file:
    csv_data = file.read().split(';')

csv_latitudes = []
csv_longitudes = []

for line in csv_data:
    if line.strip():
        parts = line.split(';')
        for part in parts:
            coordinates = part.split(',')
            if len(coordinates) == 2:
                lat, lon = coordinates
                csv_latitudes.append(float(lat))
                csv_longitudes.append(float(lon))

# Conectar a la base de datos SQLite
conn = sqlite3.connect('datos.db')
cursor = conn.cursor()

# Definir fecha de inicio y fin (ajusta según tus necesidades)
fecha_inicio = '2023-09-06 16:29:29.000000'
fecha_fin = '2023-09-07 16:59:48.000000'

# Consulta SQL para seleccionar datos de la base de datos dentro del rango de fecha y hora especificado
query = f"SELECT Latitude, Longitude, Data FROM ASV_variables WHERE Sensor='Sonar' AND Date BETWEEN '{fecha_inicio}' AND '{fecha_fin}'"
cursor.execute(query)

# Inicializar listas para latitud, longitud y valores del sensor desde la base de datos
db_latitudes = []
db_longitudes = []
db_sensor_values = []

for row in cursor.fetchall():
    lat, lon, value = row
    if lat != 0 and lon != 0:
        db_latitudes.append(lat)
        db_longitudes.append(lon)
        db_sensor_values.append(value)

# Convertir las listas de la base de datos a arrays NumPy para un procesamiento posterior
db_latitudes = np.array(db_latitudes)
db_longitudes = np.array(db_longitudes)
db_sensor_values = np.array(db_sensor_values)

# Filtrar datos de la base de datos donde los valores del sensor estén entre -50 y 50, y lat/lon no sean cero
filtered_latitudes = db_latitudes[(db_sensor_values >= -50) & (db_sensor_values <= 50) & (db_latitudes != 0) & (db_longitudes != 0)]
filtered_longitudes = db_longitudes[(db_sensor_values >= -50) & (db_sensor_values <= 50) & (db_latitudes != 0) & (db_longitudes != 0)]
filtered_sensor_values = db_sensor_values[(db_sensor_values >= -50) & (db_sensor_values <= 50) & (db_latitudes != 0) & (db_longitudes != 0)]

# Obtener los valores máximos de latitud y longitud del CSV
max_lat = max(csv_latitudes)
max_lon = max(csv_longitudes)

# Crear un mapa centrado en los valores máximos de latitud y longitud
m = folium.Map(location=[max_lat, max_lon], zoom_start=17)

# Crear una lista de tuplas que contienen latitud, longitud y valor del sensor
data = [(latitud, longitud, valor) for latitud, longitud, valor in zip(filtered_latitudes, filtered_longitudes, filtered_sensor_values)]

# Crear un mapa de calor con los datos de ubicación y valores del sensor
HeatMap(data, radius=15).add_to(m)

 # Puedes ajustar este valor según tus necesidades

# Guardar el mapa como un archivo HTML
m.save("mapa_de_calor.html")


# Crear un DataFrame de Pandas con los datos del mapa de calor
df = pd.DataFrame(data, columns=['Latitud', 'Longitud', 'Valor del Sensor'])

# Guardar el DataFrame en un archivo CSV
df.to_csv("datos_mapa_de_calor.csv", index=False)

# Cerrar la conexión de la base de datos
conn.close()

# Configurar Selenium para capturar una imagen del mapa
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # Ejecutar Chrome en modo sin cabeza (sin ventana visible)
options.add_argument('--window-size=1920,1080') 
driver = webdriver.Chrome(options=options)
driver.get("file:////home/aceti/test_comu/mapa_de_calor.html")  # Reemplaza <ruta_a_tu_directorio> con la ubicación de tu archivo HTML

# Capturar una imagen de la página y guardarla como PNG
driver.save_screenshot("mapa_de_calor.png")

# Cerrar el navegador Selenium
driver.quit()
