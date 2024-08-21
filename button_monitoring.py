from gpiozero import Button # imports button from the Pi GPIO library
import time
import os # imports OS library for Shutdown control
from main import * # This imports the main program

stopButton = Button(27) # defines the button as an object and chooses GPIO 27
restartProgram = Button(22)

while True: # infinite loop
	if stopButton.is_pressed or restartProgram.is_pressed: # Check to see if button is pressed
		time.sleep(1) # wait for the hold time we want.
		if stopButton.is_pressed: # check if the user let go of the button
			os.system("sudo shutdown now -h") # shut down the Pi -h is or -r will reset
		elif restartProgram.is_pressed:
#			pkill -9 -f automate_fermentation.py
#			time.sleep(1)
#			temp_display()
			print("this button is pressed")
#		else:
#			main()


	time.sleep(1) # wait to loop again so we don't use the processor too much.
