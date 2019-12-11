from lxml import html
import requests
import os

def coachK_handler(event, context):

    query = {}
    speech = ''; audio = ''; stopplay = False
    requesttype = event['request']['type']
    shouldEndSession = True

    if requesttype == "LaunchRequest":
        speech = "Coach K here, with information about our last and next Duke games.  Ask me to read the notes or quotes, replay the postgame interview, or give details about our upcoming game.  How can I help you?"
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
            query['Trigger'] = "CoachK"
            try:
                query['Enum'] = slots['enum']['value']
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
                "title": "CoachK",
                "content": ""
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
