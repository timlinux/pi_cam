# Simple test to flash each port in turn

import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)


def print_message(text):
    """Print a number in big letters using figlet.

    ..note:: sudo apt-get

    :param text: Text or number to print.

    """
    print '\n\n'
    command = 'figlet %s' % text
    import subprocess
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output = process.communicate()[0]
    print output
    print '\n\n'

works = []
for pin in [17, 18, 27]:
    try:
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, GPIO.HIGH)
        works.append(pin)
        print_message('Pin %i works' % pin)
        time.sleep(1)
    except:
        print_message('Pin %i FAILED' % pin)


for pin in works:
    GPIO.output(pin, GPIO.LOW)

# Now button test

GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_UP)


def show_message(channel):

    print_message('Button on IO %s pressed!' % channel)

GPIO.add_event_detect(24, GPIO.FALLING, callback=show_message, bouncetime=300)

while True:
    time.sleep(1)

GPIO.cleanup()
