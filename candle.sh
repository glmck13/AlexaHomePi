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

URLCDN="https://mckspot.dyndns.org:8443/cdn"
VARCDN="/var/www/html/cdn"
CANDLEDB="$VARCDN/candledb.csv"
UNKCANDLEDB="$VARCDN/unkcandle.txt"
PRAYER="$VARCDN/prayer.txt"
AUDIOURL="$URLCDN/candle.m3u"
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
	:

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
	Speech+=$(sed -e "s/%INTENTION%/$(prayerContext "$CandleType" "$Candle")/" <$PRAYER)
	Audio="<audio controls><source src=$AUDIOURL></audio>"

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
	done <$VARCDN/${AUDIOURL#$URLCDN}

	Speech+=' <break strength="x-strong"/> '

	[ "$Title" ] && Speech+="If you would like to spend a moment in reflection, here is \"$Title\" "
	[ "$Author" ] && Speech+="by $Author "
	[ "$License" ] && Speech+="released under a $License license "
fi

cat - <<EOF
<html><body><speak>$Speech</speak><p>$Repeat</p><p>$(eval print "$Card")</p>$Audio</body></html>
EOF
