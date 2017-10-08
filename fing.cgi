#!/bin/ksh

PATH=$PWD:$PATH

NETRAW=/tmp/netraw.csv
NETSCAN=/tmp/netscan.csv
NETTMP=/tmp/net$$.csv

[ "$REQUEST_METHOD" = "POST" ] && read -r QUERY_STRING

vars="$QUERY_STRING"
while [ "$vars" ]
do
print $vars | IFS='&' read v vars
[ "$v" ] && export $v
done

typeset -l Slot

Slot=$(urlencode -d ${Device:-devices})

case "$Slot" in

	user*)
		Users=$(cut -f4 -d';' $NETSCAN | sort | uniq); Users=$(print $Users)
		NumUsers=$(print $Users | wc -w)
		Response="I found ${NumUsers:-0} users on the network: ${Users// /, }.  "
		for u in $Users
		do
			devs=$(grep ";$u;" $NETSCAN | cut -f5 -d';' | sort | uniq); devs=$(print $devs)
			Response+="$u is using: ${devs// /, }.  "
		done
		;;

	device*)
		NumDevices=$(wc -l <$NETRAW)
		Users=$(cut -f4 -d';' $NETSCAN | sort | uniq); Users=$(print $Users)
		NumUsers=$(print $Users | wc -w)
		Response="I found ${NumDevices:-0} devices, and ${NumUsers:-0} users on the network: ${Users// /, }.  "
		;;

	*)
		Slot=${Slot%s}
		grep -i "$Slot" $NETSCAN >$NETTMP
		NumDevices=$(wc -l <$NETTMP)
		if [ "$NumDevices" -le 0 ]; then
			Response="I did not find any ${Slot}s on the network.  "
		else
			Users=$(cut -f4 -d';' $NETTMP | sort | uniq); Users=$(print $Users)
			NumUsers=$(print $Users | wc -w)
			Response="I found ${NumDevices:-0} ${Slot}s on the network, being used by: "
			if [ "$NumUsers" -le 0 ]; then
				Response+="everyone.  "
			else
				Response+="${Users// /, }.  "
			fi
		fi
		;;
esac

cat - <<EOF
Content-type: text/html

<html>
<body>$Response</body>
</html>
EOF

rm -f $NETTMP
