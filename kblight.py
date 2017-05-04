#!/usr/bin/python

import math
import subprocess
import sys

# Custom Ramp
increments = [ 
                 0,
                 2,
                 5,
                10,
                20,
                30,
                40,
                50,
                60,
                70,
                80,
                90,
               100,
             ]

try:
  direction = sys.argv[1]
except:
  direction = 'show'

# Get Current
popen = subprocess.Popen(('/usr/bin/xbacklight'), stdout=subprocess.PIPE)
popen.wait()
backlight = int(round(float(popen.stdout.read().strip())))

if direction == 'show':
  print(backlight)
  sys.exit()

if direction == 'up':
  if backlight == 100:
    sys.exit()
  while len(increments):
    x = increments.pop(0)
    if x > backlight:
      popen = subprocess.Popen(('/usr/bin/xbacklight', '-set',  '%s' % x))
      break

elif direction == 'down':
  if backlight == 0:
    sys.exit()
  while len(increments):
    x = increments.pop()
    if x < backlight:
      popen = subprocess.Popen(('/usr/bin/xbacklight', '-set',  '%s' % x))
      break
