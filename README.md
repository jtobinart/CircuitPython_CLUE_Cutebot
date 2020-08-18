# CircuitPython-CLUE-Cutebot
[![CircuitPython_CLUE_Cutebot YouTube Video](https://github.com/jisforjt/CircuitPython_CLUE_Cutebot/blob/master/docs/images/Cutebot_YouTube_Still.png)](https://youtu.be/jVEu-UyjuIc)

This is a higher-level library to allow Adafruit's [CLUE](https://www.adafruit.com/product/4500) and ElecFreak's micro:bit Smart [Cutebot](https://www.elecfreaks.com/micro-bit-smart-cutebot.html) to communicate while maintaining all the functionality of the CLUE, except for touch features. I am a teacher of young learners and as such the code was purposefully left simple so I can use it with them. There is also a comment on nearly every line to help explain to my students what each line is doing.

## Dependencies
This library depends on:
* [Adafruit CircuitPython](https://github.com/adafruit/circuitpython)
* [Adafruit_hcsr04](https://github.com/adafruit/Adafruit_CircuitPython_HCSR04)

The IR remote example also depends on:
* [Adafruit_irremote](https://github.com/adafruit/Adafruit_CircuitPython_IRRemote)

The Adafruit BlueFruit Connect App's Controller example also depends on:
* [Adafruit_ble](https://github.com/adafruit/Adafruit_CircuitPython_BLE)
* [Adafruit_bluefruit_connect](https://github.com/adafruit/Adafruit_CircuitPython_BluefruitConnect)

## Instalations
Follow Adafruit's [CLUE Overview](https://learn.adafruit.com/adafruit-clue) instructions under _CircuitPython on CLUE_. During the installation process, you will download the latest _library bundle_ and transfer several libraries to the CLUE. Transfer the dependencies listed above as well to the _lib folder_.
Download this repository and copy _cutebot.mpy_ and _cutebot_adafruit_clue.mpy_ over to your drive CIRCUITPY. The _.mpy_ version of the files use a quarter to a third less memory.

## Usage
You can create a new main.py file and use:
```python
import cutebot
from cutebot import clue
```
to access the CLUE and Cutebot or you can use one of the examples programs provided in the repository. Use the IR remote example to easily learn about IR signals and control your Cutebot in a snap. Download Adafruit's BlueFruit Connect app and control your Cutbot over Bluetooth. These examples and more are located in the _examples_ folder.

## License
The code of the repository is made available under the terms of the MIT license. See license.md for more information.
