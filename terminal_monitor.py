from time import sleep
## python built in library to pasuse a program for a given amount of time

## We import function from the temperature_sensor.py file to read the temperature from the sensor  
from temperature_sensor import (
    find_sensor_file,
    read_temperature_celsius,
    celsius_to_farenheit,
)

# this is the main function that will be called when the program is run, it will 
# find the sensor file, and then it will read the temperature from the sensor file 
# and print it to the terminal. It will also handle any exceptions that may occur 
# while reading the temperature and print an error message to the terminal. 
# The program will run in a loop until the user presses Ctrl+C to exit the program.
def main(): 
    sensor_file = find_sensor_file()

    print("Reading the temperature from:\t ", sensor_file)
    print("Press Ctrl+C to exit the program.")

    condition = True

    while condition:
        try: 
            temperature_celsius = read_temperature_celsius(sensor_file)
            temperature_farenheit = celsius_to_farenheit(temperature_celsius)

            print(f"Temperature: {temperature_celsius:.2f} °C | {temperature_farenheit:.2f} °F")

        except Exception as e:
                print(f"Error reading temperature: {e}")

        sleep(1)  # Wait for 1 second before reading again

        if __name__ == "__main__":
            main()