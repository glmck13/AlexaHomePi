#!/bin/ksh

PATH=~ubuntu/bin:$PATH

VARCDN="/var/www/html/cdn/candle"
URLCDN="https://mckserver.dyndns.org/cdn/candle"

[ "$REQUEST_METHOD" = "POST" ] && read -r QUERY_STRING

vars="$QUERY_STRING"
while [ "$vars" ]
do
	print $vars | IFS='&' read v vars
	[ "$v" ] && export $v
done

cd $VARCDN

. ~ubuntu/etc/credentials.conf

[ ! "$Julian" ] && Julian=$(date "+%j")
[ ! "$Color" ] && Color="FFFFFF"
[ ! "$Repeat" ] && Repeat="10"
[ ! "$Reflection" ] && Reflection="Have a nice day!"

M3UFILE="$Julian-reflect.m3u"
MP3FILE="$Julian.mp3"

Reflection=$(urlencode -d "$Reflection")

Day=$(date -d "`date +%Y`-01-01 +$(( ${Julian} - 1 ))days" +"%A, %B %d")

case "$Command" in
	Create*)
		print "$Reflection" | AWS_VOICE=$Voice aws-polly.sh >$MP3FILE
		cat - <<-EOF >$M3UFILE
		# Repeat | $Repeat
		# Button | $Color
		# Voice | $Voice
		# Alexa | Here is the reflection for $Day.
		# Reflection | $Reflection
		$URLCDN/$MP3FILE
		EOF
		;;

	Combine*)
		sox $(ls [0-9]*.mp3 | shuf | sed -e "s/$/ silence.mp3/") default.mp3
		;;
esac

cat - <<-EOF
Content-type: text/html

<html>

<h1>Candle Reflection</h1>
<form action="$SCRIPT_NAME" method="post">

<p>
Julian: <input type="text" size=3 name="Julian" value="$Julian">

Voice: <select name="Voice">
<option value="Joanna">Joanna</option>
<option value="Salli">Salli</option>
<option value="Joey">Joey</option>
<option selected value="Matthew">Matthew</option>
<option value="Brian">Brian</option>
</select>

Color: <select name="Color">
<option value="FFFFFF">White</option>
<option value="FF0000">Red</option>
<option value="00FF00">Lime</option>
<option value="0000FF">Blue</option>
<option selected value="FFFF00">Yellow</option>
<option value="00FFFF">Cyan</option>
<option value="FF00FF">Magenta</option>
<option value="C0C0C0">Silver</option>
<option value="808080">Grey</option>
<option value="800000">Maroon</option>
<option value="808000">Olive</option>
<option value="008000">Green</option>
<option value="800080">Purple</option>
<option value="008080">Teal</option>
<option value="000080">Navy</option>
</select>

Repeat: <input type="text" size=3 name="Repeat" value="$Repeat">
</p>

<p>Reflection:<br><textarea rows=8 cols=80 name="Reflection" />$Reflection</textarea></p>

<input type="submit" name="Command" value="Create File" />
<input type="submit" name="Command" value="Combine All" /><br>

</form>

<hr>

<pre>
$(print "Today is day $Julian: $Day"; ls *.m3u; [ "$Command" ] && cat $M3UFILE)
</pre>

</html>
EOF
