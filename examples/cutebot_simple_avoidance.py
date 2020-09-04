#cutebot_simple_avoidance.py
#Version 1.0
#Author(s): James Tobin


######################################################
#   Version Notes
######################################################
'''
Use the cutebot's ultrasound distance sensor and the CLUE's proximity
sensor to avoid objects. The cutebot's neopixels display their current
action.

green = going forward
yellow = avoiding an object between 20 to 50 centimeters away
red = avoiding an object 20 centimeters or less away
blue = avoiding an object seen by the proximity sensor
'''

######################################################
#   Imports
######################################################
import os
import time
import cutebot
from cutebot import clue


######################################################
#   Variables
######################################################
max_speed = 50


######################################################
#   Main Loop
######################################################

while True:
	distance = cutebot.getSonar()
	prox = clue.proximity
	if prox > 5:
		cutebot.motors(((-max_speed)), (-max_speed / 2))
		cutebot.pixels(3,[0,0,255])		# blue
		time.sleep(0.25)
	elif distance >= 50:
		cutebot.motors(max_speed, max_speed)
		cutebot.pixels(3,[0,255,0])		# green
	elif distance > 20 and distance < 50: 
		alpha = 1 - distance / 200
		cutebot.motors((max_speed/2 * alpha), max_speed)
		cutebot.pixels(3,[255,255,0])	# yellow
	else:
		alpha = -1 + distance / 200
		cutebot.motors(((max_speed / 2) * alpha), (max_speed / 2))
		cutebot.pixels(3,[255,0,0])		# red