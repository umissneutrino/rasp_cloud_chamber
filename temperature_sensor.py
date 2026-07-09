from pathlib import Path

## this is the root path for the wire 1
## the reason we do this is beacause we are not going to change the path, and thats why the SENSOR_ROOT is in all caps meaning it is a global constant
SENSOR_ROOT = Path("/sys/bus/w1/devices")


##this function is used to find the sensor file, and it will return the path to the sensor file, if it is not found it will raise a FileNotFoundError
def find_sensor_file():
    sensor_dirs = sorted(SENSOR_ROOT.glob("28-*"))

    if not sensor_dirs:
        raise FileNotFoundError("No DS18B20 sensor found, check the wiring and 1-wire setup.")
    
    sensor_file = {}
    for index, sensor_dir in enumerate(sensor_dirs, start=1):
        sensor_name = f"Sensor {index}"
        sensor_id = sensor_dir.name
        sensor_file = sensor_id / "w1_slave"

        sensor_file(sensor_name)={
            "id" : sensor_id,
            "file" : sensor_file
        }
    return sensor_file


## inside the sensor folder the temperature reading is stored inside the w1_slave folder,
## and the read_raw_sensor_text function is used to read the contents of the w1_slave file 
# and return it as a string. The parse_temperature_celsius function takes the raw text from 
# the sensor file, checks if the data is valid, and extracts the temperature in Celsius. 
# If the data is not valid or incomplete, it raises a ValueError with an appropriate message.
def read_raw_sensor_text(sensor_file):
    return sensor_file.read_text()

def parse_temperature_celsius(raw_text):
    lines = raw_text.strip().splitlines()


##the above function, uses the chain of strip() and splitlines() to clear out the leading and trailing unwanted spaces and then the 
## splitlines() method is used to split the string into a list of lines based on the newline character.
## this way whever we go to the file path and read the text, we will get bunch of code like 79 00 01 00 00 7f : crc=4d YES
##                                                                                          78 00 01 00 00 7f : t=26000
## the t=26000 is the temperature reading in millicelsius, and we will extract that value and convert it to celsius by dividing it by 1000.0
    if len(lines) < 2:
        raise ValueError("Sensor output is incomplete.")

    if "YES" not in lines[0]:
        raise ValueError("Sensor data is not valid.")

    temperature_marker = "t="
    marker_position = lines[1].find(temperature_marker)

    if marker_position == -1:
        raise ValueError("Temperature data not found in sensor output.")

## this below code now will read onl after t= and then conet the string into the integer using the casting.
    temperature_text = lines[1][marker_position + len(temperature_marker):]
    temperature_milicelsius = int(temperature_text)
    temperature_celsius = temperature_milicelsius / 1000.0
    return temperature_celsius


##simple function taking the celsius as the parameter and conveting it to farenheit and returning the value
def celsius_to_farenheit(celsius):
    return (celsius * 9.0 / 5.0) + 32.0   

def read_temperature_celsius(sensor_file):
    raw_text = read_raw_sensor_text(sensor_file)
    temperature_celsius = parse_temperature_celsius(raw_text)   

    return temperature_celsius
def read_all_temperatures():
    sensor_files = find_sensor_file()

    temperatures = {}

    for sensor_name, sensor_info in sensor_files.items():
        sensor_id = sensor_info["id"]
        sensor_file = sensor_info["file"]

        temperature_celsius = read_temperature_celsius(sensor_file)
        temperature_fahrenheit = celsius_to_farenheit(temperature_celsius)

        temperatures[sensor_name] = {
            "id": sensor_id,
            "celsius": temperature_celsius,
            "fahrenheit": temperature_fahrenheit,
        }

    return temperatures