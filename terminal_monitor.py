from time import sleep
import os
## python built in library to pasuse a program for a given amount of time

## We import function from the temperature_sensor.py file to read the temperature from the sensor  
from temperature_sensor import (
    read_all_temperatures
)

COLUMN_WIDTH = 25  # Width of each column in the table


def clear_terminal():
    os.system("clear")


def format_temperature(sensor_data):
    celsius = sensor_data["celsius"]
    fahrenheit = sensor_data["fahrenheit"]

    return f"{celsius:.2f} °C / {fahrenheit:.2f} °F"


def print_sensor_columns(temperatures):
    sensor_names = list(temperatures.keys())

    header_row = ""
    id_row = ""
    temperature_row = ""

    for sensor_name in sensor_names:
        sensor_data = temperatures[sensor_name]

        header_row += sensor_name.ljust(COLUMN_WIDTH)
        id_row += sensor_data["id"].ljust(COLUMN_WIDTH)
        temperature_row += format_temperature(sensor_data).ljust(COLUMN_WIDTH)

    print(header_row)
    print(id_row)
    print(temperature_row)

# this is the main function that will be called when the program is run, it will 
# find the sensor file, and then it will read the temperature from the sensor file 
# and print it to the terminal. It will also handle any exceptions that may occur 
# while reading the temperature and print an error message to the terminal. 
# The program will run in a loop until the user presses Ctrl+C to exit the program.
def main():
    while True:
        clear_terminal()

        print("Cloud Chamber Temperature Monitor")
        print("Press Ctrl+C to stop.\n")

        try:
            temperatures = read_all_temperatures()
            print_sensor_columns(temperatures)

        except Exception as error:
            print(f"Error reading sensors: {error}")

        sleep(1)


if __name__ == "__main__":
    main()