# bluefruitconnect_cutebot_controlpad.py
# Basic structure example for using the BLE Connect Control Pad
# To use, start this program, and start the Adafruit Bluefruit LE Connect app.
# Connect, and then select Controller-> Control Pad.

from adafruit_ble import BLERadio
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.nordic import UARTService
from adafruit_bluefruit_connect.packet import Packet
import cutebot
from cutebot import clue

# Only the packet classes that are imported will be known to Packet.
from adafruit_bluefruit_connect.button_packet import ButtonPacket

ble = BLERadio()
uart_server = UARTService()
advertisement = ProvideServicesAdvertisement(uart_server)

while True:
    print("WAITING for BlueFruit device...")
    # Advertise when not connected.
    ble.start_advertising(advertisement)
    while not ble.connected:
        pass

    # Connected
    ble.stop_advertising()
    print("CONNECTED")

    # Loop and read packets
    while ble.connected:

        # Keeping trying until a good packet is received
        try:
            packet = Packet.from_stream(uart_server)
        except ValueError:
            continue

        # Only handle button packets
        if isinstance(packet, ButtonPacket) and packet.pressed:
            if packet.button == ButtonPacket.UP:
                print("Button UP")
                cutebot.motors(50,50)
                cutebot.headlights(3,[100,100,100])
            if packet.button == ButtonPacket.DOWN:
                print("Button DOWN")
                cutebot.motors(-50,-50)
                cutebot.headlights(0,[0,0,0])
            if packet.button == ButtonPacket.LEFT:
                print("Button LEFT")
                cutebot.motors(20,50)
                cutebot.headlights(1,[100,100,0])
                cutebot.headlights(2,[0,0,0])
            if packet.button == ButtonPacket.RIGHT:
                print("Button RIGHT")
                cutebot.motors(50,20)
                cutebot.headlights(1,[0,0,0])
                cutebot.headlights(2,[100,100,0])
            if packet.button == ButtonPacket.BUTTON_1:
                print("Button 1: Full stop!")
                cutebot.motorsOff()
                cutebot.lightsOff()
            if packet.button == ButtonPacket.BUTTON_2:
                print("Button 2: Temperature")
                print("Temperature: {:.1f}C".format(clue.temperature))
            if packet.button == ButtonPacket.BUTTON_3:
                print("Button 3: Compass")
                print("Magnetic: {:.3f} {:.3f} {:.3f}".format(*clue.magnetic))
            if packet.button == ButtonPacket.BUTTON_4:
                print("Button 4: Sensors")
                print("Proximity: {}".format(clue.proximity))
                print("Sonar: {} cm".format(cutebot.getSonar))

    # Disconnected
    print("DISCONNECTED")
