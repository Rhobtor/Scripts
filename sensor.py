import re

# Input string
data_string = "{mux[meta=time,1590605500.55,s],port1[data=Cond,0.000000,mS/cm][rawi=ADC,563,none][data=TempCT,23.881313,C][rawi=ADC,428710,none],port2[data=Pressure,0.071390,dbar][rawi=ADC,844470,2sComp],port3[data=SV,0.000000,m/s][rawf=NSV,0.000000,samples],derive[data=Depth,0.070998,m]}"

# Define a regular expression pattern to match components
pattern = r'data=([^,]+),([^,\]]+)'

# Find all matches of the pattern in the input string
matches = re.findall(pattern, data_string)


# Define a mapping of sensor_str to attribute names
sensor_mapping = {
    "Cond": "Conductivity",
    "TempCT": "TempCT",
    "Pressure": "pressure",
    "SV": "sv",
    "Depth": "depth"
    # Add more mappings as needed
}

# Create a dictionary to store the sensor data
sensor_data = {}


sensor_data2 = {}

# Iterate through matches and assign values to attributes based on sensor_str
for match in matches:
    sensor_str = match[0]
    sensor_val = match[1]
    
    # Check if sensor_str is in the mapping and assign the value to the corresponding attribute
    if sensor_str in sensor_mapping:
        attribute_name = sensor_mapping[sensor_str]
        sensor_data2[attribute_name] = sensor_val
        print(f"Found2 {attribute_name}: {sensor_val}")




# Print the values stored in the sensor_data dictionary
print("Values stored in sensor_data:")
for attribute_name, value in sensor_data2.items():
    print(f"{attribute_name}: {value}")
