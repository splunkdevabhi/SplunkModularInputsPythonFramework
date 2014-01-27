# Splunk Tesla Modular Input v0.5

## Overview

This is a Splunk modular input add-on for polling your Tesla Vehicle data from the My Tesla API.

The following unofficial API reference was utilised : http://docs.timdorr.apiary.io/

### Authentication

Authentication is with your My Tesla credentials.
After the initial authentication , cookies are persisted(to inputs.conf) and sent with each request.

### Data Source Types

By default the following data is requested and returned in JSON format :

* Vehicle List
* Vehicle Mobile Status
* Vehicle Charge State
* Vehicle Climate State
* Vehicle Drive State
* Vehicle GUI Settings
* Vehicle State

### Index

By default , data will go into the "tesla" index

### Custom Response Handlers

You can provide your own custom Response Handler. This is a Python class that you should add to the 
tesla_ta/bin/responsehandlers.py module.

You can then declare this class name and any parameters in the Tesla Input setup page.


## Dependencies

* Splunk 5.0+
* Supported on Windows, Linux, MacOS, Solaris, FreeBSD, HP-UX, AIX

## Setup

* Untar the release to your $SPLUNK_HOME/etc/apps directory
* Restart Splunk
* Browse to Manager -> Data Inputs -> Tesla and setup your inputs


## Logging

Any log entries/errors will get written to $SPLUNK_HOME/var/log/splunk/splunkd.log


## Troubleshooting

* You are using Splunk 5+
* Look for any errors in $SPLUNK_HOME/var/log/splunk/splunkd.log
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