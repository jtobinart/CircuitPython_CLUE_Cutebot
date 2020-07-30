#Cutebot_Line_Following.py
#Version 1.0
#Author(s): James Tobin

'''
######################################################
#   MIT License
######################################################

Copyright (c) 2020 James Tobin

Permission is hereby granted, free of charge, to any person obtaining a copy of 
this software and associated documentation files (the "Software"), to deal in the 
Software without restriction, including without limitation the rights to use, copy, 
modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, 
and to permit persons to whom the Software is furnished to do so, subject to the 
following conditions:

The above copyright notice and this permission notice shall be included in all 
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, 
INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A 
PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT 
HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF 
CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE 
OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


######################################################
#   Version Notes
######################################################
This is a simple line following program that is similar to the method used
in the Cutebot's Instruction Manual.
'''


######################################################
#   Imports
######################################################
import time
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
        print("Forward")                                # Show us what the Cutebot is going to do
    elif leftSide == False and rightSide == True:   # Go right if rightSide is True
        cutebot.motors(speed,0)                         # Set motor speed
        last_turn_was_left = False                      # Remember that we did not turn left
        print("Right")                                  # Show us what the Cutebot is going to do
    elif leftSide == True and rightSide == False:   # Go left if leftSide is True
        cutebot.motors(0,speed)                         # Set motor speed
        last_turn_was_left = True                       # Remember that we turned left
        print("Left")                                   # Show us what the Cutebot is going to do
    else:
        print("Searching for line...")                  # Show us what the Cutebot is going to do

print("End")