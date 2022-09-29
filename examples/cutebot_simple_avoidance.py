# cutebot_simple_avoidance.py
# Date: Sep. 27, 2022
# Version: 3.0
# Author(s): James Tobin

######################################################
#   HOW TO USE:
######################################################
'''
Use the Cutebot's ultrasound distance sensor and the CLUE's proximity
sensor to avoid objects. The cutebot's neopixels display the current
action being taken.

green = All clear. Going forward!
yellow = Avoiding an object between 20 to 50 centimeters away.
red = Avoiding an object 20 centimeters or less away.
blue = Avoiding an object seen by the proximity sensor.

Play around with the distances and turning gains to see what happens.

'''

######################################################
#   Version Notes
######################################################
'''
v3.0: 
 - Pressing Button A now stops all motors and turns off lights.
 - Comments edited and added to make reading the code easier.
 - Compatible with CircuitPython v7.x

v2.0:
 - Incorporated Clue's proximity sensor.
 - Fine tuned turning.
 - Compatible with CircuitPython v5.x

'''

######################################################
#   Imports
######################################################
import time
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
max_speed = 50


######################################################
#   Main Code
######################################################
print("Press the Button A to STOP.")


######################################################
#   Main Loop
######################################################
while True:
	distance = cutebot.sonar
	prox = clue.proximity
	if prox > 5:											# Avoid object seen from the Clue's proximity sensor.
		cutebot.motors(((-max_speed)), (-max_speed / 2))
		cutebot.pixels(3,[0,0,255])		# blue
		time.sleep(0.2)
	elif distance >= 50:									# All clear. No objects less than 50 cm away.
		cutebot.motors(max_speed, max_speed)
		cutebot.pixels(3,[0,255,0])		# green
	elif distance > 20 and distance < 50: 					# Avoid object between 20-50 cm away.
		alpha = 1 - distance / 200
		cutebot.motors((max_speed/2 * alpha), max_speed)
		cutebot.pixels(3,[255,255,0])	# yellow
	else:													# Avoid object less than 20 cm away.
		alpha = -1 + distance / 200
		cutebot.motors(((max_speed / 2) * alpha), (max_speed / 2))
		cutebot.pixels(3,[255,0,0])		# red
	
	if buttonPress():										# Check if Button A is pressed.
		cutebot.motorsOff()
		cutebot.lightsOff()
		break