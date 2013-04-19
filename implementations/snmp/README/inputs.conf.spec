[snmp://<name>]

*IP or hostname of the device you would like to query
destination= <value>

*The SNMP port. Defaults to 161
port= <value>

*The MIB that contains the OID to query. Defaults to "SNMPv2-MIB"
mib= <value>

*The OID that you want to query. Defaults to "sysDescr"
oid= <value>

*The index of the OID to query. Defaults to 0
snmpindex= <value>

*Community String used for authentication
communitystring= <value>

*How often to run the SNMP query (in seconds). Defaults to 60 seconds
snmpinterval= <value>