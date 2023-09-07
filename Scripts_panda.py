import sqlite3
import pandas as pd

# Connect to the SQLite database
conn = sqlite3.connect('/home/azken/Database/sensor.db')


# Query data from the database and load it into a DataFrame
query = "SELECT * FROM ASV_variables"
df = pd.read_sql_query(query, conn)

# Close the database connection
conn.close()
