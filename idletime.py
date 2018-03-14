#!/usr/bin/python

'''
This script uses:

xprintidle
python: pulsectl

to report how long the computer has been idle
'''


import os
import psutil
from   pulsectl import Pulse
import subprocess
import sys
import time


idle_ms = 0

### Get idle time
proc = subprocess.Popen ('xprintidle', shell=False, stdout=subprocess.PIPE)
out = proc.communicate()[0]
idle_ms = int(out.strip())


### Sound check
# https://pypi.python.org/pypi/pulsectl
# equivalent to:
#   cat /proc/asound/card*/pcm*/sub*/status | grep RUNNING
#   pacmd list-sink-inputs | wc -l
pulse = Pulse('sleep-if-idle')
if len(pulse.sink_input_list()):
  idle_ms = 0

print(idle_ms, end='')
