import csv

# Read the AML file and extract data
aml_file = "aml_log_2023-09-27_10-51-24.aml"  # Replace with your AML file path

sensor_metadata = []
sensor_data = []
measurement_metadata = {}
measurement_data = []
latitude = "37.4186993"  # Replace with your latitude value
longitude = "-5.9975079"  # Replace with your longitude value

with open(aml_file, "r") as file:
    section = None
    for line in file:
        line = line.strip()
        if line.startswith("[") and line.endswith("]"):
            section = line[1:-1]
        elif section == "SensorMetaData":
            sensor_metadata.append(line.split(","))
        elif section == "SensorData":
            sensor_data.append(line.split(","))
        elif section == "MeasurementMetadata":
            if "=" in line:
                key, value = line.split("=")
                if key == "Columns":
                    measurement_metadata["Columns"] = value.split(",")
                elif key == "Units":
                    measurement_metadata["Units"] = value.split(",")
        elif section == "MeasurementData":
            measurement_data.append(line.split(","))

# Add latitude and longitude columns to MeasurementMetadata
measurement_metadata["Columns"].extend(["Latitude", "Longitude"])

# Add latitude and longitude values to MeasurementData
for row in measurement_data:
    row.extend([latitude, longitude])

# Write the extracted data to a CSV file
csv_file = "aml_log_2023-09-27_10-51-24.csv"  # Replace with your desired CSV file path

with open(csv_file, "w", newline="") as csvfile:
    # Write Sensor Meta Data as columns
    writer = csv.writer(csvfile)
    writer.writerow(["SensorMetaData"])
    writer.writerow(["Port", "Model", "SerialNumber", "Firmware", "Parameter", "Units",
                     "CalibrationDate", "CalibrationTime", "Accuracy", "RangeMin", "RangeMax"])
    writer.writerows(sensor_metadata)

    # Write Sensor Data as data
    writer.writerow([])  # Empty line
    writer.writerow(["SensorData"])
    writer.writerow(["Port", "Model", "SerialNumber", "Firmware", "Parameter", "Units",
                     "CalibrationDate", "CalibrationTime", "Accuracy", "RangeMin", "RangeMax"])
    writer.writerows(sensor_data)

    # Write Measurement Metadata as column names
    writer.writerow([])  # Empty line
    writer.writerow(["MeasurementMetadata"])
    column_names = measurement_metadata["Columns"]
    writer.writerow(column_names)

    # Write Measurement Data
    writer.writerows(measurement_data)

print(f"Data has been written to {csv_file}")
