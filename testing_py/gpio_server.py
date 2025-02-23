#!/usr/bin/env python3

from flask import Flask


app = Flask(__name__)



# Use physical pin numbering (BOARD mode) so that pin 14 is the physical pin 14.

import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
LED_PIN = 14
GPIO.setup(LED_PIN, GPIO.OUT)



@app.route("/")

def index():

    return """

    <h1>GPIO LED Control on Pin 14</h1>

    <form action="/on" method="post" style="display:inline;">

        <button type="submit">Turn LED ON</button>

    </form>

    <form action="/off" method="post" style="display:inline;">

        <button type="submit">Turn LED OFF</button>

    </form>

    """



@app.route("/on", methods=["POST"])

def led_on():

    GPIO.output(LED_PIN, GPIO.HIGH)

    return """

    <p>LED on pin 14 is now ON.</p>

    <a href="/">Back</a>

    """



@app.route("/off", methods=["POST"])

def led_off():

    GPIO.output(LED_PIN, GPIO.LOW)

    return """

    <p>LED on pin 14 is now OFF.</p>

    <a href="/">Back</a>

    """



if __name__ == "__main__":

    try:

        # Run the server on port 80 and on all interfaces

        app.run(host="0.0.0.0", port=80)

    finally:

        # Clean up GPIO on exit

        GPIO.cleanup()


