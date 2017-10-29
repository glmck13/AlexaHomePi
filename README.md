# AlexaHomePi
Alexa lamba function &amp; pi-hosted HTTP/CGI back-end utilities for home automation.
## Introduction
In the AskPi project, I created a rudimentary personal virtual assistant that executes primarily within the local network, and relies upon the Google & Amazon clouds only for speech processing support.  Then one day I stumbled upon an [Alexa app built by Nick Sypteras](https://www.nicksypteras.com/projects/teaching-alexa-to-spot-airplanes) that identifies airplanes flying outside his apartment using dump1090.  That was enough to convince me to try building my own Alexa app that could query & control devices in my home network.  That's how "Charlie" was born.  

## Alexa App
Amazon provides lots of tutorials & documentation for creating an app in Alexa.  I used Nick Sypteras' page as a guide, and found it pretty easy to create my own "Charlie" app.  In its current form the app has three intents: QueryNet, ControlTV, and AskPi.  The last intent provides a means for my Alexa app to connect to AskPi, so I can take advantage of the work I did on that project.  I used Amazon's "skill builder" to define the utterances & slots for the app.  These are stored in the "charlie.json" file.  

## Lambda Function
The Charlie skill links to an AWS Lambda function implemented in python.  I'm a newbie to python, but found it very easy to program my skill.  I followed Nick Sypteras' lead, and designed the lamba function to simply serve as a gateway to an HTTPS server I stood up on my local network.  Python's "requests" libary makes it really easy to issue web requests, and "lxml" does the same for parsing HTML responses.  Since my web server is going to be exposed to the Internet, I added some modest security by having it listen on a non-standard port, and require basic authentication.  The URL, username, and password for my server are saved in AWS as environment variables, which are then passed to my function when it is invoked.  

The python code for the skill can be found in "lambda\_function.py".  AWS requires that any/all library dependencies are packaged together with the function when it is uploaded.  You can do this by creating a directory on your development machine (I call it "alexa" below), copying lambda\_function.py to that directory, populating the directory with the python "requests" and "lxml" libraries using the "pip" command, then zipping the result:
```
mkdir alexa; cd alexa
cp ../lambda_function.py .
pip install lxml requests -t .
zip -r ../alexa.zip *
```
The resultant alexa.zip file is then uploaded to AWS.  

Note that the Lambda "Handler" entry is specified as <file name, w/o extension>.<function name>.  So in the current instance this would be specified as "lambda_function.alexa_handler", since "lambda_function.py" is the name of the python file, and "alexa_handler" is the name of the method defined within the file that is invoked when "Charlie" is opened.  

## HTTPS Home Server
I configured an Apache web server on one of my Pi's to listen to port 8443 for HTTPS requests.  This required that I edit a couple of the Apache configuration files as follows:

```
diff ports.conf /etc/apache2 
5c5
< # Listen 80
---
> Listen 80
8c8
< 	Listen 8443
---
> 	Listen 443

diff default-ssl.conf /etc/apache2/sites-available
2,3c2
< 	<VirtualHost _default_:8443>
< 		ServerName mckspot.dyndns.org
---
> 	<VirtualHost _default_:443>
```
In addition, I needed to install certificate & key files for use by the server.  For this purpose, I just copied the files I obtained from LetsEncrypt, as explained under the MobilePi project:
```
SSLCertificateFile  /etc/ssl/certs/ssl-cert-snakeoil.pem # copy of /etc/ipsec.d/certs/fullchain.pem
SSLCertificateKeyFile /etc/ssl/private/ssl-cert-snakeoil.key # copy of /etc/ipsec.d/private/privkey.pem
```
Lastly, I reconfigured my home router to port-forward 8443 to the Pi which is servicing Alexa requests.  

## Fing & IR CGI scripts
