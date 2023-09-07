import numpy as np
import matplotlib.pyplot as plt
import sqlite3

# Leer los datos desde el archivo CSV (coordenadas del mapa)
with open('Alamillo95x216grid.csv', 'r') as file:
    csv_data = file.read().split(';')

# Inicializar listas para latitudes y longitudes desde el CSV
csv_latitudes = []
csv_longitudes = []

# Procesar los datos del CSV
for line in csv_data:
    if line.strip():  # Ignorar líneas vacías
        parts = line.split(';')
        for part in parts:
            coordinates = part.split(',')
            if len(coordinates) == 2:
                lat, lon = coordinates
                csv_latitudes.append(float(lat))
                csv_longitudes.append(float(lon))

# Conectar a la base de datos SQLite (reemplazar 'tu_basededatos.db' con el nombre de tu archivo de base de datos)
conn = sqlite3.connect('/home/azken/Database/sensor.db')
cursor = conn.cursor()

# Fecha y hora de inicio y fin (ajusta las fechas y horas como necesites)
fecha_inicio = '2023-09-06 16:29:29.000000'
fecha_fin = '2023-09-07 16:59:48.000000'

# Conectar a la base de datos SQLite (reemplazar 'tu_basededatos.db' con el nombre de tu archivo de base de datos)
conn = sqlite3.connect('/home/azken/Database/sensor.db')
cursor = conn.cursor()

# Consulta SQL para seleccionar los datos de la base de datos dentro del rango de fechas y horas
query = f"SELECT Latitude, Longitude, Data FROM ASV_variables WHERE Sensor='Sonar' AND Date BETWEEN '{fecha_inicio}' AND '{fecha_fin}'"
cursor.execute(query)

# Inicializar listas para latitudes, longitudes y valores del sensor desde la base de datos
db_latitudes = []
db_longitudes = []
db_sensor_values = []

# Procesar los datos desde la base de datos y agregarlos a las listas
for row in cursor.fetchall():
    lat, lon, value = row
    if lat != 0 and lon != 0:  # Filtrar valores con latitud y longitud no igual a 0
        db_latitudes.append(lat)
        db_longitudes.append(lon)
        db_sensor_values.append(value)

# Convertir las listas de la base de datos a arrays de numpy
db_latitudes = np.array(db_latitudes)
db_longitudes = np.array(db_longitudes)
db_sensor_values = np.array(db_sensor_values)

# Definir una cuadrícula regular de latitud y longitud basada en los datos del CSV
min_lat, max_lat = min(csv_latitudes), max(csv_latitudes)
min_lon, max_lon = min(csv_longitudes), max(csv_longitudes)
grid_latitude = np.linspace(min_lat, max_lat, 1000)
grid_longitude = np.linspace(min_lon, max_lon, 1000)
grid_latitude, grid_longitude = np.meshgrid(grid_latitude, grid_longitude)

import numpy as np
import matplotlib.pyplot as plt
import sqlite3

# ... (Previous code for reading data from the database) ...

# Filter data from the database where sensor values are between -50 and 50, and lat/lon are not zero
filtered_latitudes = db_latitudes[(db_sensor_values >= -50) & (db_sensor_values <= 50) & (db_latitudes != 0) & (db_longitudes != 0)]
filtered_longitudes = db_longitudes[(db_sensor_values >= -50) & (db_sensor_values <= 50) & (db_latitudes != 0) & (db_longitudes != 0)]
filtered_sensor_values = db_sensor_values[(db_sensor_values >= -50) & (db_sensor_values <= 50) & (db_latitudes != 0) & (db_longitudes != 0)]

# Define the number of bins for the heatmap (size of drawing)
num_bins = 100 #The higher the more cells it will draw,

# Calculate the mean sensor value for each grid cell
heatmap, xedges, yedges = np.histogram2d(filtered_longitudes, filtered_latitudes, bins=num_bins, weights=filtered_sensor_values)


# Create a figure and axis with a transparent background
fig, ax = plt.subplots(figsize=(12, 8))
ax.patch.set_alpha(0)  # Make the axis background transparent

# Plot the values of the sensor directly without a colormap
heatmap = ax.imshow(heatmap.T, cmap='coolwarm', extent=[xedges[0], xedges[-1], yedges[0], yedges[-1]], origin='lower', aspect='auto', alpha=1.0, vmin=-50, vmax=50)

# Add a colorbar
cbar = plt.colorbar(heatmap, ax=ax, label='Mean Sensor Value')

# Set plot title and axis labels
ax.set_title('Mean Sensor Values (Filtered for Values between -50 and 50)')
ax.set_xlabel('Longitude')
ax.set_ylabel('Latitude')


# Save the image to a file (adjust the name and format)
plt.savefig('heatmap.png', dpi=300, bbox_inches='tight')

# Cierra la conexión a la base de datos
conn.close()
