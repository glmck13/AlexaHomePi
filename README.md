# AlexaHomePi
Alexa lamba function &amp; pi-hosted HTTP/CGI back-end utilties for home automation.
## Introduction
In the AskPi project, I created a rudimentary, but powerful personal virtual assitant that executes primarily within the local network, and relies upon the Google & Amazon clouds only for speech processing support.  Then one day I stumbled upon an [Alexa app built by Nick Sypteras](https://www.nicksypteras.com/projects/teaching-alexa-to-spot-airplanes) that identies airplanes flying outside his apartment using dump1090.  That was enough to convince me to try building my own Alexa app that could query & control devices in my home network.  That's how "Charlie" was born.
## Alexa App
Amazon provides lots of tutorials & documentation for creating an app in Alexa.  I used Mick Sypteras' page as a guide, and found it pretty easy to create my own "Charlie" app.  In its current form the app has two intents: QueryNet, and ControlTV.
## Lambda Function
```
pip install lxml requests -t ./alexa
```
## HTTPS Home Server
## Fing & IR utilites
