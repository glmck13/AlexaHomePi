#!/bin/ksh

URLCDN="https://mckserver.dyndns.org/cdn/candle"
VARCDN="/var/www/html/cdn/candle"
CANDLEDB="$VARCDN/candledb.csv"

Current=$(wc -l <$CANDLEDB)
if [ "$Current" -eq 0 ]; then
	Speech="No candles are currently lit. "
elif [ "$Current" -eq 1 ]; then
	Speech="$Current candle is currently lit. "
else
	Speech="$Current candles are currently lit. "
fi

Audio=""

LastSeen=$(grep "^$User," $CANDLEDB)

if [ "$Intent" = "GetCandleStats" ]; then
	:

elif [ "$Intent" = "BlowoutCandle" ]; then
	grep -v "^$User," $CANDLEDB >$CANDLEDB.tmp
	mv $CANDLEDB.tmp $CANDLEDB
	Speech="Your candle is out. "

elif [ "$LastSeen" ]; then
	print "$LastSeen" | IFS="," read User Candle
	Speech+="I'm happy to see you back again today. "
	Audio="y"

elif [ "$Request" = "LaunchRequest" ]; then
	Speech+="Do you need help, or would you like to light a candle? "

elif [ "$Intent" = "LightCandle" ]; then
	print "$User,$Candle" >>$CANDLEDB
	Speech="I am lighting a candle for you. "
	Audio="y"
fi

chmod g+w $CANDLEDB

if [ "$Audio" ]; then

	AudioFile="$VARCDN/$(date +%j)-*.m3u"

	if [ ! "$LastSeen" -a -f $AudioFile ]; then
		AudioFile=$(ls $AudioFile)
	else
		AudioFile="default.m3u"
	fi
	AudioFile=${AudioFile##*/}

	Audio="<audio controls><source src=$URLCDN/$AudioFile></audio>"

	while IFS="|" read comment text
	do
		text=$(print $text)
		case "$comment" in
		*mediainfo*)
			let Repeat="$text"/4500+8
			;;
		*Repeat*)
			Repeat="$text"
			;;
		*Alexa*)
			AlexaText="$text"
			;;
		*Button*)
			ButtonColor="$text"
			;;
		*Card*)
			Card="$text"
			;;
		esac
	done <$VARCDN/$AudioFile

	[ "$AlexaText" ] && Speech+="$AlexaText<break time=\"1s\"/></break>"
fi

cat - <<EOF
<html><body><speak>$Speech</speak><p>$ButtonColor</p><p>$Repeat</p><p>$(eval print "$Card")</p>$Audio</body></html>
EOF
