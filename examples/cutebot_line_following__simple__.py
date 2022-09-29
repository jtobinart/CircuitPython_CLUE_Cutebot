# Cutebot_Line_Following.py
# Date: Sep. 27, 2022
# Version: 3.0
# Author(s): James Tobin

######################################################
#   HOW TO USE:
######################################################
'''
Draw a black line on a white surface. Place the Cutebot over
the line and watch it follow it.

'''

######################################################
#   Version Notes
######################################################
'''
v3.0
 - Add STOP functionality (Button A). Turns off motors and lights.
 - Comments edited to make them easier to read.
 - Added HOW TO USE section.
 - Compatible with CircuitPython v7.x

v2.0
 - This is a simple line following program that is similar to the method used
   in the Cutebot's Instruction Manual.
 - Compatible with CircuitPython v5.x
'''

######################################################
#   Imports
######################################################
from jisforjt_cutebot_clue import cutebot
from adafruit_clue import clue


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
speed = 20               # Set the speed of the robot


######################################################
#   Main Loop
######################################################
while True:
    if buttonPress():                          # Check if Button A is pressed.
        cutebot.motorsOff()
        cutebot.lightsOff()
        break

    leftSide, rightSide = cutebot.tracking     # Ask Cutebot if it sees the line. (True = I see black; False = I don't see black.) 
    print(leftSide, rightSide)                      # Show us what the Cutebot sees

    if leftSide == True and rightSide == True:      # Go forwards when both are True
        cutebot.motors(speed,speed)                     # Set motor speed
        print("Forward")
    elif leftSide == False and rightSide == True:   # Go right if rightSide is True
        cutebot.motors(speed,0)                         # Set motor speed
        print("Right")
    elif leftSide == True and rightSide == False:   # Go left if leftSide is True
        cutebot.motors(0,speed)                         # Set motor speed
        print("Left")
    else:
        print("Searching for line...")