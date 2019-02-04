#!/bin/ksh

URLBASE="https://mckserver.dyndns.org"
VARBASE="/var/www/html"
M3UFILE="./cdn/misc/scripture.m3u"

print "http://ccc.usccb.org/cccradio/NABPodcasts/$(date +"%Y/%y_%m_%d").mp3" >$VARBASE/$M3UFILE

cat - <<EOF
<html><body>
<p>Downloading $(date +"%B %d")</p>
<audio controls><source src="$URLBASE/$M3UFILE"></audio>
</body></html>
EOF
