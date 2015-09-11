# Splunk Tesla Modular Input v0.6

## Overview

This is a Splunk modular input add-on for polling your Tesla Vehicle data from the My Tesla API.

The following unofficial API reference was utilised : http://docs.timdorr.apiary.io/

## Dependencies

* Splunk 5.0+
* Supported on Windows, Linux, MacOS, Solaris, FreeBSD, HP-UX, AIX

## Setup

* Untar the release to your $SPLUNK_HOME/etc/apps directory
* Restart Splunk
* Browse to Manager -> Data Inputs -> Tesla and setup your inputs


### Authentication

Authentication is with your My Tesla credentials , plain text email and password, matching the owner's login information for https://my.teslamotors.com/user/login.

A client ID and secret are also required.

The current client ID and secret are available here : http://pastebin.com/fX6ejAHd

You can setup up your My Tesla username and password in each pre defined stanza via SplunkWeb.

Or you can edit SPLUNK_HOME/etc/apps/tesla_ta/default/inputs.conf directly and set the username and password in the parent tesla stanza so that all child stanzas inherit your username and password.

### Data Source Types

By default the following data is requested and returned in JSON format :

* Vehicle List
* Vehicle Mobile Status
* Vehicle Charge State
* Vehicle Climate State
* Vehicle Drive State
* Vehicle State

There are default stanzas setup for each of these.

Aside from "Vehicle List" . all of the other stanzas take a vehicle id which you can set via SplunkWeb.
If you have more than 1 vehicle , you can clone the default stanzas and setup your other vehicle id(s).

### Index

By default , data will go into the "tesla" index

### Custom Response Handlers

You can provide your own custom Response Handler. This is a Python class that you should add to the 
SPLUNK_HOME/etc/apps/tesla_ta/bin/responsehandlers.py module.

You can then declare this class name and any parameters in the Tesla Input setup page.


## Logging

Any log entries/errors will get written to SPLUNK_HOME/var/log/splunk/splunkd.log


## Troubleshooting

* You are using Splunk 5+
* Look for any errors in SPLUNK_HOME/var/log/splunk/splunkd.log
* Any firewalls blocking outgoing HTTP calls
* Is your REST URL correct
* Is you authentication setup correctly

## Contact

This project was initiated by Damien Dallimore
<table>

<tr>
<td><em>Email</em></td>
<td>ddallimore@splunk.com</td>
</tr>

</table>