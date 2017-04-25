#!/usr/bin/python

'''
If you run Arch, it doesn't come w/ a suspend timer by default. Oops.
However, since it's Lunix we can do a bit better

Put this in ~/.config/openbox/autostart

  xautolock -detectsleep -time 10 -locker /home/lhl/bin/sleep-if-idle.py -notify 60 -notifier 'notify-send -u critical -t 10000 "SLEEP in 60s"' &

This script will:
  * IGNORED: do an AC check
  * Check if sound is in use (presumably video watching will trigger this and it's slightly cleaner than looking for full screen apps)
  * Look for specific processes running: rsync, scp, cp, mv
  * Look for file read/write greater than 2MB - should cover nonslow writes w/ Thunar and anything else missed


See also: http://rabexc.org/posts/awesome-xautolock-battery
'''


import psutil
from pulsectl import Pulse
import subprocess
import sys
import time


SHOULD_SLEEP = 1


### AC check
'''
if open('/sys/class/power_supply/AC/online').read().strip() == '1':
  print('ac')
  SHOULD_SLEEP = 0
'''


### Sound check
# https://pypi.python.org/pypi/pulsectl
# equivalent to:
#   cat /proc/asound/card*/pcm*/sub*/status | grep RUNNING
#   pacmd list-sink-inputs | wc -l
pulse = Pulse('sleep-if-idle')
if len(pulse.sink_input_list()):
  print('sound')
  SHOULD_SLEEP = 0


### Disk I/O Check
# we're just using psutil
# https://pythonhosted.org/psutil/
# iostat -k
# https://www.kernel.org/doc/Documentation/ABI/testing/procfs-diskstats
# [5] sectors read
# [9] sectors written
# [11] ios currently in progress
# https://gist.github.com/mmalone/1081615/a37b09ce1d6ac6960742444c50f99728bffc9859
# https://gist.github.com/mmalone/1081615
# diskstats = open('/proc/diskstats').readline().split()
'''
http://unix.stackexchange.com/questions/225095/how-to-get-total-read-and-write-iops-in-linux

pidstat -d 2 5 | grep 1000 <-- gives user over 5s
overall we can't reliably see when disk is being used
doesn't help that file copying seems to be intermittent
'''
# Process Check
busy_procs = ['rsync', 'scp', 'cp', 'mv', 'pacaur', 'wget', 'curl', 'youtube-dl']
for proc in psutil.process_iter():
  if proc.name() in busy_procs:
    SHOULD_SLEEP = 0
    break

# File I/O check
diskio1 = psutil.disk_io_counters()
time.sleep(1)
diskio2 = psutil.disk_io_counters()
read = diskio2.read_bytes - diskio1.read_bytes
write = diskio2.write_bytes - diskio1.write_bytes

# > 2MB read/write, works w/ thunar well
io = read + write
if read+write > 2000000:
  SHOULD_SLEEP = 0


### DEBUG
# print(SHOULD_SLEEP)
# sys.exit()


### FINALLY, do we sleep?
if not SHOULD_SLEEP:
  subprocess.call(['xautolock', '-restart'])
else:
  subprocess.call(['systemctl', 'suspend'])
