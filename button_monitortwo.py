#!/home/brewmaster/projects/autoferment/venv/bin/python3

from gpiozero import Button
import subprocess
from signal import pause
import sys

def restart_program():
   try:
      subprocess.run(['python3', 'main.py'])
   except KeyboardInterrupt:
      print("Exiting script...")
      sys.exit()
   finally:
      sys.exit()

restart_button = Button(27)

restart_button.when_pressed = restart_program

pause()
