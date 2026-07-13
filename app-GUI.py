import tkinter as tk
from datetime import datetime

from temperature_sensor import read_all_temperatures


REFRESH_RATE_MS = 1000


class CloudChamberGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Cloud Chamber Temperature Monitor")
        self.root.geometry("700x400")

        self.title_label = tk.Label(
            self.root,
            text="Cloud Chamber Temperature Monitor",
            font=("Arial", 20, "bold"),
        )
        self.title_label.pack(pady=15)

        self.time_label = tk.Label(
            self.root,
            text="Last updated: --",
            font=("Arial", 12),
        )
        self.time_label.pack(pady=5)

        self.sensor_frame = tk.Frame(self.root)
        self.sensor_frame.pack(pady=20)

        self.status_label = tk.Label(
            self.root,
            text="Starting sensor monitor...",
            font=("Arial", 12),
        )
        self.status_label.pack(pady=10)

        self.sensor_labels = {}

        self.update_temperatures()

    def clear_sensor_frame(self):
        for widget in self.sensor_frame.winfo_children():
            widget.destroy()

    def create_sensor_card(self, sensor_name, sensor_data, column_number):
        sensor_id = sensor_data["id"]
        celsius = sensor_data["celsius"]
        fahrenheit = sensor_data["fahrenheit"]

        card = tk.Frame(
            self.sensor_frame,
            borderwidth=2,
            relief="groove",
            padx=20,
            pady=15,
        )

        card.grid(row=0, column=column_number, padx=10, pady=10)

        name_label = tk.Label(
            card,
            text=sensor_name,
            font=("Arial", 16, "bold"),
        )
        name_label.pack()

        id_label = tk.Label(
            card,
            text=sensor_id,
            font=("Arial", 9),
        )
        id_label.pack(pady=5)

        temp_label = tk.Label(
            card,
            text=f"{celsius:.2f} °C\n{fahrenheit:.2f} °F",
            font=("Arial", 18),
        )
        temp_label.pack(pady=10)

    def update_temperatures(self):
        try:
            temperatures = read_all_temperatures()

            self.clear_sensor_frame()

            for column_number, (sensor_name, sensor_data) in enumerate(temperatures.items()):
                self.create_sensor_card(sensor_name, sensor_data, column_number)

            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.time_label.config(text=f"Last updated: {current_time}")
            self.status_label.config(text="Sensors connected")

        except Exception as error:
            self.status_label.config(text=f"Error reading sensors: {error}")

        self.root.after(REFRESH_RATE_MS, self.update_temperatures)


def main():
    root = tk.Tk()
    app = CloudChamberGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()