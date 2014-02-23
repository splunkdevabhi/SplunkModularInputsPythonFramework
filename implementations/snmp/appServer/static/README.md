## SNMP Modular Input v1.2.2

By Damien Dallimore and Scott Spencer

## Overview

This is a Splunk modular input add-on for polling SNMP attributes and catching traps.

## Features

* Simple UI based configuration via Splunk Manager
* Capture SNMP traps (Splunk becomes a SNMP trap daemon in its own right)
* Poll SNMP object attributes
* SNMP version 1,2c and 3 support
* Declare objects to poll in textual or numeric format
* Ships with a wide selection of standard industry MIBs
* Add in your own Custom MIBs
* Walk object trees using GET BULK
* Optionally index bulk results as individual events in Splunk
* Monitor 1 or more Objects per stanza
* Create as many SNMP input stanzas as you require
* IPv4 and IPv6 support
* Indexes SNMP events in key=value semantic format
* Plug in your own custom response handler for formatting or pre-processing
* Ships with some additional custom field extractions

## Dependencies

* Splunk 5.0+
* Supported on Windows, Linux, MacOS, Solaris, FreeBSD, HP-UX, AIX

## Setup

* Untar the release to your $SPLUNK_HOME/etc/apps directory
* Restart Splunk

## SNMP Version 3 Crypto Libraries

If you are using SNMP version 3 , you have to obtain, build and add the pycrypto package yourself :

https://pypi.python.org/pypi/pycrypto

The simplest way is to build pycrypto and drop the "Crypto" directory in $SPLUNK_HOME/etc/apps/snmp_ta/bin.
I don't recommend installing the pycrypto package to the Splunk Python runtime's site-packages, this could have unforeseen side effects.

### Building and installing PyCrypto

I do not bundle the pycrypto module with the core release , because :

* you need to build it for each separate platform
* US export controls for encrypted software

So , here are a few instructions for building and installing pycrypto yourself :

* Download the pycrypto package from https://pypi.python.org/pypi/pycrypto

* Then run these 3 commands  (note : you will  need to use a System python 2.7 runtime , not the Splunk python runtime)

        python setup.py build
        python setup.py install
        python setup.py test
        
3) browse to where the Crypto module was installed to ie: /usr/local/lib/python2.7/dist-packages/Crypto

4) Copy the "Crypto" directory to $SPLUNK_HOME/etc/apps/snmp_ta/bin


## Adding Custom MIBs

The pysnmp library is used under the hood so you need to convert your plain text MIB files 
into python modules :

Many industry standard MIBs ship with the Modular Input.
You can see which MIBs are available by looking in SPLUNK_HOME/etc/apps/snmp_ta/bin/mibs/pysnmp_mibs-0.1.4-py2.7.egg

Any additional custom MIBs need to be converted into Python Modules.

You can simply do this by using the build-pysnmp-mib tool that is part of the pysnmp installation

build-pysnmp-mib -o SOME-CUSTOM-MIB.py SOME-CUSTOM-MIB.mib

build-pysnmp-mib is just a wrapper around smidump.

So alternatively you can also execute :

smidump -f python <mib-text-file.txt> | libsmi2pysnmp > <mib-text-file.py>

Then you can either copy the generated python files to SPLUNK_HOME/etc/apps/snmp_ta/bin/mibs or build a Python "egg" of 
the generated python files(maybe tidier if you have many python files) and copy the egg to that same location.

In the configuration screen for the SNMP input in Splunk Manager , there is a field called “MIB Names” (see above).
Here you can specify the MIB names you want applied to the SNMP input definition ie: IF-MIB,DNS-SERVER-MIB,BRIDGE-MIB
The MIB Name is the same as the name of the MIB python module in your egg package.

### Custom Response Handlers

You can provide your own custom Response Handler. This is a Python class that you should add to the 
rest_ta/bin/responsehandlers.py module.

You can then declare this class name and any parameters in the SNMP Modular Input setup page.

For the most part the Default Response Handler should suffice.

But there may be situations where you want to format the response in a manner that is more convenient for handling your data ie: CSV or JSON.
Furthermore , you can also use a custom Response Handler implementation to perform preprocessing of your raw response data before sending 
it to Splunk.

## Logging

Any modular input log errors will get written to $SPLUNK_HOME/var/log/splunk/splunkd.log


## Troubleshooting

* You are using Splunk 5+
* Look for any errors in $SPLUNK_HOME/var/log/splunk/splunkd.log


