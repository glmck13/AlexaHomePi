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
        query['Enum'] = os.environ.get('ALEXA_EVENT')

        page = requests.get(os.environ.get('ALEXA_URL'), auth=(os.environ.get('ALEXA_USER'), os.environ.get('ALEXA_PASS')), params=query)
        tree = html.fromstring(page.content)
        speech = html.tostring(tree.xpath('//speak')[0]).decode()
    else:
        speech = "<speak>" + "Come back any time! Goodbye!" + "</speak>"

    response = {
        "version": "1.0",
        "sessionAttributes": {},
        "response": {
            "outputSpeech": {
                "type": "SSML",
                "ssml": speech
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
