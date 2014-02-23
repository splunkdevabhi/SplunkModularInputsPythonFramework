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