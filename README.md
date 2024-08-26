# auto_ferment
Automatic heating control for fermentation projects.
When temp is too hot, it turns off a relay, too cold turns it back on.
Temperature sensor is controlled in separate function.

Current Problems:
-Get this to load on reboot
-get buttons working, reboot PI and refresh program
-load VENV automatically
-when using the sleep function, it locks up the code until the function is completed, so no easy way to interrupt for a program refresh.
