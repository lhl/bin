#!/usr/bin/python

import os, re, shutil

destination_root = '/Volumes/Drobo/_incoming/_comics/_alpha/'
path = os.getcwd()

for root, dirs, files in os.walk(os.getcwd()):
  for file in files:
    firstletter = file[0].upper()

    # Numbers
    if re.search("[0-9]", firstletter):
      firstletter = "0-9"

    source = os.path.join(root, file)
    destination = os.path.join(destination_root, firstletter, file)
    try:
      # print "MOVING", source, "TO", destination
      print " MOVE", file
      print "   TO", os.path.join(destination_root, firstletter)
      shutil.move(source, destination)
      print " DONE"
      print
    except IOError:
      print "ERROR Couldn't move", source
      print "                 to", destination
      print
