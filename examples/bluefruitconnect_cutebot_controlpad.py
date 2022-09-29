# bluefruitconnect_cutebot_controlpad.py
# Date: Sep. 27, 2022
# Version: 3.0
# Author(s): James Tobin

######################################################
#   HOW TO USE
######################################################
'''
Run this program on your clue. 

On your mobile device, open the Adafruit Bluefruit LE Connect app. 
Top the Connect button. Your clue's name should start with CIRUITPY. 
Tap the Controller button and then tap Control Pad.

Enjoy!
'''

######################################################
#   Version Notes
######################################################
'''
v3.0
 - buttonPress() function added.
 - Comments edited to make the code more readable.
 - Added HOW TO USE section.
 - Compatible with CircuitPython v7.x

v2.0
 - Reconfigured buttons.
 - Added comments.
 - Compatible with CircuitPython v5.x
'''

######################################################
#   Import
######################################################
from adafruit_ble import BLERadio
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.nordic import UARTService
from adafruit_bluefruit_connect.packet import Packet
from jisforjt_cutebot_clue import cutebot
from adafruit_clue import clue


# Used to create random neopixel colors
import random

# Only the packet classes that are imported will be known to Packet.
from adafruit_bluefruit_connect.button_packet import ButtonPacket


######################################################
#   Functions
######################################################
def buttonPress():
    '''
    Why sperate this part out. Well it appears that CircuitPython runs soother
    when button presses are checked in a function. No more issues since doing 
    this. This was reccomended by another Adafruit users, username unknown.
    '''
    if clue.button_a:
        return True
    return False


######################################################
#   Variables
######################################################
ble = BLERadio()                                            # Turn on Bluetooth
uart_server = UARTService()                                 # Turn on UART
advertisement = ProvideServicesAdvertisement(uart_server)   # Set up notice for other devices that Clue has a Bluetooth UART connection

maxSpeed = 35

clue.sea_level_pressure = 1020                              # Set sea level pressure for Clue's Altitude sensor.


######################################################
#   Main Loop
######################################################
while True:
    print("WAITING for BlueFruit device...")
    
    # Advertise when not connected.
    ble.start_advertising(advertisement)                # Tell other devices that Clue has a Bluetooth UART connection.
    while not ble.connected:                            # Check to see if another device has connected with the Clue via Bluetooth.
        if buttonPress():
            time.sleep(0.2)
            break
        pass                                            # Do nothing this loop.

    # Connected
    ble.stop_advertising()                              # Stop telling other devices about the Clue's Bluetooth UART Connection.
    print("CONNECTED")

    # Loop and read packets
    while ble.connected:                                # Check to see if we are still connected.

        if buttonPress():
            time.sleep(0.2)
            break

        # Keeping trying until a good packet is received
        try:
            packet = Packet.from_stream(uart_server)    # Try to get new messages from connected device.
        except ValueError:
            continue

        # Only handle button packets
        if isinstance(packet, ButtonPacket) and packet.pressed:     # Check to see if new messages have anything we can use.
            if packet.button == ButtonPacket.UP:                    # Check to see if the useful message says the up button was pressed.
                print("Button UP")
                cutebot.motors(maxSpeed,maxSpeed)                                                           
                cutebot.headlights(3,[255,255,255])
            elif packet.button == ButtonPacket.DOWN:                  # Check to see if the useful message says the down button was pressed.
                print("Button DOWN")
                cutebot.motors(-maxSpeed,-maxSpeed)
                cutebot.headlights(0,[0,0,0])
            elif packet.button == ButtonPacket.LEFT:                  # Check to see if the useful message says the left button was pressed.
                print("Button LEFT")
                cutebot.motors(int(maxSpeed/2),maxSpeed)
                cutebot.headlights(1,[150,50,0])
                cutebot.headlights(2,[0,0,0])
            elif packet.button == ButtonPacket.RIGHT:                 # Check to see if the useful message says the right button was pressed.
                print("Button RIGHT")
                cutebot.motors(maxSpeed,int(maxSpeed/2))
                cutebot.headlights(1,[0,0,0])
                cutebot.headlights(2,[200,100,0])
            elif packet.button == ButtonPacket.BUTTON_1:              # Check to see if the useful message says button 1 was pressed.
                print("Button 1: Stop and lights off")
                cutebot.motorsOff()
                cutebot.lightsOff()
            elif packet.button == ButtonPacket.BUTTON_2:              # Check to see if the useful message says button 2 was pressed.
                print("Button 2: Random neopixel color")
                colors = [] 
                for i in range(3):
                    colors.append(random.randint(0, 255))
                cutebot.pixels(3,colors)
            elif packet.button == ButtonPacket.BUTTON_3:              # Check to see if the useful message says button 3 was pressed.
                print("----------------------------------")
                print("Button 3: Cutebot Sensors")
                print("Sonar: {:.2f}".format(cutebot.sonar))
                s_left, s_right = cutebot.tracking
                print("Left Line Tracking: {}".format(s_left))
                print("Right Line Tracking: {}".format(s_right))
                print("P1: {}".format(cutebot.p1))
                print("P2: {}".format(cutebot.p2))
                print("----------------------------------")
            elif packet.button == ButtonPacket.BUTTON_4:              # Check to see if the useful message says button 4 was pressed.
                print("----------------------------------")
                print("Button 4: Clue Sensors")
                print("Acceleration: {:.2f} {:.2f} {:.2f} m/s^2".format(*clue.acceleration))
                print("Gyro: {:.2f} {:.2f} {:.2f} dps".format(*clue.gyro))
                print("Magnetic: {:.3f} {:.3f} {:.3f} uTesla".format(*clue.magnetic))
                print("Pressure: {:.3f} hPa".format(clue.pressure))
                print("Altitude: {:.1f} m".format(clue.altitude))
                print("Temperature: {:.1f} C".format(clue.temperature))
                print("Humidity: {:.1f} %".format(clue.humidity))
                print("Proximity: {}".format(clue.proximity))
                print("Gesture: {}".format(clue.gesture))
                print("Color: R: {} G: {} B: {} C: {}".format(*clue.color))
                print("----------------------------------")

    # Disconnected
    print("DISCONNECTED")
