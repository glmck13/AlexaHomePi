#!/bin/ksh

PATH=$PWD:$PATH

CHANNELS=channels.conf

[ "$REQUEST_METHOD" = "POST" ] && read -r QUERY_STRING

vars="$QUERY_STRING"
while [ "$vars" ]
do
	print $vars | IFS='&' read v vars
	[ "$v" ] && export $v
done

Script="" Response="Complete."

[[ "$OnOff" == *off ]] && ChannelName=""

if [ "$UpDown" ]; then

	case "$UpDown" in

		*up|*increase)
			Script+="; irsend SEND_START dtv KEY_VOLUMEUP"
			Script+="; sleep 2"
			Script+="; irsend SEND_STOP dtv KEY_VOLUMEUP"
			;;

		*down|*decrease)
			Script+="; irsend SEND_START dtv KEY_VOLUMEDOWN"
			Script+="; sleep 2"
			Script+="; irsend SEND_STOP dtv KEY_VOLUMEDOWN"
			;;

		*mute|*unmute)
			Script+="; irsend SEND_ONCE dtv KEY_MUTE"
			;;

	esac

	Response="Volume set."

elif [ "$ChannelName" ]; then

	channel=$(urlencode -d $ChannelName)
	channel=${channel#channel }

	if [[ "$channel" != [0-9]* ]]; then
		channel=$(grep -i -m1 "$channel" $CHANNELS)
		channel=${channel#*,}
	fi
	
	for digit in $(print $channel | grep -o .)
	do
		keys+="KEY_${digit} "
	done

	keys+="KEY_ENTER "

	Script+="; irsend SEND_ONCE dtv $keys"

	Response="Channel set."

elif [ "$OnOff" ]; then

	case "$OnOff" in

		*on)
			Script+="; irsend SEND_ONCE dynex KEY_POWER"
			Script+="; sleep 1"
			Script+="; irsend SEND_ONCE dtv KEY_POWER"
			;;

		*off)
			Script+="; irsend SEND_ONCE dynex KEY_POWER2"
			Script+="; sleep 1"
			Script+="; irsend SEND_ONCE dtv KEY_POWER2"
			;;
	esac

	Response="Power set."
fi

if [ "$Script" ]; then
	eval "$Script"
fi

cat - <<-EOF
Content-type: text/html

<html>
<body>$Response</body>
</html>
EOF
