#!/bin/ksh

PATH=$PWD:$PATH

IRURL="http://mckpi.home/ir.cgi"
FINGURL="http://mckpi.home/fing.cgi"
ASKPICLIENTURL="http://askpi.home/fifo.cgi"
ASKPISERVERURL="http://askpi.home"
#ASKPICLIENTURL="http://192.168.10.1/fifo.cgi"
#ASKPISERVERURL="http://192.168.10.1"

[ "$REQUEST_METHOD" = "POST" ] && read -r QUERY_STRING

vars="$QUERY_STRING"
while [ "$vars" ]
do
	print $vars | IFS='&' read v vars
	[ "$v" ] && export $v
done

case "$Intent" in

	QueryNet)
		Response=$(curl -s "$FINGURL?Device=$Device")
		;;

	ControlTV)
		Response=$(curl -s "$IRURL?OnOff=$OnOff&UpDown=$UpDown&ChannelName=$ChannelName")
		;;

	AskPi)
		Response=$(curl -s "$ASKPISERVERURL?Announce=T&Speech=Alexa+$Trigger+$Enum")
		;;

	*)
		Response="<html><body><p>I don't know how to handle $Intent requests.</p></body></html>"
		;;
	esac

cat - <<EOF
Content-type: text/html

$Response
EOF
