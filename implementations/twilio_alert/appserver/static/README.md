## Splunk Twilio Modular Alert v0.5

## Overview

This is a Splunk Modular Alert for sending SMS messages using Twilio.

## Dependencies

* Splunk 6.3+
* Supported on Windows, Linux, MacOS, Solaris, FreeBSD, HP-UX, AIX

## Setup

* Untar the release to your $SPLUNK_HOME/etc/apps directory
* Restart Splunk

## Configuration

You will need a Twilio account to use this Modular Alert.

You can sign up at twilio.com

Once your Twilio account is setup you will then be able to obtain your Auth Token and Account SID from your profile.

To enter these values in Splunk , just browse to Settings -> Alert Actions -> Twilio SMS Alerts -> Setup Twilio SMS Alerting

## Using

Perform a search in Splunk and then navigate to : Save As -> Alert -> Trigger Actions -> Add Actions -> Twilio SMS Alerts

On this dialogue you can enter your "from number", "to number" and "SMS message"

For the SMS message field , token substitution can be used just the same as for email alerts.

http://docs.splunk.com/Documentation/Splunk/latest/Alert/Setupalertactions#Tokens_available_for_email_notifications


## Logging

Browse to : Settings -> Alert Actions -> Twilio SMS Alerts -> View Log Events

Or you can search directly in Splunk : index=_internal sourcetype=splunkd component=sendmodalert action="twilio"


## Troubleshooting

1) Is your "from number" correct and valid for sending SMS messages via Twilio ?
2) Are your alerts actually firing ?
3) Are your Auth token and Account SID correct ?

## Contact

This project was initiated by Damien Dallimore , ddallimore@splunk.com

