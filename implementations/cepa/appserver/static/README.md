# Splunk CEPA Modular Input v1.4

## Overview

This is a Splunk Modular Input Add-On for the EMC CEPA API. When enabled it establishes a HTTP server and listens for events via HTTP PUT requests that are sent from the EMC Common Event Enabler (CEE) Framework client.

## Initial Setup

* Untar the release to your $SPLUNK_HOME/etc/apps directory
* Do not restart Splunk yet.Perform the next step regarding Python dependencies and then restart Splunk.

## Python Dependencies that must be installed

This Modular Input depends on a few Python packages that are not included in Splunk's Python runtime and need to
be built for the platform that you are deploying this Modular Input on.

### Twisted 14.0

The Twisted Web package provides for implementing a HTTP server that is asynchronous and event driven which should
scale optimally for high throughput environments.

* Download the Twisted tarball from here : https://pypi.python.org/packages/source/T/Twisted/Twisted-14.0.0.tar.bz2
* Untar it , browse to the untarred directory and run : python setup.py install
* Browse to "site-packages" and copy the "twisted" directory to $SPLUNK_HOME/etc/apps/cepa_ta/bin

### Zope 4.1.1

Zope is depended on by Twisted

* Download the Zope tarball from here : https://pypi.python.org/packages/source/z/zope.interface/zope.interface-4.1.1.tar.gz
* Untar it , browse to the untarred directory and run : python setup.py install
* Browse to "site-packages" and copy the "zope" directory to $SPLUNK_HOME/etc/apps/cepa_ta/bin

### PyOpenSSL 0.14

Splunk's version of PyOpenSSL is 0.8 , however a minimum version of 0.12 is required by Twisted

* Download the Zope tarball from here : https://pypi.python.org/packages/source/p/pyOpenSSL/pyOpenSSL-0.14.tar.gz
* Untar it , browse to the untarred directory and run : python setup.py install
* Browse to "site-packages" and copy the "OpenSSL" directory to $SPLUNK_HOME/etc/apps/cepa_ta/bin


## CEE Framework Setup

The CEE framework runs on Windows and Linux and can be downloaded from the EMC website.

You will be installing the CEE, the Splunk Universal Forwarder, and this Modular input on
the same server.  Once installed and the CEE server/daemon is running, the Splunk
Universal Forwarder with the Modular Input will receive HTTP PUT requests from CEE, register, respond to
heartbeat requests, and receive the check_event_requests which will be indexed in Splunk.

Example config of emc_cee_config.xml:

```
<Configuration>
        <Enabled>1</Enabled>
        <EndPoint>Splunk@http://YOUR_CEE_SERVER:PORT</EndPoint>
</Configuration>
```

Example config of inputs.conf for the Modular Input where the CEPA API and a Splunk Forwarder or Indexer is running on 10.0.0.4:

```
[cepa://isilon]
host = Isilon
http_bind_address = 10.0.0.4
http_port = 12229
index = emc
sourcetype = CEPA
```

Isilon OneFS:

1.  Login to OneFS
2.  Select Cluster Management
3.  Select Auditing
4.  Under Event Forwarding add the server where CEPA is installed : http://10.0.0.4:12228/CEE

## Logging

Any log entries/errors will get written to $SPLUNK_HOME/var/log/splunk/splunkd.log


## Troubleshooting

* You are using Splunk 5+
* Look for any errors in $SPLUNK_HOME/var/log/splunk/splunkd.log
