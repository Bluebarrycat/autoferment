'''#!/home/brewmaster/projects/autoferment/venv/bin/python3'''

'''The purpose of this program is to take temperature readings from a DS18B20 temperature
   sensor (function), write to a file in CSV format (for export to excel), and print what is going into the
   file on an LCD screen'''

from temp_read import *  # Import the functions to handle the temp reader temp_read.py
import sys
import gpiozero
import signal
import threading
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
from RPLCD.i2c import CharLCD

RELAY_PIN = 17 # The GPIO pin the 5v relay is connected to
# create a relay object.
# Triggered by the output pin going low: active_high=False.
# Initially off: initial_value=False

relay = gpiozero.OutputDevice(RELAY_PIN, active_high=False, initial_value=True)
lcd = CharLCD(i2c_expander='PCF8574', address=0x27, port=1, cols=16, rows=2, dotsize=8) # Initialize the lcd. This code is for an LCD with an i2c piggyback.
degree_sign = chr(223) # For the degree symbol, assign this character to the "degree_sign" variable for ease of use.
MIN_TEMP = 24
MAX_TEMP = 26
stopButton = gpiozero.Button(27) # defines the button as an object and chooses GPIO 27
restartProgram = gpiozero.Button(22)

# The below function is to display the temperatures.
def temp_display():
	dev_temperature_celsius, dev_temperature_fahrenheit, = read_temp() # Calls on function "read_temp()", assigns the returned items to the corresponding variable name
	dt = datetime.datetime.now() # Assigns current date and time to the variable "dt"
	f = open("Ferment Log.txt", "a+") #a+ parameter tells open to append every time the program runs, otherwise create a new file.
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
   
def run_script():
	if stopButton.is_pressed or restartProgram.is_pressed: # check if the user let go of the button
		time.sleep(1) # wait for the hold time we want.
		if stopButton.is_pressed: # check if the user let go of the button
			os.system("sudo shutdown now -h") # shut down the Pi -h is or -r will reset
		elif restartProgram.is_pressed:
			#print("the restart program button is pressed")
			temp_display()


def do_timed_stuff():
	global t
	print("timer fired")
	t.cancel() # Just to be sure
	t = threading.Timer(15, do_timed_stuff)
	t.start() # after the timer restart to minimise drift
	
stopButton.when_pressed = run_script
restartProgram = run_script
t = threading.Timer(15, do_timed_stuff)
t.start()
run_script()

signal.pause() # this pauses your main program so nothing will happen until one of the callbacks fires.


# try:
# 	while True:
# 		temp_display()
# 		#countdown(0, 15, 0)
  
# except KeyboardInterrupt:
# 	lcd.clear()
# 	lcd.write_string("Cancelled by\n\rUser") # the "\n" moves to next line, the "\r" means to return it to beginning of current line.
    
# Inputs for hours, minutes, seconds on timer
# h = input("Enter the time in hours: ")
# m = input("Enter the time in minutes: ")
# s = input("Enter the time in seconds: ")
# countdown(int(h), int(m), int(s))


# Below is the main while loop that will run the program forever. It is within a try loop that is triggered when Ctl+c is pressed. It is clean code to capture a keyboard termination.
# try:

# 	while True:
# 		main()
# 		#temp_display()
# 		#time.sleep(900) # 15 minutes
# except KeyboardInterrupt:
# 	lcd.clear()
# 	lcd.write_string("Cancelled by\n\rUser") # the "\n" moves to next line, the "\r" means to return it to beginning of current line.
