from __future__ import print_function
from lxml import html
import requests
import os

def candle_handler(event, context):

    query = {}
    speech = ''; repeat=''; audio = ''; stopplay = False
    requesttype = event['request']['type']
    userId = event['session']['user']['userId']
    shouldEndSession = True
    help = "You can ask to light a candle for an intention, blow out your candle, or ask what the other candles are lit for.  If you have an Echo button, press it once now so I can light that up too. How can I help you? "

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
            try:
                query['Candle'] = slots['intention']['value']
                query['CandleType'] = slots['intention']['resolutions']['resolutionsPerAuthority'][0]['values'][0]['value']['name']
            except:
                pass

            try:
                query['Candle'] = slots['blessing']['value']
                query['CandleType'] = slots['blessing']['resolutions']['resolutionsPerAuthority'][0]['values'][0]['value']['name']
            except:
                pass

            try:
                query['Candle'] = slots['relative']['value']
                query['CandleType'] = slots['relative']['resolutions']['resolutionsPerAuthority'][0]['values'][0]['value']['name']
            except:
                pass

            try:
                query['Candle'] = slots['needy']['value']
                query['CandleType'] = slots['needy']['resolutions']['resolutionsPerAuthority'][0]['values'][0]['value']['name']
            except:
                pass

        elif intentname == "AMAZON.FallbackIntent":
            speech = "I did not understand that. " + help
            shouldEndSession = False

        elif intentname == "AMAZON.HelpIntent":
            shouldEndSession = False
            speech = help

        elif intentname == "AMAZON.PauseIntent" or intentname == "AMAZON.CancelIntent" or intentname == "AMAZON.StopIntent":
            stopplay = True

        elif intentname == "AMAZON.ResumeIntent":
            pass

    else:
        speech = "Come back any time! Goodbye!"

    if query:
        page = requests.get(os.environ.get('ALEXA_URL'), auth=(os.environ.get('ALEXA_USER'), os.environ.get('ALEXA_PASS')), params=query)
        tree = html.fromstring(page.content)
        speech = tree.xpath('//body/p/text()')[0]
        try:
            repeat = tree.xpath('//body/p/text()')[1]
            audio = tree.xpath('//body//audio/source/@src')[0]
        except:
            repeat = ''
            audio = ''

    if audio:
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
                "title": "Votive Candle",
                "content": speech
            },
            "shouldEndSession": shouldEndSession
        }
    }

    if audio:
        # response['response']['card']['content'] = speech + " [" + audio + "] "
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
                                "color": "#000000",
                                "blend": True
                                },
                                {
                                "durationMs": 2000,
                                "color": "#FFD400",
                                "blend": True
                                },
                                {
                                "durationMs": 300,
                                "color": "#FFD400",
                                "blend": True
                                },
                                {
                                "durationMs": 2000,
                                "color": "#000000",
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
