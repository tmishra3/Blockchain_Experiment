from Box import File, Box
import os
import time

box = Box(1)
box += 'Kalimba.mp3'

print(box)
#box.bundle()

#box.dump()

##########################################
inputPause = input("Pause. Press Enter.")#
##########################################


box -= 'Kalimba.mp3'