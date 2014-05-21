"""Simple little python script to control a little toy car.

This code requires a piface board to be setup and the python digitalio libs
installed.

sudo apt-get install python{,3}-pifacedigitalio

Add this to your /etc/rc.local:

/usr/bin/python -u /home/pi/pi_car/test_car.py
"""

import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)


RED_LED_PIN = 11   # GPIO 17
GPIO.setup(RED_LED_PIN, GPIO.OUT)
GREEN_LED_PIN = 12  # GPIO 18
GPIO.setup(GREEN_LED_PIN, GPIO.OUT)
YELLOW_LED_PIN = 13  # GPIO 21
GPIO.setup(YELLOW_LED_PIN, GPIO.OUT)
#BUTTON_PIN = 6  # GND on pin 6
#GPIO.setup(BUTTON_PIN, GPIO.IN)


def wait(period):
    """Wait for a while.

    :param period: Time in ms to wait for.
    :param period: int
    """
    period /= 1000
    target_time = time.clock() + period
    while time.clock() < target_time:
        pass


def restart():
    """Restart the computer (useful if you have updated this script).

    ..note:: This script must have been run by root for this function to work.

    """
    print 'Restarting'
    command = '/usr/bin/sudo /sbin/shutdown -r now'
    import subprocess
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output = process.communicate()[0]
    print output


def halt():
    """Halt the computer (useful if you have updated this script).

    ..note:: This script must have been run by root for this function to work.

    """
    print 'Shutting down'
    command = '/usr/bin/sudo /sbin/shutdown now'
    import subprocess
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output = process.communicate()[0]
    print output


def flash_led(pin, count=2, duration=500):
    """Flash the led.

    :param pin: Pin number to flash on and off.
    :param count: Number of times to flash.
    :param duration: Length of time in ms for each flash.
    """
    for value in xrange(0, count):
        GPIO.output(pin, GPIO.HIGH)
        wait(duration)
        GPIO.output(pin, GPIO.LOW)
        wait(duration)


def switch_pressed(event):
    """When user presses wait a second then let the motor start.

    If it is button 0 (forward) or button 1 (backward) the led on pin 7 will
    be turned on.

    """
    if event.pin_num == 2:  # reboot
        # Short flash the led to show we are restarting
        flash_led(RED_LED_PIN, 5, 500)
        restart()

    elif event.pin_num == 3: # halt
        # Long flash the led to show we are shutting down
        flash_led(YELLOW_LED_PIN, 5, 500)
        halt()

    elif event.pin_num in [0, 1]:
        # Go forwards (0) or backwards (1)
        event.chip.output_pins[event.pin_num].turn_on()
        # Turn on the led on pin 7 too
        GPIO.output(GREEN_LED_PIN, GPIO.HIGH)


def switch_unpressed(event):
    """When user releases let the motor run for 25 ms then stop it."""
    wait(250)
    event.chip.output_pins[event.pin_num].turn_off()
    # Turn off the led on pin 7 after waiting an extra second
    wait(250)
    GPIO.output(GREEN_LED_PIN, GPIO.HIGH)


if __name__ == '__main__':
    # Flash the leds to show we are online
    flash_led(RED_LED_PIN, 5)
    flash_led(GREEN_LED_PIN, 5)
    flash_led(YELLOW_LED_PIN, 5)
    GPIO.cleanup()
