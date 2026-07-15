# rasp_cloud_chamber
This repository contains Python code for controlling and monitoring the Raspberry Pi-based cloud chamber system. The Raspberry Pi is used as the main computer for reading temperature sensors and, later, controlling the relay system for the Peltier coolers and fans.

- `temperature_sensor.py` handles DS18B20 temperature sensor detection and reading.
- `terminal_monitor.py` displays live temperature readings in the terminal.
- `app-GUI.py` will display sensor readings in an interactive Python GUI.
- `relay_system.py` will handle relay control for devices such as Peltier coolers and fans.


---

## Function of each python file:

### `temperature_sensor.py`

This file handles the temperature sensor backend for the cloud chamber system.

It is responsible for:

- finding connected DS18B20 temperature sensors
- reading raw sensor data from the Raspberry Pi 1-Wire device folder
- checking whether the sensor reading is valid
- converting raw sensor values into Celsius
- converting Celsius into Fahrenheit
- returning all detected sensor readings in a clean dictionary format

This file is used by both the terminal monitor and the GUI, so the sensor-reading logic only has to be written once.

---

### `terminal_monitor.py`

This file displays live temperature readings in the Raspberry Pi terminal.

It is responsible for:

- importing temperature data from `temperature_sensor.py`
- reading all connected sensors repeatedly
- printing each sensor name, sensor ID, Celsius temperature, and Fahrenheit temperature
- supporting one or multiple sensors automatically
- allowing quick testing before using the GUI

This file is useful for checking that the sensors work correctly before running the full application window.

---

### `app-GUI.py` 

This file creates the graphical user interface for the cloud chamber temperature monitor.

It is responsible for:

- opening an interactive Tkinter window
- displaying live temperature readings from the sensors
- showing each sensor in its own visual card
- updating the readings automatically
- showing the last update time
- displaying sensor connection or error status

This file uses `temperature_sensor.py` as the backend and does not directly handle the hardware reading itself.

---

### `relay_system.py`

This file controls the relay module connected to the Raspberry Pi.

It is responsible for:

- setting up the GPIO pin used for relay control
- turning the relay on
- turning the relay off
- testing relay behavior by switching it on and off
- later controlling external devices such as Peltier coolers, fans, or lights

---
