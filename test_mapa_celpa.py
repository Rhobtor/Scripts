import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import numpy as np

# Ruta de tu archivo CSV
ruta_archivo = 'Alamillo95x216grid.csv'

# Leer el archivo CSV y procesar los datos
with open(ruta_archivo, 'r') as file:
    csv_data = file.read().split(';')   # Leer el archivo CSV y dividirlo en una lista utilizando ';' como delimitador.

# Inicializar listas para latitud y longitud desde el CSV
csv_latitudes = []         # Crear una lista vacía para almacenar los valores de latitud del CSV.
csv_longitudes = []        # Crear una lista vacía para almacenar los valores de longitud del CSV.

# Procesar los datos del CSV
for line in csv_data:
    if line.strip():          # Ignorar líneas vacías en el archivo CSV.
        parts = line.split(';')   # Dividir cada línea utilizando ';' como delimitador.
        for part in parts:
            coordinates = part.split(',')  # Dividir cada parte utilizando ',' como delimitador.
            if len(coordinates) == 2:
                lat, lon = coordinates    # Extraer los valores de latitud y longitud.
                csv_latitudes.append(float(lat))   # Convertir latitud a float y agregar a la lista.
                csv_longitudes.append(float(lon))  # Convertir longitud a float y agregar a la lista.

# Crear un DataFrame de pandas a partir de las listas de latitud y longitud del CSV
data = pd.DataFrame({'latitud': csv_latitudes, 'longitud': csv_longitudes})

# Valores de ejemplo de latitud y longitud
latitudes_ejemplo = [37.420088, 37.421088, 37.422088, 37.423088, 37.424088, 37.425088]
longitudes_ejemplo = [-6.001346, -6.001328, -6.001310, -6.001292, -6.001274, -6.001256]

# Agregar los valores de ejemplo a tus datos
data_ejemplo = pd.DataFrame({'latitud': latitudes_ejemplo, 'longitud': longitudes_ejemplo})

# Concatenar los datos de ejemplo con tus datos reales (si lo deseas)
data = pd.concat([data, data_ejemplo], ignore_index=True)

# Definir el tamaño de las celdas grandes (en grados de latitud y longitud)
cell_size_lat_large = 10  # Ajusta según tus necesidades
cell_size_lon_large = 100  # Ajusta según tus necesidades

# Agrupar tus datos en celdas grandes
data['lat_group'] = np.floor(data['latitud'] / cell_size_lat_large) * cell_size_lat_large
data['lon_group'] = np.floor(data['longitud'] / cell_size_lon_large) * cell_size_lon_large

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


plt.figure(figsize=(10, 8))
sns.kdeplot(x=data['longitud'], y=data['latitud'], cmap='viridis', fill=True)
plt.title('Heatmap of Latitude and Longitude Data')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.show()