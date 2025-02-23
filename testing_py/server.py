#!/usr/bin/env python3

from flask import Flask, request
import RPi.GPIO as GPIO



app = Flask(__name__)



# Paths for the built-in Pi LED named "ACT"

LED_TRIGGER = "/sys/class/leds/ACT/trigger"

LED_BRIGHTNESS = "/sys/class/leds/ACT/brightness"

GPIO.setmode(GPIO.BOARD)
LED_PIN = 14
GPIO.setup(LED_PIN, GPIO.OUT)


# Optionally store the default trigger so we can restore it later (often "mmc0")

DEFAULT_TRIGGER = None

with open(LED_TRIGGER, 'r') as f:

    # The line might look like: "none usb-gadget usb-host [mmc0]"

    # The bracket indicates the currently active trigger. Let's parse it out:

    line = f.read().strip()

    # We'll pick the word in brackets, if available:

    import re

    match = re.search(r"\[(.+?)\]", line)

    DEFAULT_TRIGGER = match.group(1) if match else "mmc0"



@app.route("/")

def index():

    """

    Main page with buttons for turning the LED on or off.

    """

    return """

    <h1>Raspberry Pi LED Control</h1>

    <form action="/on" method="post" style="display:inline;">

        <button>Turn ON</button>

    </form>

    <form action="/off" method="post" style="display:inline;">

        <button>Turn OFF</button>

    </form>

    <form action="/restore" method="post" style="display:inline;">

        <button>Restore Default Trigger</button>

    </form>

    """



@app.route("/on", methods=["POST"])

def led_on():

    # Disable default trigger

    GPIO.output(LED_PIN, GPIO.HIGH)
    with open(LED_TRIGGER, 'w') as f:

        f.write('none')

    # Turn the LED on

    with open(LED_BRIGHTNESS, 'w') as f:

        f.write('1')

    return """

    <p>LED turned ON.</p>

    <a href="/">Go Back</a>

    """



@app.route("/off", methods=["POST"])

def led_off():

    # Disable default trigger
    GPIO.output(LED_PIN, GPIO.LOW)

    with open(LED_TRIGGER, 'w') as f:

        f.write('none')

    # Turn the LED off

    with open(LED_BRIGHTNESS, 'w') as f:

        f.write('0')

    return """

    <p>LED turned OFF.</p>

    <a href="/">Go Back</a>

    """



@app.route("/restore", methods=["POST"])

def restore_trigger():

    # Restore the LED to the default trigger (commonly "mmc0")

    with open(LED_TRIGGER, 'w') as f:

        f.write(DEFAULT_TRIGGER)

    return f"""

    <p>LED trigger restored to '{DEFAULT_TRIGGER}'.</p>

    <a href="/">Go Back</a>

    """



if __name__ == "__main__":

    # Run on all interfaces, port 80 (you'll need sudo for port 80)
    try:
        # Run the server on port 80 and on all interfaces
        app.run(host="0.0.0.0", port=80)
    finally:
        # Clean up GPIO on exit
        GPIO.cleanup()



