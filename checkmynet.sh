#!/bin/ksh

NETRAW=/tmp/netraw.csv
NETSCAN=/tmp/netscan.csv
NETDB=/usr/local/etc/netdb.csv
ITERATIONS=10

loop=$ITERATIONS; while [ "$loop" -gt 0 ]
do
	fing -n 192.168.1.0/24 -r 1 -o log,csv,console
	(( --loop ))
done | sed -e "/>/d" -e "/^$/d" -e "s/.*[^;];;//" | sort -k1,1 -t';' | uniq >$NETRAW

join -j1 -t';' $NETRAW $NETDB >$NETSCAN
