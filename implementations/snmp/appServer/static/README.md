## Splunk SNMP Modular Input v1.0.1beta

## Overview

This is a Splunk modular input add-on for polling SNMP attributes and catching traps.

## Features

* Simple UI based configuration via Splunk Manager
* Capture SNMP traps (Splunk becomes a snmp trap daemon in its own right)
* Poll SNMP object attributes
* Declare objects to poll in textual or numeric format
* Dynamically add Custom MIBs
* Walk object trees using GET BULK
* Monitor 1 or more Objects per stanza
* Create as many SNMP input stanzas as you require
* SNMP v1/v2c support  , v3 will be implemented if demand is there for it
* IPv4 and IPv6 support
* Indexes SNMP events in key=value semantic format
* Ships with some additional custom extractions


## Dependencies

* Splunk 5.0+
* Supported on Windows, Linux, MacOS, Solaris, FreeBSD, HP-UX, AIX

## Setup

* Untar the release to your $SPLUNK_HOME/etc/apps directory
* Restart Splunk

## Adding Custom MIBs

The pysnmp library is used under the hood so you need to convert your plain text MIB files 
into python modules :

http://pysnmp.sourceforge.net/faq.html#4

Then zip these up in a python "egg" file and drop in the $SPLUNK_HOME/etc/apps/snmp_ta/bin/mibs directory


## Logging

Any log entries/errors will get written to $SPLUNK_HOME/var/log/splunk/splunkd.log


## Troubleshooting

* You are using Splunk 5+
* Look for any errors in $SPLUNK_HOME/var/log/splunk/splunkd.log

## Contact

This project was initiated by Damien Dallimore & Scott Spencer 
<table>

<tr>
<td><em>Email</em></td>
<td>ddallimore@splunk.com</td>
</tr>
<tr>
<td><em>Email</em></td>
<td>sspencer@splunk.com</td>
</tr>


</table>
