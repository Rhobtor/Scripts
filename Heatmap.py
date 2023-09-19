import numpy as np                  
import matplotlib.pyplot as plt     
import sqlite3                     

# Read data from the CSV file (map coordinates)
with open('Alamillo95x216grid.csv', 'r') as file:
    csv_data = file.read().split(';')   # Read the CSV file and split it into a list using ';' as the delimiter.

# Initialize lists for latitude and longitude from the CSV
csv_latitudes = []         # Create an empty list to store latitude values from the CSV.
csv_longitudes = []        # Create an empty list to store longitude values from the CSV.

# Process the CSV data
for line in csv_data:
    if line.strip():          # Ignore empty lines in the CSV file.
        parts = line.split(';')   # Split each line using ';' as the delimiter.
        for part in parts:
            coordinates = part.split(',')  # Split each part using ',' as the delimiter.
            if len(coordinates) == 2:
                lat, lon = coordinates    # Extract latitude and longitude values.
                csv_latitudes.append(float(lat))   # Convert latitude to float and append to the list.
                csv_longitudes.append(float(lon))  # Convert longitude to float and append to the list.

# Connect to the SQLite database // change it if you have it locally
conn = sqlite3.connect('/home/azken/Database/sensor.db')   # Connect to the SQLite database.
cursor = conn.cursor()    # Create a cursor object to execute SQL queries.

# Define start and end date and time (adjust as needed)
fecha_inicio = '2023-09-06 16:29:29.000000'   # Define the start date and time.
fecha_fin = '2023-09-07 16:59:48.000000'     # Define the end date and time.


# SQL query to select data from the database within the specified date and time range
query = f"SELECT Latitude, Longitude, Data FROM ASV_variables WHERE Sensor='Sonar' AND Date BETWEEN '{fecha_inicio}' AND '{fecha_fin}'"
cursor.execute(query)   

# Initialize lists for latitude, longitude, and sensor values from the database
db_latitudes = []        # Create an empty list to store latitude values from the database.
db_longitudes = []       # Create an empty list to store longitude values from the database.
db_sensor_values = []    # Create an empty list to store sensor values from the database.

# Process data from the database and add it to the lists
for row in cursor.fetchall():
    lat, lon, value = row    # Extract latitude, longitude, and sensor value from the database row.
    if lat != 0 and lon != 0:  # Filter out values where latitude and longitude are not equal to 0.
        db_latitudes.append(lat)    # Append latitude to the list.
        db_longitudes.append(lon)   # Append longitude to the list.
        db_sensor_values.append(value)  # Append sensor value to the list.

# Convert the database lists to NumPy arrays for further processing
db_latitudes = np.array(db_latitudes)       # Convert latitude list to NumPy array.
db_longitudes = np.array(db_longitudes)     # Convert longitude list to NumPy array.
db_sensor_values = np.array(db_sensor_values)   # Convert sensor value list to NumPy array.

# Define a regular grid of latitude and longitude based on CSV data
min_lat, max_lat = min(csv_latitudes), max(csv_latitudes)  # Find minimum and maximum latitudes from the CSV data.
min_lon, max_lon = min(csv_longitudes), max(csv_longitudes)  # Find minimum and maximum longitudes from the CSV data.
grid_latitude = np.linspace(min_lat, max_lat, 1000)   # Create a 1D array of 1000 evenly spaced latitudes.
grid_longitude = np.linspace(min_lon, max_lon, 1000)  # Create a 1D array of 1000 evenly spaced longitudes.
grid_latitude, grid_longitude = np.meshgrid(grid_latitude, grid_longitude)  # Create a 2D grid of latitudes and longitudes.



# Filter data from the database where sensor values are between -50 and 50, and lat/lon are not zero
filtered_latitudes = db_latitudes[(db_sensor_values >= -50) & (db_sensor_values <= 50) & (db_latitudes != 0) & (db_longitudes != 0)]
filtered_longitudes = db_longitudes[(db_sensor_values >= -50) & (db_sensor_values <= 50) & (db_latitudes != 0) & (db_longitudes != 0)]
filtered_sensor_values = db_sensor_values[(db_sensor_values >= -50) & (db_sensor_values <= 50) & (db_latitudes != 0) & (db_longitudes != 0)]

# Define the number of bins for the heatmap (size of drawing)
num_bins = 100  # The higher the value, the more cells will be drawn in the heatmap.

# Calculate the mean sensor value for each grid cell
heatmap, xedges, yedges = np.histogram2d(filtered_longitudes, filtered_latitudes, bins=num_bins, weights=filtered_sensor_values)

# Create a figure and axis with a transparent background
fig, ax = plt.subplots(figsize=(12, 8))   # Create a figure with specified size.
ax.patch.set_alpha(0)   # Make the axis background transparent.

# Plot the values of the sensor directly without a colormap
heatmap = ax.imshow(heatmap.T, cmap='coolwarm', extent=[xedges[0], xedges[-1], yedges[0], yedges[-1]], origin='lower', aspect='auto', alpha=1.0, vmin=-50, vmax=50)

# Add a colorbar
cbar = plt.colorbar(heatmap, ax=ax, label='Mean Sensor Value')  # Add a colorbar to the plot.

# Set plot title and axis labels
ax.set_title('Sensor Values (Filtered for Values between -50 and 50)')  
ax.set_xlabel('Longitude')  
ax.set_ylabel('Latitude')   

# Save the image to a file (adjust the name and format)
plt.savefig('heatmap.png', dpi=300, bbox_inches='tight')  

# Close the database connection
conn.close()  
