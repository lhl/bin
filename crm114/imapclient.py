#!/usr/bin/python

"""
A simple IMAP client that checks a specified account for spam and moves them
onto the CRM114 account for training/filing.  It also moves the message to the
"Deleted Message" folder that Apple Mail.app uses.

Reads an imap.cfg file w/ a [imap-crm] and [imap-usc] section for account 
details - you should change this appropriately if you use this!

You may also be interested in: 
  http://www.rogerbinns.com/isbg/
  http://rgruet.free.fr/imap.py
  http://software.place.org/mhi/browser/mhi.py
"""

import ConfigParser
import base64, email, imaplib, popen2, string, sys, time
from email.utils import parsedate
from pprint import pprint # DEBUG


### Load Settings from ConfigParser
config = ConfigParser.ConfigParser()
config.read("imap.cfg")

# USC Server
CRM_SERVER     = config.get("imap-crm", "server")
CRM_USER       = config.get("imap-crm", "user")
CRM_PASSWORD   = base64.b64decode(config.get("imap-crm", "password"))
CRM_SPAM       = config.get("imap-crm", "spam")
CRM_UNSURE     = config.get("imap-crm", "unsure")
crm = imaplib.IMAP4_SSL(CRM_SERVER)
crm.login(CRM_USER, CRM_PASSWORD)

# USC Server
USC_SERVER     = config.get("imap-usc", "server")
USC_USER       = config.get("imap-usc", "user")
USC_PASSWORD   = base64.b64decode(config.get("imap-usc", "password"))
usc= imaplib.IMAP4_SSL(USC_SERVER)
usc.login(USC_USER, USC_PASSWORD)


# Select USC Inbox
mailbox = "INBOX"
resp, count = usc.select(mailbox)
resp, items = usc.search(None, "UNSEEN")
items = string.split(items[0])

inbox = []
for item in items:
  resp, data = usc.fetch(item, "(UID RFC822)")
  flags = string.split(data[0][0])

  msg = email.message_from_string(data[0][1])
  msg.item = item
  msg.uid = (flags[2])
  try:
    msg.date = time.mktime(parsedate(msg.get("Date")))
  except TypeError:
    msg.date = time.mktime(parsedate(msg.get("Received").split(";")[-1]))
  inbox.append(msg)

# print "# of New Messages:   ", len(inbox)

# Date Sort and CRM this bitch
for msg in sorted(inbox, key=lambda x: x.date):
   # print "Submitting msg #%3s ..." % msg.uid,

   # Remove CRM114 Headers
   for key in msg.keys():
     if key.startswith("X-CRM114"):
       del msg[key]

   # Find status
   pipe = popen2.Popen4("./mailreaver.crm | grep X-CRM114-Status")
   pipe.tochild.write(msg.as_string())
   pipe.tochild.close()
   status = string.split(pipe.fromchild.read())
   score = status[3]
   status = status[1]
   # print "%-6s (%7s) ..." % (status, score), 


   # Not Sure
   if status == "UNSURE":
     # print "moved to", CRM_UNSURE
     usc.copy(msg.item, "Deleted Messages")
     crm.append(CRM_UNSURE, None, msg.date, msg.as_string())
     resp, error = usc.store(msg.item, '+FLAGS', '(\Deleted)')
     pass
   elif status == "SPAM":
     # print "moved to", CRM_SPAM
     usc.copy(msg.item, "Deleted Messages")
     crm.append(CRM_SPAM, None, msg.date, msg.as_string())
     resp, error = usc.store(msg.item, '+FLAGS', '(\Deleted)')
   else:
     # print "left as new"
     resp, error = usc.store(msg.item, '-FLAGS', '(\Seen)')

# Final Results

usc.expunge()
usc.logout()
crm.logout()
