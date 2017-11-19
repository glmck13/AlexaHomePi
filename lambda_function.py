from __future__ import print_function
from lxml import html
import requests
import os

def alexa_handler(event, context):

    query = {}
    speech = ''; audio = ''

    if event['request']['type'] == "LaunchRequest":
        speech = "Charlie here!  I can control your TV, explore your network, and connect to AskPi.  How can I help you?"
        shouldEndSession = False

    elif event['request']['type'] == "IntentRequest":
        intent = event['request']['intent']
        slots = intent['slots']
        query['Intent'] = intent['name']
        if intent['name'] == "QueryNet":
            try:
                query['Device'] = slots['devices']['value']
            except:
                pass
        elif intent['name'] == "ControlTV":
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
        elif intent['name'] == "AskPi":
            try:
                query['Trigger'] = slots['trigger']['value']
            except:
                pass
            try:
                query['Enum'] = slots['enum']['value']
            except:
                pass

        page = requests.get(os.environ.get('ALEXA_URL'), auth=(os.environ.get('ALEXA_USER'), os.environ.get('ALEXA_PASS')), params=query)
        tree = html.fromstring(page.content)
        speech = tree.xpath('//body/p/text()')[0]
        try:
            audio = tree.xpath('//body//audio/source/@src')[0]
        except:
            audio = ''
        shouldEndSession = True

    else:
        speech = "Come back soon! Goodbye!"
        shouldEndSession = True

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
            "shouldEndSession": "True"
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

    return response
