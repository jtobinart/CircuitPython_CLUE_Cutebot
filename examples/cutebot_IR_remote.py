# cutebot_IR_remote.py
# Date: Sep. 27, 2022
# Version: 3.0
# Author(s): James Tobin

######################################################
#   HOW TO USE:
######################################################
'''
Use any IR remote you have lying around. I used a TV remote. I only use six buttons
but you can set up as many as you like.

To set up your IR remote buttons, simply aim your buttons at your Cutebot. For best 
results aim at the back. Press each button and write down the codes you see on the
Clue's display. 

Pro-Tip: Press each button a few times to make sure it wasn't miss decoded.

Afterwards, change the button directions and button_1 below, by default they are = to (None).

Now when you press a button Cutebot will follow your every command... eventually.

'''

######################################################
#   Version Notes:
######################################################
'''
v3.0 
 - Compatible with CircuitPython v7.x
 - Added HOW TO USE section.
 - Simplified code.
 - Comments edited to make them easier to read.

v2.0
 - Added comments.
 - Updated code.
 - Compatible with CircuitPython v5.x
'''

######################################################
#   Import
######################################################
import board
import pulseio
import adafruit_irremote
from jisforjt_cutebot_clue import cutebot
from adafruit_clue import clue


######################################################
#   Global Variables
######################################################
pulsein = pulseio.PulseIn(board.D16, maxlen=120, idle_state=True)       #Set Infrared (IR) pin
decoder = adafruit_irremote.GenericDecode()                             #Set infrared (IR) decoder to Adafruit's generic decoder
maxSpeed = 30

#Example:
'''
button_UP =    (255, 8,  79, 176)
button_DOWN =  (255, 8,  87, 168)
button_LEFT =  (255, 8, 247,   8)
button_RIGHT = (255, 8, 183,  72)
button_STOP =  (255, 8, 191,  64)
button_1 =     (255, 8,  63, 192)
'''

button_UP = (None)                       # Set the up button code
button_DOWN = (None)                     # Set the down button code
button_LEFT = (None)                     # Set the left button code
button_RIGHT = (None)                    # Set the right button code
button_STOP = (None)                     # Set the stop button code
button_1 = (None)                        # Set the button 1 code


######################################################
#   Main Code
######################################################
print("Waiting for remote signal...")
while True:
    code = None

    pulses = decoder.read_pulses(pulsein)                   # Stop, wait and listen for an IR signal.

    try:
        code = decoder.decode_bits(pulses)                  # Try to decode pulses.
    except:
        pass                                                # Failed to decode pulses.

    if code == button_UP:                       # Check to see if our code matches.
        print("Button UP")
        cutebot.motors(maxSpeed,maxSpeed)                                                           
        cutebot.headlights(3,[255,255,255])
    elif code == button_DOWN:                   # Check to see if our code matches.
        print("Button DOWN")
        cutebot.motors(-maxSpeed,-maxSpeed)
        cutebot.headlights(0,[0,0,0])
    elif code == button_LEFT:                   # Check to see if our code matches.
        print("Button LEFT")
        cutebot.motors(int(maxSpeed/2),maxSpeed)
        cutebot.headlights(1,[150,50,0])
        cutebot.headlights(2,[0,0,0])
    elif code == button_RIGHT:                  # Check to see if our code matches.
        print("Button RIGHT")
        cutebot.motors(maxSpeed,int(maxSpeed/2))
        cutebot.headlights(1,[0,0,0])
        cutebot.headlights(2,[150,100,0])
    elif code == button_STOP:                   # Check to see if our code matches.
        print("Button STOP")
        cutebot.motorsOff()
        cutebot.lightsOff()
    elif code == button_1:                      # Check to see if our code matches.
        print("Button 1")
        clue.play_tone(1568, 1)
    else:                                       # It does not match!
        if code != (None):
            print("I don't know: ", code)
