from lxml import html
import requests
import os

def alexa_handler(event, context):

    query = {}
    speech = ''; audio = ''; stopplay = False
    requesttype = event['request']['type']
    sysinfo = event['context']['System']
    shouldEndSession = True

    if requesttype == "LaunchRequest":
        speech = "Charlie here!"
        shouldEndSession = False

    elif requesttype == "IntentRequest":
        intent = event['request']['intent']
        intentname = intent['name']
        try:
            slots = intent['slots']
        except:
            slots = {}

        if intentname == "QueryNet":
            query['Intent'] = intentname
            try:
                query['Device'] = slots['devices']['value']
            except:
                pass

        elif intentname == "ControlTV":
            query['Intent'] = intentname
            try:
                query['OnOff'] = slots['onoff']['value']
            except:
                pass
            try:
                query['UpDown'] = slots['updown']['value']
            except:
                pass
            try:
                query['ChannelName'] = slots['channelname']['value']
            except:
                pass

        elif intentname == "AskPi":
            query['Intent'] = intentname
            try:
                query['Trigger'] = slots['trigger']['value']
            except:
                pass
            try:
                query['Enum'] = slots['enum']['value']
            except:
                pass
            try:
                query['Endpoint'] = sysinfo['apiEndpoint']
            except:
                pass
            try:
                query['Accesstoken'] = sysinfo['apiAccessToken']
            except:
                pass
            try:
                query['Device'] = sysinfo['device']['deviceId']
            except:
                pass

        elif intentname == "AMAZON.PauseIntent" or intentname == "AMAZON.CancelIntent" or intentname == "AMAZON.StopIntent":
            stopplay = True

        elif intentname == "AMAZON.ResumeIntent" or intentname == "AMAZON.HelpIntent":
            pass

        if query:
            page = requests.get(os.environ.get('ALEXA_URL'), auth=(os.environ.get('ALEXA_USER'), os.environ.get('ALEXA_PASS')), params=query)
            tree = html.fromstring(page.content)
            speech = tree.xpath('//body/p/text()')[0]
            try:
                audio = tree.xpath('//body//audio/source/@src')[0]
            except:
                audio = ''

    else:
        speech = "Come back soon! Goodbye!"

    response = {
        "version": "1.0",
        "sessionAttributes": {},
        "response": {
            "outputSpeech": {
                "type": "PlainText",
                "text": speech
            },
            "reprompt": {
                "outputSpeech": {
                    "type": "PlainText",
                    "text": ""
                }
            },
            "card": {
                "type": "Simple",
                "title": "Charlie",
                "content": speech
            },
            "shouldEndSession": shouldEndSession
        }
    }

    if audio:
        response['response']['card']['content'] = speech + " [" + audio + "] "
        response['response']['directives'] = [
            {
            "type": "AudioPlayer.Play",
            "playBehavior": "REPLACE_ALL",
              "audioItem": {
                "stream": {
                  "token": audio,
                  "url": audio,
                "offsetInMilliseconds": 0
                }
              }
            }
        ]

    if stopplay:
        response['response']['directives'] = [
            {
            "type": "AudioPlayer.ClearQueue",
            "clearBehavior": "CLEAR_ALL"
            }
        ]

    return response
