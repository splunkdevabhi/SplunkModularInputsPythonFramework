1.2.7
-----

Merged in community Pull requests.

1) Add a new option to get subtree
2) Add a new option to perform rDNS for trap source
3) Fix to resolve missing server extractions on the SNMPv3 trap receiver


1.2.6
-----

In the destination field for polling attributes , you can now optionally specify a comma delimited list of hosts

1.2.5
-----

Fixed Bug in UI that prevented declaring custom MIB Names when in listen traps mode

1.2.4
-----
Fixed host field extraction for receiving v2 traps

1.2.3
-----
Minor code fixes

1.2.2
-----
Updated the manager UI

1.2.1
-----
Minor cosmetic fixes

1.2
---
SNMP v3 support , please follow the docs regarding pycrypto dependencies

pysnmp library update to 4.2.5

Support for plugging in custom response handlers that can format the raw SNMP data in a particular format or perform preprocessing on the raw SNMP data before indexing in Splunk. Has a default response handler which produces the same output as previous versions.Also ships with an example JSONFormatterResponseHandler.

Robustified exception handling

More detailed logging