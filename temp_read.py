'''The purpose of this script is to take temperature readings from a DS18B20 temperature
   sensor, then have the function return the temperature in F and Celcius'''

import sys
import gpiozero
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
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
# Next, load the above kernel modules (w1-gpio and w1-therm) to interface with the DS18B20
# sensor via one-wire communication protocol. These commands use the os.system function to
# execute shell commands within Python

# The below lines set up paths and filenames for reading the temperature data.
base_dir = '/sys/bus/w1/devices/'
# base_dir represents the directory where the one-wire devices are located under the
# /sys filesystem.

device_folder = glob.glob(base_dir + '28-3ce1e3809a4e')[0]
# device_folder is obtained using the glob.glob function, which searches for directories
# matching the pattern '28*'. The DS18B20 sensors typically have a unique address starting
# with 28. This ensures that the code finds the correct folder representing the DS18B20
# sensor connected to the Raspberry Pi. Remember, everything in Linux is a file structure.

device_file = device_folder + '/w1_slave'
# device_file represents the path to the w1_slave file that contains the raw temperature data.

'''The below function read_temp_raw() gets the temperature readings from the w1_slave file (that's the
place where those are stored). This function opens the w1_slave file, reads its contents line by
line, and then returns a list containing the lines.
To see what is in the w1_slave file you would navigate to it's directory and type: cat w1_slave
It then lists two lines with numbers and letters. There are two important items:
	crc=fe YES(can also say NO - this is the temp status)
		and
	t=24062 (which is the temperature)'''

def read_temp_raw():
	# assign to variable g, to open appropriate file. 'r' makes it open and read file
	g = open(device_file, 'r')
	lines = g.readlines()
	g.close() # Always close your files
	return lines

# The read_temp() function reads the temperature data.
def read_temp():
	lines = read_temp_raw()

	while lines[0].strip()[-3:] != 'YES': # Checks in lines variable the first line (0), removes all whitespace (.strip()), checks the last 3 digits to see if they are YES or NO #
		time.sleep(0.2)
		lines = read_temp_raw()
	equals_pos = lines[1].find('t=') # searches line 2(yes, 1=line 2) until t=, returns value up until =t which is 27 usually.
	if equals_pos != -1:
		temp_string = lines[1][equals_pos+2:] # this takes 'lines' line 2, takes equal_pos(27), adds two (29), and assigns everying after postion 29 to the variable temp_string, which is the temperature.
		temp_c= round((float(temp_string) / 1000.0), 2)
		temp_f = round((temp_c * 9.0 / 5.0 + 32.0), 2)

	return temp_c, temp_f

# The above function then extracts the temperature value from the second line after t= and converts it to Celsius (temp_c) and Fahrenheit (temp_f).
# It returns both temperature values. We need to divide by 1000 to get the temperature in Celsius degrees. Then we convert that value to fahrenheit.