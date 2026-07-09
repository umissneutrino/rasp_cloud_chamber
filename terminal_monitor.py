from time import sleep
from datetime import datetime

from temperature_sensor import read_all_temperatures


COLUMN_WIDTH = 28


def format_temperature(sensor_data):
    """
    Convert one sensor's temperature data into a clean display string.
    """

    celsius = sensor_data["celsius"]
    fahrenheit = sensor_data["fahrenheit"]

    return f"{celsius:.2f} °C | {fahrenheit:.2f} °F"


def print_sensor_columns(temperatures):
    """
    Print all sensors side-by-side in columns.

    The number of columns automatically depends on the number of sensors detected.
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
    Main terminal monitor.

    This keeps printing temperature readings once every second.
    Press Ctrl+C to stop the program.
    """

    print("Cloud Chamber Temperature Monitor")
    print("Press Ctrl+C to stop.\n")

    while True:
        try:
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            print(f"Time: {current_time}")

            temperatures = read_all_temperatures()
            print_sensor_columns(temperatures)

            print("-" * 80)

        except Exception as error:
            print(f"Error reading sensors: {error}")
            print("-" * 80)

        sleep(1)


if __name__ == "__main__":
    main()