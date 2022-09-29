# Cutebot_line_following__better__.py
# Date: Sep. 27, 2022
# Version 3.0
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
 - Updated STOP button (Button A).
    - Put inside function.
    - Turns off lights too.
 - Comments edited to make them easier to read.
 - Added HOW TO USE section.
 - Compatible with CircuitPython v7.x

v2.0
 - A countdown clock and a more advanced line following code was implemented in this version.
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

def countdown(duration):
    duration = max(duration, 1.5)       # Make sure the time is at least 1.5 seconds long
    duration/=6                         # Divide the time equally. There are 6 because the last note plays twice as long
    print('5')
    clue.play_tone(1568,duration)       # G6 music note
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
maxSpeed = 20                  # Set the speed of the robot


######################################################
#   Main Code
######################################################
print("\nPress the Button A to STOP the Cutebot. This program will start in...")
countdown(3)
print("Looking for line!")


######################################################
#   Main Loop
######################################################
while True:
    if buttonPress():						   # Check if Button A is pressed.
		cutebot.motorsOff()
		cutebot.lightsOff()
		break

    leftSide, rightSide = cutebot.tracking     # Ask Cutebot if it sees the line. (True = I see black; False = I do not see black.) 
    print(leftSide, rightSide)

    if leftSide == True and rightSide == True:      # Go forwards when both sensors see the line (both are True)
        cutebot.motors(maxSpeed,maxSpeed)           # Set motor speed
        print("Forward")
    elif leftSide == False and rightSide == True:   # Go right when left side sensor cannot see the line.
        cutebot.motors(maxSpeed,0)                  # Set motor speed
        last_turn_was_left = False                  # Remember that we did not turn left
        print("Right")
    elif leftSide == True and rightSide == False:   # Go left when the right side sensor cannot see the line.
        cutebot.motors(0,maxSpeed)                  # Set motor speed
        last_turn_was_left = True                   # Remember that we turned left
        print("Left")
    elif leftSide == False and rightSide == False:  # Line lost. Spin in the same direction we last saw the line.
        if last_turn_was_left == True:              # Cutebot last turned left.
            cutebot.motors(-maxSpeed,maxSpeed)      # Set motor speed
            print("Spin Left")
        else:                                       # Cutebot last turned right.
            cutebot.motors(maxSpeed,-maxSpeed)      # Set motor speed
            print("Spin Right")
    else:
        print("ERROR: UNKNOWN TRACKING STATE")