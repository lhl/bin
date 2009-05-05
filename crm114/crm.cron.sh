#!/bin/bash

# See: http://andrew.mcmillan.net.nz/blog/crm114_awesomeness

for SPAM in /home/lhl/Maildir/._crm114.train-spam/cur/*; do
  [ ! -f "${SPAM}" ] && break
  /usr/bin/crm -u /home/lhl/crm114 --spam mailreaver.crm <"${SPAM}" >/dev/null
  # /usr/bin/crm -u /home/lhl/crm114 --spam mailreaver.crm <"${SPAM}" | grep X-CRM114
  mv "${SPAM}" /home/lhl/Maildir/._crm114.corpus-spam/cur
done

for HAM in /home/lhl/Maildir/._crm114.train-ham/cur/*; do
  [ ! -f "${HAM}" ] && break
  /usr/bin/crm -u /home/lhl/crm114 --good mailreaver.crm <"${HAM}" >/dev/null
  # /usr/bin/crm -u /home/lhl/crm114 --good mailreaver.crm <"${HAM}" | grep X-CRM114
  mv "${HAM}" /home/lhl/Maildir/._crm114.corpus-ham/cur
done
