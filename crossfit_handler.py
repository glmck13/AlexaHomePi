from __future__ import print_function
from lxml import html
import requests
import os

def crossfit_handler(event, context):

    query = {}
    speech = ''
    requesttype = event['request']['type']
    shouldEndSession = True

    if requesttype == "LaunchRequest":
        speech = "Hello!  What workout are you interested in?"
        shouldEndSession = False

    elif requesttype == "IntentRequest":
        intent = event['request']['intent']
        intentname = intent['name']
        try:
            slots = intent['slots']
        except:
            slots = {}

        if intentname == "AskPi":
            query['Intent'] = intentname
            query['Trigger'] = "Crossfit"
            try:
                query['Enum'] = slots['enum']['value']
            except:
                pass

        if query:
            page = requests.get(os.environ.get('ALEXA_URL'), auth=(os.environ.get('ALEXA_USER'), os.environ.get('ALEXA_PASS')), params=query)
            tree = html.fromstring(page.content)
            speech = tree.xpath('//body/p/text()')[0]

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
                "title": "Crossfit",
                "content": speech
            },
            "shouldEndSession": shouldEndSession
        }
    }

    return response
