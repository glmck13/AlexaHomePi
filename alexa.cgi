#!/bin/ksh

PATH=$PWD:$PATH

IRURL="http://mckpi.home/ir.cgi"
FINGURL="http://mckpi.home/fing.cgi"
ASKPICLIENTURL="http://askpi.home/fifo.cgi"
ASKPISERVERURL="http://askpi.home"

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
		curl -s "$ASKPISERVERURL?Announce=T&Speech=$Trigger+$Enum" | while read html
		do
			if [[ "$html" == @(*src=*|*href=*) ]]; then
				Speech=$(curl -s "$ASKPICLIENTURL?Trigger=$Trigger&Enum=$Enum")

			elif [[ "$html" == \<p\>*\<?p\> ]]; then
				html=${html#<p>} html=${html%</p>}
				Speech="$html"
			fi
		done
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
