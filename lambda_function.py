from __future__ import print_function
from lxml import html
import requests
import os

def alexa_handler(event, context):

    query = {}
    if event['request']['type'] == "LaunchRequest":
        speech = "Charlie here!  I can explore your home network and control your TV. Ask me things like: What iPhones are on the network? Or, Turn on MSNBC.  How can I help you?"
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
            try:
                query['ChannelNumber'] = slots['channelnumber']['value']
            except:
                pass

        page = requests.get(os.environ.get('ALEXA_URL'), auth=(os.environ.get('ALEXA_USER'), os.environ.get('ALEXA_PASS')), params=query)
        tree = html.fromstring(page.content)
        speech = tree.xpath('//body/text()')[0]
        shouldEndSession = True

    else:
        speech = "Come back soon! Goodbye!"
        shouldEndSession = True

    return {
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
