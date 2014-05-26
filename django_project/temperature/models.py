
"""Temperature recording app models."""

import time
import glob
from django.db import models


# Create your models here.

class Temperature(models.Model):
    """Temperature.

    This class represents a temperature at a given time.
    """
    timestamp = models.DateTimeField(auto_now=True, auto_now_add=True)
    temperature = models.FloatField(default=0, null=True, blank=True)
    host = models.CharField(
        max_length=50,
        help_text='Host name on which this temperature was recorded.',
        blank=False,
        null=True)

    def __init__(self, *args, **kwargs):
        super(Temperature, self).__init__(*args, **kwargs)
        if not self.pk:
            self.temperature = Temperature.get_temperature()

    @classmethod
    def get_temperature(cls):
        """Get the temperature from the pi w1 interface.

        :returns: Current temperature in degrees Celcius.
        :rtype: float
        """
        lines = cls.read_temp_raw()
        while lines[0].strip()[-3:] != 'YES':
            time.sleep(0.2)
            lines = cls.read_temp_raw()
        equals_pos = lines[1].find('t=')
        if equals_pos != -1:
            temp_string = lines[1][equals_pos+2:]
            temp_c = float(temp_string) / 1000.0
            return temp_c

    @classmethod
    def read_temp_raw(cls):
        """Read the temperature from the raw w1 device."""
        base_dir = '/sys/bus/w1/devices/'
        device_folder = glob.glob(base_dir + '10*')[0]
        device_file = device_folder + '/w1_slave'
        f = open(device_file, 'r')
        lines = f.readlines()
        f.close()
        return lines
