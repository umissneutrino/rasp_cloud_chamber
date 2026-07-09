from time import sleep
import os

from temperature_sensor import read_all_temperatures


# Width of each sensor column in the terminal display.
COLUMN_WIDTH = 28


def clear_terminal():
    """
    Clear the terminal screen.

    This makes the program look like a live dashboard instead of printing
    endless lines forever.
    """

    os.system("clear")


def format_temperature(sensor_data):
    """
    Format one sensor's temperature as a readable string.
    """

    celsius = sensor_data["celsius"]
    fahrenheit = sensor_data["fahrenheit"]

    return f"{celsius:.2f} °C / {fahrenheit:.2f} °F"


def print_sensor_columns(temperatures):
    """
    Print all sensors in columns.

    If one sensor is connected, it prints one column.
    If two sensors are connected, it prints two columns.
    If more sensors are connected, it automatically adds more columns.
    """

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


def main():
    """
    Main program loop.

    This keeps reading the sensors once every second until the user presses Ctrl+C.
    """

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