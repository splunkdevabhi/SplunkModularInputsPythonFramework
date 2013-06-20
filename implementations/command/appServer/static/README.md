## Splunk Command Modular Input v1.0beta

## Overview

This is a Splunk modular input add-on for executing commands and indexing the output.
It is quite simply just a Modular Input wrapper around whatever system command/programs that you want to 
periodically execute and capture the output from.


## Dependencies

* Splunk 5.0+
* Supported on Windows, Linux, MacOS, Solaris, FreeBSD, HP-UX, AIX

## Setup

* Untar the release to your $SPLUNK_HOME/etc/apps directory
* Restart Splunk


## Logging

Any modular input errors will get written to $SPLUNK_HOME/var/log/splunk/splunkd.log


## Troubleshooting

* You are using Splunk 5+
* You have permissions to execute the command
* The command is on the system PATH if you're just specifying the command name
* The path to the command is correct if you're specifying the full path to the command
* The command arguments are correct
* The command is installed
* Look for any errors in $SPLUNK_HOME/var/log/splunk/splunkd.log

## Contact

This project was initiated by Damien Dallimore
<table>

<tr>
<td><em>Email</em></td>
<td>ddallimore@splunk.com</td>
</tr>

</table>
