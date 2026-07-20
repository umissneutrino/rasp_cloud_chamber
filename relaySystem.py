## todo
## write code to control whole cloud chamber.

## will be ading new sensor info now.

from gpiozero import OutputDevice

## adding a dictonary to connect the gpio with the relay

RELAY_CONFIG = {
        "peltier":{
            "pin":17,
            "active_high":False,
            },
##essntially what this is doing is assigning the pin 17, and the 27 to the pin for peltier and fan, then seting the switch to off, which is what active_high:False means.

        "fan": {
            "pin":27,
            "active_high":False,
            }
        #These might be the future devices that we would be able to use.
    # "lights": {
    #     "pin": 22,
    #     "active_high": False,
    # },

    # "electric_field": {
    #     "pin": 23,
    #     "active_high": False,
    # },

    }

class CloudChamberController:
    #controls all the relay-operated cloud chamber devices
    def __init__(self, relay_config=None):
        config = RELAY_CONFIG

        self._relays = {}

        for device_name, settings in config.items():
            relayOutputDevice(
                pin=settings["pin"],
                active_high=settings.get("active_high", False),
                initial_value=False,
            )

            self._relays[device_name] = relay

    @property
    def device_names(self):
        """Return the names of all configured devices."""

        return tuple(self._relays.keys())

    def _get_relay(self, device_name):
        """Find and return a relay using its device name."""

        normalized_name = device_name.strip().lower()

        if normalized_name not in self._relays:
            valid_names = ", ".join(self.device_names)

            raise ValueError(
                f"Unknown device '{device_name}'. "
                f"Valid devices: {valid_names}"
            )

        return self._relays[normalized_name]

    def turn_on(self, device_name):
        """Turn one device on."""

        relay = self._get_relay(device_name)
        relay.on()

    def turn_off(self, device_name):
        """Turn one device off."""

        relay = self._get_relay(device_name)
        relay.off()

    def toggle(self, device_name):
        """Reverse the current state of one device."""

        relay = self._get_relay(device_name)
        relay.toggle()

    def is_on(self, device_name):
        """Return True if a device is currently on."""

        relay = self._get_relay(device_name)

        return bool(relay.value)

    def get_status(self):
        """Return the current status of every configured device."""

        status = {}

        for device_name, relay in self._relays.items():
            status[device_name] = bool(relay.value)

        return status

    def all_off(self):
        """Turn every relay-operated device off."""

        for relay in self._relays.values():
            relay.off()

    def close(self):
        """Turn everything off and release the GPIO resources."""

        self.all_off()

        for relay in self._relays.values():
            relay.close()

