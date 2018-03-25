#!/usr/bin/python

from   pulsectl import Pulse

### Sound check
# https://pypi.python.org/pypi/pulsectl
# equivalent to:
#   cat /proc/asound/card*/pcm*/sub*/status | grep RUNNING
#   pacmd list-sink-inputs | wc -l
try:
  pulse = Pulse('sleep-if-idle')
  if len(pulse.sink_input_list()):
    active = 1
  else:
    active = 0
except:
  active = 0
print(active, end='')
