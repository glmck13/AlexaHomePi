#!/bin/ksh

PATH=$PWD:$PATH

IRURL="http://mckpi.home/ir.cgi"
FINGURL="http://mckpi.home/fing.cgi"
ASKPIURL="http://askpi.home/fifo.cgi"

[ "$REQUEST_METHOD" = "POST" ] && read -r QUERY_STRING

vars="$QUERY_STRING"
while [ "$vars" ]
do
	print $vars | IFS='&' read v vars
	[ "$v" ] && export $v
done

case "$Intent" in

	QueryNet)
		Speech=$(curl -s "$FINGURL?Device=$Device")
		;;

	ControlTV)
		Speech=$(curl -s "$IRURL?OnOff=$OnOff&UpDown=$UpDown&ChannelName=$ChannelName")
		;;

	AskPi)
		Speech=$(curl -s "$ASKPIURL?Trigger=$Trigger&Enum=$Enum")
		;;

	*)
		Speech="I don't know how to handle $Intent requests."
		;;
	esac

cat - <<EOF
Content-type: text/html

<html>
<body>$Speech</body>
</html>
EOF
