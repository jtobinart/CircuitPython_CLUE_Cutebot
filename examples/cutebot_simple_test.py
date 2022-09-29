# cutebot_simple_test.py
# Date: Sep. 27, 2022
# Version: 3.0
# Author: James Tobin

######################################################
#   HOW TO USE
######################################################
'''
Scroll down to the "Main Loop" section and uncomment the 
sensor function you want to run. There are two functions.
One shows you the Cutebot's sensor data and the second 
shows you the Clue's sensor data. 

TO UNCOMMENT: 
Delete the "#" that preceeds the function statment. 

'''

######################################################
#   Version Notes
######################################################
'''
v3.0
 - Added HOW TO USE section
 - Added Version Notes section
 - Added buttonPress() function
 - Compatible with CircuitPython v7.x

v2.0
 - Added comments.
 - Compatible with CircuitPython v5.x


'''

######################################################
#   Import
######################################################
import time
from jisforjt_cutebot_clue import cutebot
from adafruit_clue import clue


######################################################
#   Variables
######################################################
clue.sea_level_pressure = 1020                         # Set sea level pressure for Clue's Altitude sensor.


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

def cutebot_Sensors():
    print("Sonar: {:.2f}".format(cutebot.sonar))
    s_left, s_right = cutebot.tracking
    print("Left Line Tracking: {}".format(s_left))
    print("Right Line Tracking: {}".format(s_right))
    print("P1: {}".format(cutebot.p1))
    print("P2: {}".format(cutebot.p2))
    print("----------------------------------")

def clue_Sensors():
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


######################################################
#   Main Loop
######################################################
while True:
    """
    SENSORS ==========================================
    """
    cutebot_Sensors()
    #clue_Sensors()

    #=================================================
    
    time.sleep(2) # Wait for two seconds
    
    if clue.button_a:
        break
print("========== End ==========")
