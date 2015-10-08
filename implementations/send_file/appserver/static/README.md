## Scheduled Export of Indexed Data (SEND)  to File v0.5

## Overview

This is a Splunk Modular Alert used to facilitate scheduled export of indexed data (SEND) to a file location

The exported file is just a gzipped CSV of the search results that triggered the alert.

The real intent of this add-on though is as an example for developers to follow to show how you can essentially leverage the Modular Alerts framework to perform a scheduled data output.

Other types of outputs to consider implementing : ftp,scp,jms,kafka,aws,rdbms,datawarehouse,some other data storage or processing platform etc...

## Note from the Modular Alerts engineer

The only thing to keep in mind is constraint of alerts in terms of scalability. The alert action script has a limited lifetime before it’s being killed by the scheduler. The scheduler itself is also not designed for massive output loads. It should be perfectly fine for smaller scale output, though.

## Dependencies

* Splunk 6.3+
* Supported on Windows, Linux, MacOS, Solaris, FreeBSD, HP-UX, AIX

## Setup

* Untar the release to your $SPLUNK_HOME/etc/apps directory
* Restart Splunk


## Using

Perform a search in Splunk and then navigate to : Save As -> Alert -> Trigger Actions -> Add Actions -> SEND to File

On this dialogue you can enter your file output settings.


## Logging

Browse to : Settings -> Alert Actions -> SEND to File -> View Log Events

Or you can search directly in Splunk : index=_internal sourcetype=splunkd component=sendmodalert action="sendfile"


## Contact

This project was initiated by Damien Dallimore , ddallimore@splunk.com

