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
proc = subprocess.Popen ('xprintidle', shell=False, stdout=subprocess.PIPE, env=dict(os.environ, DISPLAY=":0"))
out = proc.communicate()[0]
idle_ms = int(out.strip())


### Sound check
# https://pypi.python.org/pypi/pulsectl
# equivalent to:
#   cat /proc/asound/card*/pcm*/sub*/status | grep RUNNING
#   pacmd list-sink-inputs | wc -l
proc = subprocess.Popen ('/home/lhl/bin/soundactive.py', shell=False, stdout=subprocess.PIPE, env=dict(os.environ, XDG_RUNTIME_DIR="/run/user/1000"))
# proc = subprocess.Popen (['pactl', 'info'], shell=False, stdout=subprocess.PIPE, env=dict(os.environ, XDG_RUNTIME_DIR="/run/user/1000"))
out = proc.communicate()[0]
out = out.strip()
if int(out):
  idle_ms = 0

print(idle_ms, end='')
