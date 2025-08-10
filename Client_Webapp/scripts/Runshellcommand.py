"""Example script for toggling relay channels using shell commands."""

import os
import time

COMMAND = "/home/admin/8mosfet-rpi/8mosfet 0 write {channel} {state}"
CHANNELS = [6, 5, 4, 3, 8, 1, 2, 7]

for channel in CHANNELS:
    os.system(COMMAND.format(channel=channel, state="on"))
    time.sleep(0.5)

time.sleep(2)

for channel in CHANNELS:
    os.system(COMMAND.format(channel=channel, state="off"))
    time.sleep(0.5)
