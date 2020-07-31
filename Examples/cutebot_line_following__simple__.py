#Cutebot_Line_Following.py
#Version 1.0
#Author(s): James Tobin


######################################################
#   Version Notes
######################################################
'''
This is a simple line following program that is similar to the method used
in the Cutebot's Instruction Manual.
'''


######################################################
#   Imports
######################################################
import cutebot
from cutebot import clue


######################################################
#   Variables
######################################################
speed = 20               # Set the speed of the robot


######################################################
#   Main Code
######################################################
while True:

    leftSide, rightSide = cutebot.getTracking()     # Ask Cutebot if it sees the line. (True = I see black; False = I don't see black.) 
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

print("End")