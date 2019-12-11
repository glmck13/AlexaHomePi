from lxml import html
import requests
import os

def scripture_handler(event, context):

    query = {}
    speech = ''; audio = ''; stopplay = False
    requesttype = event['request']['type']
    shouldEndSession = True

    if requesttype == "LaunchRequest":
        query['Intent'] = "PlayScripture"

    elif requesttype == "IntentRequest":

        intentname = event['request']['intent']['name']

        if intentname in ("PlayScripture", "AMAZON.FallbackIntent", "AMAZON.HelpIntent"):
            query['Intent'] = "PlayScripture"

        elif intentname in ("AMAZON.PauseIntent", "AMAZON.CancelIntent", "AMAZON.StopIntent", "AMAZON.NavigateHomeIntent"):
            stopplay = True

        elif intentname == "AMAZON.ResumeIntent":
            pass

    if query:
        page = requests.get(os.environ.get('ALEXA_URL'), auth=(os.environ.get('ALEXA_USER'), os.environ.get('ALEXA_PASS')), params=query)
        tree = html.fromstring(page.content)
        try:
            speech = tree.xpath('//body/p/text()')[0]
        except:
            speech = ''
        try:
            audio = tree.xpath('//body//audio/source/@src')[0]
        except:
            audio = ''

    response = {
        "version": "1.0",
        "sessionAttributes": {},
        "response": {
            "outputSpeech": {
                "type": "PlainText",
                "text": speech
            },
            "shouldEndSession": shouldEndSession
        }
    }

    if shouldEndSession:
        response['response']['reprompt'] = {
            "outputSpeech": {
                "type": "PlainText",
                "text": ""
            }
        }
        response['response']['card'] = {
            "type": "Simple",
            "title": os.environ.get('ALEXA_CARDTITLE'),
            "content": speech
        }

    if audio:
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
