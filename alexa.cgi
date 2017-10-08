#!/bin/ksh

PATH=$PWD:$PATH

IRURL="http://askpi.home/ir.cgi"
FINGURL="http://askpi.home/fing.cgi"

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
	esac

cat - <<EOF
Content-type: text/html

<html>
<body>$Speech</body>
</html>
EOF
