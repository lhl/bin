#!/usr/bin/python

"""
A simple CRM114 training script that reads ham and spam from the specified
mailboxes and calls mailreaver.crm (takes advantage of the replacements,
thick/thin settings, reaver_cache, etc.)

Reads an imap.cfg file w/ a [training] section for account details
"""

import ConfigParser
import base64, email, imaplib, popen2, string, sys, time
from email.utils import parsedate
from pprint import pprint # DEBUG


### Load Settings from ConfigParser
config = ConfigParser.ConfigParser()
config.read("imap.cfg")

SERVER     = config.get("training", "server")
USER       = config.get("training", "user")
PASSWORD   = base64.b64decode(config.get("training", "password"))

# Login
server = imaplib.IMAP4(SERVER)
server.login(USER, PASSWORD)

# Select Ham Box
mailbox = config.get("training", "hambox")
resp, count = server.select(mailbox, "readonly")
resp, items = server.search(None, "ALL")
items = string.split(items[0])

ham = []
for item in items:
  resp, data = server.fetch(item, "(UID FLAGS RFC822)")
  flags = string.split(data[0][0])

  msg = email.message_from_string(data[0][1])
  msg.uid = (flags[2])
  try:
    msg.date = time.mktime(parsedate(msg.get("Date")))
  except TypeError:
    msg.date = time.mktime(parsedate(msg.get("Received").split(";")[-1]))
  msg.type = "ham"
  ham.append(msg)

print "# of Ham:   ", len(ham)

# Select Spam Box
mailbox = config.get("training", "spambox")
resp, count = server.select(mailbox, "readonly")
resp, items = server.search(None, "ALL")
items = string.split(items[0])

spam = []
for item in items:
  resp, data = server.fetch(item, "(UID FLAGS RFC822)")
  flags = string.split(data[0][0])

  msg = email.message_from_string(data[0][1])
  msg.uid = (flags[2])
  try:
    msg.date = time.mktime(parsedate(msg.get("Date")))
  except TypeError:
    msg.date = time.mktime(parsedate(msg.get("Received").split(";")[-1]))
  msg.type = "spam"
  spam.append(msg)

print "# of Spam:  ", len(spam)


# Put it together to a Corpus Box
corpus = ham + spam
print "# of Corpus:", len(corpus)

print ""


# Counters
count = { "correct_ham": 0,
          "correct_spam": 0,
          "unsure_ham": 0,
          "unsure_spam": 0,
          "wrong_ham": 0,
          "wrong_spam": 0
        }

# Date Sort and CRM this bitch
for msg in sorted(corpus, key=lambda x: x.date):
   print "Submitting msg #%3s %-6s ..." % (msg.uid, "(" + msg.type + ")"),

   # Remove CRM114 Headers
   for key in msg.keys():
     if key.startswith("X-CRM114"):
       del msg[key]

   ## DEBUG
   # pipe = popen2.Popen4("./mailreaver.crm | grep X-CRM114-Status")
   # pipe.tochild.write(msg.as_string())
   # pipe.tochild.close()
   # print pipe.fromchild.read()

   # Find status
   pipe = popen2.Popen4("./mailreaver.crm | grep X-CRM114-Status")
   pipe.tochild.write(msg.as_string())
   pipe.tochild.close()
   status = string.split(pipe.fromchild.read())
   score = status[3]
   status = status[1]
   print "%-6s (%7s) ..." % (status, score),


   # Not Sure
   if status == "UNSURE":
     if msg.type == "ham":
       pipe = popen2.Popen4("./mailreaver.crm --good | grep X-CRM114")
       pipe.tochild.write(msg.as_string())
       pipe.tochild.close()
       print "Trained as GOOD"
       count["unsure_ham"] += 1
     if msg.type == "spam":
       pipe = popen2.Popen4("./mailreaver.crm --spam | grep X-CRM114")
       pipe.tochild.write(msg.as_string())
       pipe.tochild.close()
       print "Trained as SPAM"
       count["unsure_spam"] += 1
  
   # Misclassified, is really Spam
   if status == "GOOD":
     if msg.type == "spam":
       pipe = popen2.Popen4("./mailreaver.crm --spam | grep X-CRM114")
       pipe.tochild.write(msg.as_string())
       pipe.tochild.close()
       print "INCORRECT: retrained as SPAM"
       print "  " + msg["Subject"]
       count["wrong_spam"] += 1
     else:
       print ": is GOOD"
       count["correct_ham"] += 1
  
   # Misclassified, is really Spam
   if status == "SPAM":
     if msg.type == "ham":
       pipe = popen2.Popen4("./mailreaver.crm --good | grep X-CRM114")
       pipe.tochild.write(msg.as_string())
       pipe.tochild.close()
       print "INCORRECT: retrained as GOOD"
       print "  " + msg["Subject"]
       count["wrong_ham"] += 1
     else:
       print ": is SPAM"
       count["correct_spam"] += 1

# Final Results
print ""
print "---"
print "Correctly detected HAM:             ", count['correct_ham']
print "Unsure HAM trained:                 ", count['unsure_ham']
print "Incorrectly detected HAM retrained: ", count['wrong_ham']
print ""
print "---"
print "Correctly detected SPAM:             ", count['correct_spam']
print "Unsure SPAM trained:                 ", count['unsure_spam']
print "Incorrectly detected SPAM retrained: ", count['wrong_spam']

server.logout()
