Some simple (probably nowhere near optimal!) code to run an APA102 RGB LED strip.

All the hard work explaining how to use this LED strip is taken from this great youtube video: https://youtu.be/UYvC-hukz-0

My python code is pretty awful, but it works, so that's good enough for me :)

Features:

- LED strip data channel driven from the GPIO port on a RaspberyPi
- Simple code to send the relevant serial outputs using python
- Small wrapper to run the code as a daemon which can then be controlled from the command line to set and change patterns
- Simple web GUI using Flask so you can control the LEDs from a web gui (on a phone, tablet or laptop)


## Installing ##

To install, clone this repository into the home directory of your "pi" user (/home/pi):

```
git clone https://github.com/ahatherly/led-strip-pi.git
```

You can try it out directly from the command line:

```
cd led-strip-pi
./led.sh start
```

You can stop it again using:

```
./led.sh stop
```

## Starting the web gui on boot ##

You'll need to install green unicorn into your python environment (for the root user):

```
sudo pip install gunicorn
```

Now, you can add the below lines into /etc/rc.local to start the web server at boot:

```
# Start LED Web GUI
cd /home/pi/led-strip-pi && gunicorn --daemon --bind 0.0.0.0:80 wsgi
```

