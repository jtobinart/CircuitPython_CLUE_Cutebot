#Cutebot_line_following__better__.py
#Version 1.0
#Author(s): James Tobin


######################################################
#   Version Notes
######################################################
'''
A countdown clock and a more advanced line following code was implemented in this version.
'''


######################################################
#   Imports
######################################################
import cutebot
from cutebot import clue


######################################################
#   Functions
######################################################
def countdown(duration):
    duration = max(duration, 1.5)   # Make sure the time is at least 1.5 seconds long
    duration/=6     # Divide the time equally. There are 6 because the last note plays twice as long
    print('5')
    clue.play_tone(1568,duration)   # G6 music note
    print('4')
    clue.play_tone(1396.9,duration)     # F6 music note
    print('3')
    clue.play_tone(1318.5,duration)     # E6 music note
    print('2')
    clue.play_tone(1174.7,duration)     # D6 music note
    print('1')
    clue.play_tone(1046.5,(duration*2))     # C6 music note


######################################################
#   Variables
######################################################
last_turn_was_left = True   # Cutebot can have trouble finding the line quickly. This variable helps it remember were it saw it last.
speed = 20               # Set the speed of the robot


######################################################
#   Main Code
######################################################
print("\nPress the B button to stop the program. This program will start in...")
countdown(3)
print("Looking for line!")

while True:
    if clue.button_b:       # Ask clue if the B button was pressed.
        # If it was pressed do these things
        cutebot.motorsOff()     # Stop the motors
        break                   # Stop the while loop

    leftSide, rightSide = cutebot.getTracking()     # Ask Cutebot if it sees the line. (True = I see black; False = I do not see black.) 
    print(leftSide, rightSide)

    if leftSide == True and rightSide == True:      # Go forwards when both are True
        cutebot.motors(speed,speed)                     # Set motor speed
        print("Forward")
    elif leftSide == False and rightSide == True:   # Go right if rightSide is True
        cutebot.motors(speed,0)                         # Set motor speed
        last_turn_was_left = False                      # Remember that we did not turn left
        print("Right")
    elif leftSide == True and rightSide == False:   # Go left if leftSide is True
        cutebot.motors(0,speed)                         # Set motor speed
        last_turn_was_left = True                       # Remember that we turned left
        print("Left")
    elif leftSide == False and rightSide == False:  # Spin back if both are False
        # If you Cutebot is lost, it will spin in the direction it last saw the color black.
        if last_turn_was_left == True:              # Did Cutebot last turn left?
            cutebot.motors(-speed,speed)                # Set motor speed
            print("Spin Left")
        else:                                       # If Cutebot didn't last turn left then go right.
            cutebot.motors(speed,-speed)                # Set motor speed
            print("Spin Right")
    else:
        print("***ERROR: UNKNOWN TRACKING STATE***")

print("End")