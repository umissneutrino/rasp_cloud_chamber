## very simple code, which turns relay on and off every 3 seconds.
## this is a test before we connect the pi and the whole circuit to a high voltage
## so that we are working for just 3 seconds and then we turn the relay off
## we will use a seperate code in relaySystem.py, which will actually actually allow us to cnotrol the whole circuit.
## later everythin will be integrated in the app-GUI.py


## a python library called gpiozerois used to control the GPIO pins of the Raspberry Pi.
## It provides a simple interface for controlling devices like relays, LEDs, and motors.
## this imports output devices from the gpiozero library, which allows us to control the relay connected to the GPIO pin.
# now one GPIO pin can be used as an output signal.
# and the sleep() functon just pauses the program for specified seconds.  
from gpiozero import OutputDevice
from time import sleep

## specify the GPIO pin we are using and a GND, which are located in pin number(12 and 14).
RELAY_PIN = 18

## the relay on and off in my while loop is controlled by the OutputDevice class from the gpiozero library.
## so here i am just initializing the relay object with the specified GPIO pin, setting it to active low (active_high=False), and setting the initial value to False (relay off).
## So what this means is that when the relay is off, the GPIO pin will be set to a high voltage (3.3V), and when the relay is on, the GPIO pin will be set to a low voltage (0V).
relay = OutputDevice(RELAY_PIN, active_high=False, initial_value=False)
## read the bottom explanation to understand this part

## active_high = relay on and vice versa.

print("Relay system initialized.")
print("Relay should turn ON for 3 seconds, then OFF for 3 seconds.")
print("Press Ctrl+C to stop.")

## this is  an infinite loop which will keep runnig until you hit the control+c button to stop the program.
## later you can use a boolean to control the relay to chnage the bool value to false to end the loop
while True: 
    print("Turning relay ON.")
    relay.on()
    sleep(3)

    print("Turning relay OFF.")
    relay.off()
    sleep(3)


    ###################################
    #            EXPLANATION   
    ###################################         

## Summay for why we need the code for a relay system:
"""
relay system is just siple as turning a switch of light on and off
with a little switch on and switch off button we can turn the lights on or off.

But,in our circuit

the relay device has two different side, one can be turned on or off using a small signal current from
the device without actually damaging the gpio pins(as they can only handle small amount of voltage 3.3V )
But we also have power source with 12V output, which can be used for powering up the peltiers, and the fan 
which will need heavy amount of the power.

so rather than a person turning the stuffs on and off again, the pi would control this by proving a small signal, 
that is why we would need the GPIO pins connected with teh relay device.

so summary would be :
Raspberry Pi → sends small signal → relay → controls big power
"""
