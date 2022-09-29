# CircuitPython Clue Cutebot
# Last Updated: Sep. 27, 2022
# Version 3.0
# Author(s): James Tobin

######################################################
#   MIT License
######################################################
'''
Copyright (c) 2020 James Tobin
Permission is hereby granted, free of charge, to any person obtaining a copy of this
software and associated documentation files (the "Software"), to deal in the Software
without restriction, including without limitation the rights to use, copy, modify,
merge, publish, distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to the following
conditions:
The above copyright notice and this permission notice shall be included in all copies
or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR
PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE
OR OTHER DEALINGS IN THE SOFTWARE.
'''

######################################################
#   Cutebot Information
######################################################
'''
cutebot.py:
v3
    Updated to work with Circuit Python 7.x. Adafruit Clue class has been seperated again.
v2
    Refined and more efficient code. Clue class now included in file.
v1
    This is a higher-level library to allow Adafruit's CLUE and ElecFreak's micro:bit 
    Smart Cutebot to communicate while maintaining all the functionality of the CLUE, 
    except for touch features.
'''

######################################################
#   Pin Reference
######################################################
"""
Pins
    P0  -Digital    Cutebot Buzzer
    P1  -Analog     Cutebot P1 Sensor input (P1 3V G)
    P2  -Analog     Cutebot P2 Sensor input (P2 3V G)
    P5  -Digital    Clue Button A
    P8  -Digital    Cutebot ultrasonic pulse transmitter (2cm-400cm, precision +-1.5mm)
    P11 -Digital    Clue Button B
    P12 -Digital    Cutebot ultrasonic pulse receiver
    P13 -Digital    Cutebot left line tracking
    P14 -Digital    Cutebot right line tracking
    P15 -Digital    Cutebot Neopixel
    P16 -Digital    Cutebot Infrared Control
    P17 -Digital    Clue LED
    P18 -Digital    Clue Neopixel
    P19 -Digital    Shared i2c Port G V P19 P20
    P20 -Digital    Shared i2c Port G V P19 P20
    P43 -Digital    Clue White LEDs
"""


######################################################
#   Import
######################################################
import time
import board
import busio
import pwmio
import neopixel
from digitalio import DigitalInOut, Direction, Pull
from analogio import AnalogIn
import adafruit_hcsr04

