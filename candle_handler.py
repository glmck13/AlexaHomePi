from lxml import html
import requests
import os
import json
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def candle_handler(event, context):

    query = {}
    speech = ''; color=''; repeat=''; card = ''; audio = ''; stopplay = False
    requesttype = event['request']['type']
    userId = event['session']['user']['userId']
    shouldEndSession = True
    help = "You can ask to light a candle for an intention, or blow out your candle.  If you have an Echo button, press it once now so I can light that up too. How can I help you? "

    if requesttype == "LaunchRequest":
        query['Intent'] = "LightCandle"
        query['Request'] = requesttype
        query['User'] = userId
        shouldEndSession = False

    elif requesttype == "IntentRequest":
        intent = event['request']['intent']
        intentname = intent['name']
        try:
            slots = intent['slots']
        except:
            slots = {}

        if intentname == "GetCandleStats":
            query['Intent'] = intentname
            query['Request'] = requesttype
            query['User'] = userId

        elif intentname == "BlowoutCandle":
            query['Intent'] = intentname
            query['Request'] = requesttype
            query['User'] = userId

        elif intentname == "LightCandle":
            query['Intent'] = intentname
            query['Request'] = requesttype
            query['User'] = userId
            query['Candle'] = "Intention"

        elif intentname == "AMAZON.FallbackIntent":
            speech = "<speak>" + "OK. " + help + "</speak>"
            shouldEndSession = False

        elif intentname == "AMAZON.HelpIntent":
            shouldEndSession = False
            speech = "<speak>" + help + "</speak>"

        elif intentname == "AMAZON.PauseIntent" or intentname == "AMAZON.CancelIntent" or intentname == "AMAZON.StopIntent":
            stopplay = True

        elif intentname == "AMAZON.ResumeIntent":
            pass

    else:
        speech = "<speak>" + "Come back any time! Goodbye!" + "</speak>"

    if query:
        page = requests.get(os.environ.get('ALEXA_URL'), auth=(os.environ.get('ALEXA_USER'), os.environ.get('ALEXA_PASS')), params=query)
        tree = html.fromstring(page.content)
        speech = html.tostring(tree.xpath('//speak')[0], encoding="unicode")
        subtree = tree.xpath('//body/p')
        try:
            color = subtree[0].xpath('string()')
            repeat = subtree[1].xpath('string()')
            card = subtree[2].xpath('string()')
            audio = tree.xpath('//body//audio/source/@src')[0]
        except:
            repeat = ''; card = ''; audio = ''

    if audio:
        shouldEndSession = True

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
                "title": "Votive Candle",
                "content": card
            },
            "shouldEndSession": shouldEndSession
        }
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
            },
            {
            "type": "GadgetController.SetLight",
            "version": 1,
            "targetGadgets": [ ],
            "parameters": {
                "triggerEvent": "none",
                "triggerEventTimeMs": 0,
                "animations": [ 
                        {
                        "repeat": int(repeat),
                        "targetLights": ["1"],
                        "sequence": [
                                {
                                "durationMs": 1,
                                "color": "000000",
                                "blend": True
                                },
                                {
                                "durationMs": 2000,
                                "color": color,
                                "blend": True
                                },
                                {
                                "durationMs": 300,
                                "color": color,
                                "blend": True
                                },
                                {
                                "durationMs": 2000,
                                "color": "000000",
                                "blend": True
                                }
                            ]
                        }
                    ]
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
