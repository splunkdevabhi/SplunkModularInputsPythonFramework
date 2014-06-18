## Splunk CEPA Modular Input v1.4

## Overview

This is a Splunk modular input add-on for EMC CEPA API. When enabled it establishes an HTTP server and listens for events via HTTP PUT requests that are sent from the EMC Common Event Enabler (CEE) Framework client.

## Python Twisted

This Moduar Input depends on the Python Twisted package.
Please download it and build it for your platform : https://twistedmatrix.com

## Dependencies

* Splunk 5.0+
* Supported on Windows, Linux, MacOS, Solaris, FreeBSD, HP-UX, AIX

## Setup

* Untar the release to your $SPLUNK_HOME/etc/apps directory
* Restart Splunk


# CEE Framework Setup

The CEE framework runs on Windows and Linux and can be downloaded from the EMC website.

You will be installing the CEE, the Splunk Universal Forwarder, and this Modular input on
the same server.  Once installed and the CEE server/daemon is running, the Splunk
Universal Forwarder with the Modular Input will receive HTTP PUT requests from CEE, register, respond to
heartbeat requests, and receive the check_event_requests which will be indexed in Splunk.

Example config of emc_cee_config.xml:

<Configuration>
        <Enabled>1</Enabled>
        <EndPoint>Splunk@http://YOUR_CEE_SERVER:PORT</EndPoint>
</Configuration>

Example config of inputs.conf for the Modular Input where the CEPA API and a Splunk Forwarder or Indexer is running on 10.0.0.4:

[cepa://isilon]
host = Isilon
http_bind_address = 10.0.0.4
http_port = 12229
index = emc
sourcetype = CEPA


Isilon OneFS:

1.  Login to OneFS
2.  Select Cluster Management
3.  Select Auditing
4.  Under Event Forwarding add the server where CEPA is installed.

http://10.0.0.4:12228/CEE

## Logging

Any log entries/errors will get written to $SPLUNK_HOME/var/log/splunk/splunkd.log


## Troubleshooting

* You are using Splunk 5+
* Look for any errors in $SPLUNK_HOME/var/log/splunk/splunkd.log
