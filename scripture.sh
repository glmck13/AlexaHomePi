#!/bin/ksh

URLBASE="https://mckserver.dyndns.org"
VARBASE="/var/www/html"
M3UFILE="./cdn/misc/scripture.m3u"

url=$(curl -s "https://soundcloud.com/usccb-readings/$(date +"%Y-%m-%d")-usccb-daily-mass-readings" | grep '<script>' | tr ',' '\n' | grep '^"media":')
url=${url#*:} url=${url#*:} url=${url#*:}
url=$(curl -s ${url//\"/}?client_id=td3EmUt9FTcWzOKw2nAgPrTj8XIM8WEq)
url=${url#*:} url=${url%*?}
curl -s ${url//\"/} >$VARBASE/$M3UFILE

cat - <<EOF
<html><body>
<p>Downloading $(date +"%B %d")</p>
<audio controls><source src="$URLBASE/$M3UFILE"></audio>
</body></html>
EOF
