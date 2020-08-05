# cutebot_IR_remote.py
# Version: 1.0
# Author(s) James Tobin

######################################################
#   Version Notes
######################################################
'''
Use any IR remote you have lying around. I used a TV remote. Follow the directions below
to find the codes for each button. You can add as many as you like. There are s
'''

######################################################
#   Import
######################################################
import board
import pulseio
import adafruit_irremote
import cutebot
from cutebot import clue


######################################################
#   Variables
######################################################
pulsein = pulseio.PulseIn(board.D16, maxlen=120, idle_state=True)       #Set Infrared (IR) pin
decoder = adafruit_irremote.GenericDecode()                             #Set infrared (IR) decoder to Adafruit's generic decoder
'''
Set each of the buttons codes to the codes for your IR remote.
To find codes, run the program with all the buttons set to None.
Afterwards, press each button and write down its code that you see on the Cluebot below.

Example:
    button_UP = [120, 85]
    button_DOWN = [127, 21]
    button_LEFT = [122, 65]
    button_RIGHT = [124, 65]
    button_STOP = [120, 65]
    button_1 = [127, 109]
'''

button_UP = [None]                       # Set the up button code
button_DOWN = [None]                     # Set the down button code
button_LEFT = [None]                     # Set the left button code
button_RIGHT = [None]                    # Set the right button code
button_STOP = [None]                     # Set the stop button code
button_1 = [None]                        # Set the button 1 code


######################################################
#   Main Code
######################################################
print("Waiting for remote signal...")
while True:
    #This first part if from the adafruit_irremote example.
    pulses = decoder.read_pulses(pulsein)                   # Stop, wait and listen for an IR signal.
    #print("Heard", len(pulses), "Pulses:", pulses)
    try:
        code = decoder.decode_bits(pulses)                  # Read the IR signal code
        #print("Decoded:", code)
    except adafruit_irremote.IRNECRepeatException:          # unusual short code!
        print("NEC repeat!")
    except adafruit_irremote.IRDecodeException as e:        # failed to decode
        print("Failed to decode: ", e.args)
    

    if code == button_UP:                       # Check to see if our code matches.
        print("Button UP")
        cutebot.motors(50,50)                                                           
        cutebot.headlights(3,[255,255,255])
    elif code == button_DOWN:                   # Check to see if our code matches.
        print("Button DOWN")
        cutebot.motors(-50,-50)
        cutebot.headlights(0,[0,0,0])
    elif code == button_LEFT:                   # Check to see if our code matches.
        print("Button LEFT")
        cutebot.motors(20,50)
        cutebot.headlights(1,[150,50,0])
        cutebot.headlights(2,[0,0,0])
    elif code == button_RIGHT:                  # Check to see if our code matches.
        print("Button RIGHT")
        cutebot.motors(50,20)
        cutebot.headlights(1,[0,0,0])
        cutebot.headlights(2,[150,100,0])
    elif code == button_STOP:                   # Check to see if our code matches.
        print("Button STOP")
        cutebot.motorsOff()
        cutebot.lightsOff()
    elif code == button_1:                      # Check to see if our code matches.
        print("Button 1")
        clue.play_tone(1568, 0.5)
    else:                                       # It does not match!
        print("I don't know: ", code)

print("========== End ==========")
