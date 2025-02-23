#!/usr/bin/env python3

import time



LED_TRIGGER = "/sys/class/leds/ACT/trigger"

LED_BRIGHTNESS = "/sys/class/leds/ACT/brightness"



def blink_led(num_blinks=5, on_time=0.5, off_time=0.5):

    # Disable the default trigger so we can manually control the LED

    with open(LED_TRIGGER, 'w') as f:

        f.write('none')



    try:

        for _ in range(num_blinks):

            # Turn LED on

            with open(LED_BRIGHTNESS, 'w') as f:

                f.write('1')

            time.sleep(on_time)



            # Turn LED off

            with open(LED_BRIGHTNESS, 'w') as f:

                f.write('0')

            time.sleep(off_time)

    finally:

        # Restore the default trigger (often 'mmc0' for the activity LED).

        # To confirm which trigger is default, run:  cat /sys/class/leds/ACT/trigger

        with open(LED_TRIGGER, 'w') as f:

            f.write('mmc0')



if __name__ == "__main__":

    blink_led()


