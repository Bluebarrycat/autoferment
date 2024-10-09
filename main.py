
'''The purpose of this program is to take temperature readings from a DS18B20 temperature
   sensor (function), write to a file in CSV format (for export to excel), and print what is going into the
   file on an LCD screen'''

from temp_read import *  # Import the functions to handle the temp reader temp_read.py
import sys
import gpiozero
import signal
import threading
import logging
import os
# The os library allows you to interact with the operating system, and in this code, it's used to
# execute system commands (os.system) to load the required kernel modules for 1one-wire
# communication with the DS18B20 sensor.

import glob
# The glob library helps find files or directories that match a specific pattern, and it's used here to
# locate the directory representing the DS8B20 sensor based on its unique address prefix.
import time

# The time library is used to introduce delays in the code to give enough time for the sensor to get
# valid readings.

import datetime
from RPLCD.i2c import CharLCD # This import will require a virtual environment

RELAY_PIN = 17 # The GPIO pin the 5v relay is connected to
# create a relay object.
# Triggered by the output pin going low: active_high=False.
# Initially off: initial_value=False

relay = gpiozero.OutputDevice(RELAY_PIN, active_high=False, initial_value=True)
lcd = CharLCD(i2c_expander='PCF8574', address=0x27, port=1, cols=16, rows=2, dotsize=8) # Initialize the lcd. This code is for an LCD with an i2c piggyback.
degree_sign = chr(223) # For the degree symbol, assign this character to the "degree_sign" variable for ease of use.

MIN_TEMP = 25 # Kombucha Changed from 24 to 25.
MAX_TEMP = 26 # Kombucha

# MIN_TEMP = 23 # Water Kefir
# MAX_TEMP = 24 # Water Kefir

stopButton = gpiozero.Button(27) # defines the button as an object and chooses GPIO 27
restartProgram = gpiozero.Button(22)

# Logging
#Set up the basic configuration for logging
logging.basicConfig(filename='log_running.txt', level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Log messages of various severity levels
logging.debug('This is a debug message')
logging.info('This is an info message')
logging.warning('This is a warning message')
logging.error('This is an error message')
logging.critical('This is a critical message')

# The below function is to display the temperatures.
def temp_display():
	dev_temperature_celsius, dev_temperature_fahrenheit, = read_temp() # Calls on function "read_temp()", assigns the returned items to the corresponding variable name
	dt = datetime.datetime.now() # Assigns current date and time to the variable "dt"
	f = open("/home/brewmaster/projects/autoferment/logs/Kombucha_log.txt", "a+") #a+ parameter tells open to append every time the program runs, otherwise create a new file.
	toWrite = dt.strftime("%m/%d/%Y,%H:%M:%S") + ",Temperature:," + str(dev_temperature_celsius) + "," + str(dev_temperature_fahrenheit)
	# This above string is created and assigned to the variable toWrite.
	f.write(toWrite + "\n")
	f.close()
	lcd.clear() # clears the lcd
	lcd.write_string(f'Temp: {dev_temperature_celsius:.2f}{degree_sign}C')

	if dev_temperature_celsius <= MIN_TEMP:
		# I want to turn on the heat now.
		relay.on()
		print("Power on ",dev_temperature_celsius)
	else:
		if dev_temperature_celsius >= MAX_TEMP:
			relay.off()
			print("Power off ",dev_temperature_celsius)

def shutdown_system():
	lcd.clear()
	lcd.write_string("Shutting down\n\rSystem")
	os.system("sudo shutdown now -h") # shut down the Pi -h is or -r will reset

def restart_program():
	temp_display()


def do_timed_stuff():
	global t
	print("timer fired")
	temp_display()
	t.cancel() # Just to be sure
	t = threading.Timer(900, do_timed_stuff) # 900 seconds = 15 minutes
	t.start() # after the timer restart to minimise drift

try:
	stopButton.when_pressed = shutdown_system
	restartProgram.when_pressed = restart_program

	t = threading.Timer(900, do_timed_stuff) # 900 seconds = 15 minutes
	t.start()
	temp_display()

	signal.pause() # this pauses your main program so nothing will happen until one of the callbacks fires.
except KeyboardInterrupt:
	lcd.clear()
	lcd.write_string("Cancelled by\n\rUser")  # the "\n" moves to next line, the "\r" means to return it to beginning of current line.
