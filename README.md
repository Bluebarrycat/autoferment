# auto_ferment
Automatic heating control for fermentation projects.
When temp is too hot, it turns off a relay, too cold turns it back on.
Temperature sensor is controlled in separate function.

Current Problems:
-Exception capturing is untested.
-In morning sometimes, come to see it has shut down the system.  Why?
Normally in the log it would turn relay ON, and then there is a 15 minute counter.
The last item seen in the log is Turn relay on, but there is no timer issue. This could indicate a problem with the timer starting.

-Still not restarting at midnight
