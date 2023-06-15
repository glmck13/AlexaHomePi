#!/bin/ksh

URLBASE="https://mckspot.net:8443"
VARBASE="/var/www/html"
M3UFILE="./cdn/misc/scripture.m3u"

typeset -l today
today=$(date +"%B-%e-%Y")
today=${today// /}
today="https://soundcloud.com/usccb-readings/daily-mass-reading-podcast-for-$today"

#url=$(curl -s "https://soundcloud.com/usccb-readings/$(date +"%Y-%m-%d")-usccb-day-mass-readings" | grep '<script>' | tr ',' '\n' | grep '^"media":')
#url=$(curl -s "https://soundcloud.com/usccb-readings/$(date +"%Y-%m-%d")-usccb-year-b-mass-readings" | grep '<script>' | tr ',' '\n' | grep '^"media":')
#url=$(curl -s "https://soundcloud.com/usccb-readings/$(date +"%Y-%m-%d")-usccb-daily-mass-readings" | grep '<script>' | tr ',' '\n' | grep '^"media":')

url=$(curl -s "$today" | grep '<script>' | tr ',' '\n' | grep '^"media":')
url=${url#*:} url=${url#*:} url=${url#*:}
url=$(curl -s ${url//\"/}?client_id=LBCcHmRB8XSStWL6wKH2HPACspQlXg2P)
url=${url#*:} url=${url%*?}

curl -s ${url//\"/} >$VARBASE/$M3UFILE

cat - <<EOF
<html><body>
<p>Downloading $(date +"%B %d")</p>
<audio controls><source src="$URLBASE/$M3UFILE"></audio>
</body></html>
EOF
