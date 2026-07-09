from pathlib import Path

# This is the Linux folder where Raspberry Pi lists 1-Wire devices.
# DS18B20 temperature sensors usually appear inside this folder.
SENSOR_ROOT = Path("/sys/bus/w1/devices")


def find_sensor_files():
    """
    Find all connected DS18B20 sensors.

    Each DS18B20 sensor usually appears as a folder starting with '28-'.
    Example:
        /sys/bus/w1/devices/28-00000abc1234

    This function returns a dictionary like:

        {
            "Sensor 1": {
                "id": "28-00000abc1234",
                "file": Path("/sys/bus/w1/devices/28-00000abc1234/w1_slave")
            }
        }
    """

    # Find every folder that starts with "28-".
    # sorted() keeps the order stable, so Sensor 1 and Sensor 2 stay consistent.
    sensor_dirs = sorted(SENSOR_ROOT.glob("28-*"))

    # If no sensors are found, stop and give a useful error.
    if not sensor_dirs:
        raise FileNotFoundError(
            "No DS18B20 sensors found. Check wiring, 1-Wire setup, and reboot the Pi."
        )

    # This dictionary will store all sensors we find.
    sensor_files = {}

    # Loop through each sensor folder.
    # start=1 makes the first sensor become Sensor 1 instead of Sensor 0.
    for index, sensor_dir in enumerate(sensor_dirs, start=1):
        sensor_name = f"Sensor {index}"
        sensor_id = sensor_dir.name

        # The actual temperature data is inside the w1_slave file.
        sensor_file = sensor_dir / "w1_slave"

        # Store the sensor ID and file path.
        sensor_files[sensor_name] = {
            "id": sensor_id,
            "file": sensor_file,
        }

    return sensor_files


def read_raw_sensor_text(sensor_file):
    """
    Read the raw text from the sensor's w1_slave file.

    The raw text usually looks something like:

        xx xx xx xx : crc=YES
        xx xx xx xx t=23562

    The number after t= is the temperature in milli-Celsius.
    """

    return sensor_file.read_text()


def parse_temperature_celsius(raw_text):
    """
    Extract the Celsius temperature from the raw DS18B20 text.
    """

    # Split the raw text into separate lines.
    lines = raw_text.strip().splitlines()

    # A valid DS18B20 reading should have at least two lines.
    if len(lines) < 2:
        raise ValueError("Sensor output is incomplete.")

    # The first line should contain YES if the sensor read passed the CRC check.
    if "YES" not in lines[0]:
        raise ValueError("Sensor data is not valid. CRC check failed.")

    # The temperature value appears after "t=" on the second line.
    temperature_marker = "t="
    marker_position = lines[1].find(temperature_marker)

    # If "t=" is missing, we cannot extract the temperature.
    if marker_position == -1:
        raise ValueError("Temperature data was not found in sensor output.")

    # Get only the number after "t=".
    temperature_text = lines[1][marker_position + len(temperature_marker):]

    # Convert the text value into an integer.
    temperature_millicelsius = int(temperature_text)

    # DS18B20 gives temperature in thousandths of a degree Celsius.
    temperature_celsius = temperature_millicelsius / 1000.0

    return temperature_celsius


def celsius_to_fahrenheit(celsius):
    """
    Convert Celsius to Fahrenheit.
    """

    return (celsius * 9.0 / 5.0) + 32.0


def read_temperature_celsius(sensor_file):
    """
    Read one sensor file and return its temperature in Celsius.
    """

    raw_text = read_raw_sensor_text(sensor_file)
    temperature_celsius = parse_temperature_celsius(raw_text)

    return temperature_celsius


def read_all_temperatures():
    """
    Read every connected DS18B20 sensor.

    Returns a dictionary like:

        {
            "Sensor 1": {
                "id": "28-00000abc1234",
                "celsius": 23.5,
                "fahrenheit": 74.3
            }
        }
    """

    sensor_files = find_sensor_files()
    temperatures = {}

    for sensor_name, sensor_info in sensor_files.items():
        sensor_id = sensor_info["id"]
        sensor_file = sensor_info["file"]

        temperature_celsius = read_temperature_celsius(sensor_file)
        temperature_fahrenheit = celsius_to_fahrenheit(temperature_celsius)

        temperatures[sensor_name] = {
            "id": sensor_id,
            "celsius": temperature_celsius,
            "fahrenheit": temperature_fahrenheit,
        }

    return temperatures