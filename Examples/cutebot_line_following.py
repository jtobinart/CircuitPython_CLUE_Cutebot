#Cutebot_Line_Following.py

import time
import cutebot
from cutebot import clue

print("Looking for line!")

last_turn_was_left = True
maxSpeed = 20

while True:
    if clue.button_b:
        cutebot.motorsOff()
        break

    leftSide, rightSide = cutebot.getTracking()
    print(leftSide, rightSide)

    if leftSide == True and rightSide == True:
        cutebot.motors(maxSpeed,maxSpeed)
        print("Straight")
    elif leftSide == False and rightSide == True:
        cutebot.motors(maxSpeed,0)
        last_turn_was_left = False
        print("Right")
    elif leftSide == True and rightSide == False:
        cutebot.motors(0,maxSpeed)
        last_turn_was_left = True
        print("Left")
    elif leftSide == False and rightSide == False:
        if last_turn_was_left == True:
            cutebot.motors(-maxSpeed,maxSpeed)
            print("Sharp Left")
        else:
            cutebot.motors(maxSpeed,-maxSpeed)
            print("Sharp Right")
    else:
        print("ERROR")

print("End")