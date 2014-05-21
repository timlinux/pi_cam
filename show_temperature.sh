#!/bin/bash

TEMP=`python /home/pi/show_temperature.py`
DATE=`date`
echo "${DATE} : Temperature (Celcius) ${TEMP}" >> /home/pi/temperature.log
