from __future__ import print_function
from lxml import html
import requests
import os

def savethedate_handler(event, context):

    query = {}
    speech = ''
    requesttype = event['request']['type']
    shouldEndSession = True

    if requesttype in ("LaunchRequest", "IntentRequest"):
        query['Intent'] = "AskPi"
        query['Trigger'] = "Savethedate"
        query['Enum'] = "09/22/2018 21401 Katie and Danny are getting married"

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
                "title": "Savethedate",
                "content": speech
            },
            "shouldEndSession": shouldEndSession
        }
    }

    return response