class Cutebot:

    def __init__(self):
        # Define i2c
        #self._i2c = busio.I2C(board.SCL, board.SDA, frequency = 100000)
        self._i2c = board.I2C()
        self._cutebot = 0x10
        self._i2c_rest = 0.1
        self._error_thresh = 12

        # Define sound
        self._buzzer = pwmio.PWMOut(board.P0, variable_frequency=True)

        # Define headlights
        self._RGB_RIGHT_HEADLIGHT = 0x04
        self._RGB_LEFT_HEADLIGHT = 0X08

        # Define neopixels
        self._rainbow_pixels = neopixel.NeoPixel(board.D15, 2)

        # Define motor states
        self._LEFT_MOTOR = 0x01
        self._RIGHT_MOTOR = 0x02
        self._BACKWARDS = 0x01
        self._FORWARDS = 0x02

        # Define servo
        self._servoMaxAngleInDegrees = 180
        self._SERVO_S1 = 0x05 
        self._SERVO_S2 = 0x06

        # Define expansion pins
        self._p1 = AnalogIn(board.P1)
        self._p2 = AnalogIn(board.P2)
        
        # Define ultrasound sonar 
        self._sonar = adafruit_hcsr04.HCSR04(trigger_pin=board.D8, echo_pin=board.D12)
        
        # Define line tracking sensors
        # Left sensor
        self._leftLineTracking = DigitalInOut(board.D13)
        self._leftLineTracking.direction = Direction.INPUT
        self._leftLineTracking.pull = None
        # Right sensor
        self._rightLineTracking = DigitalInOut(board.D14)
        self._rightLineTracking.direction = Direction.INPUT
        self._rightLineTracking.pull = None

        # Reset cutebot
        self.motorsOff()
        self.lightsOff()


    ######################################################
    #   Sounds
    ######################################################
    def playTone(self, tone, duration):
        '''
        Plays a tone for a set duration.

        tone (integer) =  the frequency of the tones/music notes you want to play
        duration (float) = the number of seconds you want to play the tone
         
            tone     music note
            262    =     C4
            294    =     D4
            330    =     E4
            349    =     F4
            392    =     G4
            440    =     A4
            494    =     B4

        examples:
            playTone(294, 0.5)
            playTone(349, 1.0)
            playTone(440, 2.2)
        '''
        self._buzzer.frequency = tone
        self._buzzer.duty_cycle = 2**15
        time.sleep(duration)        
        self._buzzer.duty_cycle = 0


    ######################################################
    #   Lights
    ######################################################
    def headlights(self, whichLight, colors):
        '''
        Control the headlights.

        whichLight (integer):
            0 = Set both lights to off
            1 = Set left light only
            2 = Set right light only
            3 = Set both lights

        colors - RGB (array of three integers):
            colors[0] = red
            colors[1] = green
            colors[2] = blue

        examples:
            black = [0, 0, 0]
            white = [255, 255, 255]
            pink = [255, 192, 203]
            red = [255, 0, 0]
            headlights(0, black)          # turns off the headlights
            headlights(1, pink)           # sets the left headlight to pink
            headlights(2, red)            # sets the right headlight to red
            headlights(3, [80, 255, 80])  # sets both headlights to a light green color
        '''
        while not self._i2c.try_lock():
            pass
        error_count = 0
        while True:
            try:
                red, green, blue = colors
                r = int(min(max(red, 0),255))
                g = int(min(max(green, 0),255))
                b = int(min(max(blue, 0),255))
                if whichLight == 0:
                    data = [self._RGB_LEFT_HEADLIGHT, 0, 0, 0]
                    self._i2c.writeto(self._cutebot, bytes(data))
                    data[0] = self._RGB_RIGHT_HEADLIGHT    
                    self._i2c.writeto(self._cutebot, bytes(data))
                elif whichLight == 1:
                    data = [self._RGB_RIGHT_HEADLIGHT, r, g, b] 
                    self._i2c.writeto(self._cutebot, bytes(data))
                elif whichLight == 2: 
                    data = [self._RGB_LEFT_HEADLIGHT, r, g, b]
                    self._i2c.writeto(self._cutebot, bytes(data))
                elif whichLight == 3:
                    data = [self._RGB_LEFT_HEADLIGHT, r, g, b]
                    self._i2c.writeto(self._cutebot, bytes(data))
                    data[0] = self._RGB_RIGHT_HEADLIGHT
                    self._i2c.writeto(self._cutebot, bytes(data))
                break
            except:
                error_count += 1
                if error_count > self._error_thresh:
                    print('HEADLIGHTS: i2c ERROR')
                    break
        self._i2c.unlock()
        time.sleep(self._i2c_rest)

    def pixels(self, whichLight, colors):
        '''
        Controls your two neopixels.

        whichLight (integer):
            0 = Set both lights to off
            1 = Set left light only
            2 = Set right light only
            3 = Set both lights

        colors - RGB (array of three integers):
            colors[0] = red
            colors[1] = green
            colors[2] = blue

        examples:
            black = [0, 0, 0]
            white = [255, 255, 255]
            pink = [255, 192, 203]
            red = [255, 0, 0]
            headlights(0, black)           # turns off the neopixels
            headlights(1, pink)            # sets the left neopixel to pink
            headlights(2, red)             # sets the right neopixel to red
            headlights(3, [80, 255, 80])   # sets both neopixels to a light green color
        '''
        red, green, blue = colors
        r = int(min(max(red, 0),255))
        g = int(min(max(green, 0),255))
        b = int(min(max(blue, 0),255))
        if whichLight == 0: 
            self._rainbow_pixels[0] = (0, 0, 0)
            self._rainbow_pixels[1] = (0, 0, 0)
        elif whichLight == 1:
            self._rainbow_pixels[0] = (r, g, b)
        elif whichLight == 2:
            self._rainbow_pixels[1] = (r, g, b)
        elif whichLight == 3:
            self._rainbow_pixels[0] = (r, g, b)
            self._rainbow_pixels[1] = (r, g, b)

    def lightsOff(self):
        self.headlights(0,[0,0,0])
        self.pixels(0, [0,0,0])


    ######################################################
    #   Motors
    ######################################################
    def motors(self, leftSpeed, rightSpeed):      # set motors speeds
        '''
        leftSpeed = the speed of the left motor (integer between -100 and 100)
        rightSpeed = the speed of the right motor (integer between -100 and 100)

        examples:
            motors(50, 20)      # sets cutebot's motors so it turns right slowly
            motors(-100, 100)   # sets cutebot's motors so it spins counter-clockwise
            motors(-50, -50)    # sets cutebot's motors so it backs up at about half speed
        '''
        while not self._i2c.try_lock():
            pass
        error_count = 0
        while True:
            try:
                leftSpeed = int(min(max(leftSpeed, -100),100))
                rightSpeed = int(min(max(rightSpeed, -100),100))
                # Stop motors
                if leftSpeed == 0 and rightSpeed == 0:
                    data = [self._LEFT_MOTOR, self._FORWARDS, 0, 0]
                    self._i2c.writeto(self._cutebot, bytes(data))
                    data[0] = self._RIGHT_MOTOR
                    self._i2c.writeto(self._cutebot, bytes(data))
                # Left motor
                if leftSpeed > 0:
                    data = [self._LEFT_MOTOR, self._FORWARDS, leftSpeed, 0]
                    self._i2c.writeto(self._cutebot, bytes(data))
                else:
                    data = [self._LEFT_MOTOR, self._BACKWARDS, (leftSpeed * -1), 0]
                    self._i2c.writeto(self._cutebot, bytes(data))
                # Right motor
                if rightSpeed > 0:
                    data = [self._RIGHT_MOTOR, self._FORWARDS, rightSpeed, 0]
                    self._i2c.writeto(self._cutebot, bytes(data))
                else:
                    data = [self._RIGHT_MOTOR, self._BACKWARDS, (rightSpeed * -1), 0]
                    self._i2c.writeto(self._cutebot, bytes(data))
                break
            except:
                error_count += 1
                if error_count > self._error_thresh:
                    print('MOTOR: i2c ERROR')
                    break
        self._i2c.unlock()
        time.sleep(self._i2c_rest)

    def motorsOff(self):
        self.motors(0,0)     # stop motors


    ######################################################
    #   Servos
    ######################################################
    def servos(self, whichServo, angleInDegrees):     # set servos angles
        '''
        whichServo:
            1 = S1 Servo (0x05)
            2 = S2 Servo (0x06)
            3 = S1 and S2 Servos

        examples:
            servos(1, 90)       #Sets Servo S1 to 90 degrees
            servos(2, 120)      #Sets Servo S2 to 120 degrees
            servos(3, 180)      #Sets Servo S1 and S2 to 180 degrees
        '''
        while not self._i2c.try_lock():
            pass
        error_count = 0
        while True:
            try:
                angleInDegrees = int(min(max(angleInDegrees, 0),self._servoMaxAngleInDegrees))
                if whichServo == 1:
                    data = [self._SERVO_S1, angleInDegrees, 0, 0]
                    self._i2c.writeto(self._cutebot, bytes(data))
                elif whichServo == 2:
                    data = [self._SERVO_S2, angleInDegrees, 0, 0]
                    self._i2c.writeto(self._cutebot, bytes(data))
                elif whichServo == 3:
                    data = [self._SERVO_S1, angleInDegrees, 0, 0]
                    self._i2c.writeto(self._cutebot, bytes(data))
                    data[0] = self._SERVO_S2
                    self._i2c.writeto(self._cutebot, bytes(data))
                break
            except:
                error_count += 1
                if error_count > self._error_thresh:
                    print('SERVO: i2c ERROR')
                    break
        self._i2c.unlock()
        time.sleep(self._i2c_rest)

    def centerServos(self):
        self.servos(3,(self._servoMaxAngleInDegrees/2))


    ######################################################
    #   Sensors
    ######################################################
    @property
    def p1(self):
        return self._p1.value

    @property
    def p2(self):
        return self._p2.value

    @property
    def sonar(self):
        '''
        Output: the distance in centimeters between the cutebot and an object in front of it
        '''
        timeoutCount = 0
        data = []
        while len(data) < 3:
            try:
                data.append(self._sonar.distance)
            except RuntimeError:
                #print("*** SONAR ERROR ***")
                timeoutCount += 1
                if timeoutCount > 8:
                    print("SONAR: CONNECTION ERROR")
                    return 0.00
            time.sleep(0.025)
        distance = sum(data) - min(data) - max(data)
        return distance

    @property
    def tracking(self):
        '''
        Output: left driver side sensor, right driver side sensor

        True = I see black
        False = I see white
        '''
        return not self._leftLineTracking.value, not self._rightLineTracking.value


cutebot = Cutebot()