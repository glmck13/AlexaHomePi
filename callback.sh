#!/bin/ksh

PATH=$PATH:/usr/sbin

CONFFILE=/usr/local/etc/ringtones.conf

Name=${1:?}

grep -i "[ ,]$Name" $CONFFILE | IFS=, read Number Voice Ringtone

if [ "$Number" ]; then
	print "Dialing..."
	asterisk -x "dialplan set global CALLBACK \"<$Number>\"" >/dev/null
	asterisk -x "originate DAHDI/2/$Number extension 6000@default" >/dev/null
else
	print "No entry for $Name found in phonebook!"
fi
