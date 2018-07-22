#!/bin/ksh

statsContext() {
	if [ "$1" = "Needy" ]; then
		print "the $1"
	elif [ "$1" = "Blessing" ]; then
		print "a $1"
	elif [ "$1" = "Relative" ]; then
		print "a $1"
	elif [ "$1" = "Intention" ]; then
		print "a special $1"
	fi
}

prayerContext() {
	if [ "$1" = "Needy" ]; then
		print "the $2"
	elif [ "$1" = "Blessing" ]; then
		print "$2"
	elif [ "$1" = "Relative" ]; then
		print "my $2"
	elif [ "$1" = "Intention" ]; then
		print "my $2"
	fi
}

URLCDN="https://mckserver.dyndns.org/cdn"
VARCDN="/var/www/html/cdn"
CANDLEDB="$VARCDN/candledb.csv"
CANDLESONGS="$VARCDN/candlesongs.txt"
UNKCANDLEDB="$VARCDN/unkcandle.txt"
CANDLEPRAYERS="$VARCDN/candleprayers.txt"
Current=$(wc -l <$CANDLEDB)
if [ "$Current" -eq 0 ]; then
	Speech="No candles are currently lit. "
elif [ "$Current" -eq 1 ]; then
	Speech="$Current candle is currently lit. "
else
	Speech="$Current candles are currently lit. "
fi
Audio=""
Prayer=""
Lastseen=$(grep "^$User," $CANDLEDB)

if [ "$Intent" = "GetCandleStats" ]; then
	cut -f2 -d, <$CANDLEDB | sort | uniq | while read CandleType
	do
		n=$(grep ",$CandleType," $CANDLEDB | wc -l)
		Speech+="$n candles are lit for $(statsContext "$CandleType"). "
	done

elif [ "$Intent" = "BlowoutCandle" ]; then
	grep -v "^$User," $CANDLEDB >$CANDLEDB.tmp
	mv $CANDLEDB.tmp $CANDLEDB
	Speech="Your candle is out. "

elif [ "$Lastseen" ]; then
	print "$Lastseen" | IFS="," read User CandleType Candle
	Speech+="I'm happy to see you back again today. Please join me in a prayer. "
	Prayer="y"

elif [ "$Request" = "LaunchRequest" ]; then
	Speech+="Do you need help, or would you like to light a candle? "

elif [ "$Intent" = "LightCandle" ]; then
	if [ ! "$CandleType" ]; then
		[ "$Candle" ] && print "$Candle" >>$UNKCANDLEDB
		CandleType="Intention" Candle="Intention"
	fi
	print "$User,$CandleType,$Candle" >>$CANDLEDB
	Speech="I am lighting a candle for you. Please join me in a prayer. "
	Prayer="y"
fi

if [ "$Prayer" ]; then
	Prayer=$(shuf -n1 $CANDLEPRAYERS)
	CandleSong=$(shuf -n1 $CANDLESONGS)
	Speech+=$(sed -e "s/%INTENTION%/$(prayerContext "$CandleType" "$Candle")/" <$VARCDN/$Prayer)
	Audio="<audio controls><source src=$URLCDN/$CandleSong></audio>"

	while IFS="|" read comment text
	do
		text=$(print $text)
		case "$comment" in
		*mediainfo*)
			let Repeat="$text"/4500+8
			;;
		*Title*)
			Title="$text"
			;;
		*Author*)
			Author="$text"
			;;
		*License*)
			License="$text"
			;;
		*Card*)
			Card="$text"
			;;
		esac
	done <$VARCDN/$CandleSong

	Speech+=' <break strength="x-strong"/> '

	[ "$Title" ] && Speech+="If you would like to spend a moment in reflection, listen to \"$Title\" "
	[ "$Author" ] && Speech+="by $Author "
	# [ "$License" ] && Speech+="released under a $License license "

	Speech+='.'
fi

cat - <<EOF
<html><body><speak>$Speech</speak><p>$Repeat</p><p>$(eval print "$Card")</p>$Audio</body></html>
EOF
