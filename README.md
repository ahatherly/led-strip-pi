Some simple (probably nowhere near optimal!) code to run an APA102 RGB LED strip.

All the hard work explaining how to use this LED strip is taken from this great youtube video: https://youtu.be/UYvC-hukz-0

My python code is pretty awful, but it works, so that's good enough for me :)

Features:

- LED strip data channel driven from the GPIO port on a RaspberyPi
- Simple code to send the relevant serial outputs using python
- Small wrapper to run the code as a daemon which can then be controlled from the command line to set and change patterns
- Simple web GUI using Flask so you can control the LEDs from a web gui (on a phone, tablet or laptop)

