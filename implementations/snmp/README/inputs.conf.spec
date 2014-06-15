[snmp://<name>]

*attributes | traps
snmp_mode = <value>

*IP or hostname of the device you would like to query, or a comma delimited list
destination= <value>

*Whether or not this is an IP version 6 address. Defaults to false.
ipv6= <value>

*The SNMP port. Defaults to 161
port= <value>

*The SNMP Version , 1 / 2C / 3 . Defaults to 2C
snmp_version= <value>

*1 or more Object Names , comma delimited , in either textual(iso.org.dod.internet.mgmt.mib-2.system.sysDescr.0) or numerical(1.3.6.1.2.1.1.3.0) format.
object_names= <value>

*Whether or not to perform an SNMP GET BULK operation.This will retrieve all the object attributes in the sub tree of the declared OIDs.Be aware of potential performance issues , http://www.net-snmp.org/wiki/index.php/GETBULK. Defaults to false.
do_bulk_get= <value>

*Whether or not to split up bulk output into individual events
split_bulk_output= <value>

*The number of objects that are only expected to return a single GETNEXT instance, not multiple instances. Managers frequently request the value of sysUpTime and only want that instance plus a list of other objects.Defaults to 0. 
non_repeaters= <value>

*The number of objects that should be returned for all the repeating OIDs. Agent's must truncate the list to something shorter if it won't fit within the max-message size supported by the command generator or the agent.Defaults to 25.
max_repetitions= <value>

*Community String used for SNMP version 1 and 2C authentication.Defaults to "public"
communitystring= <value>

*SNMPv3 USM username
v3_securityName= <value>

*SNMPv3 secret authorization key used within USM for SNMP PDU authorization. Setting it to a non-empty value implies MD5-based PDU authentication (defaults to usmHMACMD5AuthProtocol) to take effect. Default hashing method may be changed by means of further authProtocol parameter
v3_authKey= <value>

*SNMPv3 secret encryption key used within USM for SNMP PDU encryption. Setting it to a non-empty value implies MD5-based PDU authentication (defaults to usmHMACMD5AuthProtocol) and DES-based encryption (defaults to usmDESPrivProtocol) to take effect. Default hashing and/or encryption methods may be changed by means of further authProtocol and/or privProtocol parameters. 
v3_privKey= <value>

*may be used to specify non-default hash function algorithm. Possible values include usmHMACMD5AuthProtocol (default) / usmHMACSHAAuthProtocol / usmNoAuthProtocol
v3_authProtocol= <value> 

*may be used to specify non-default ciphering algorithm. Possible values include usmDESPrivProtocol (default) / usmAesCfb128Protocol / usm3DESEDEPrivProtocol / usmAesCfb192Protocol / usmAesCfb256Protocol / usmNoPrivProtocol
v3_privProtocol= <value>

*How often to run the SNMP query (in seconds). Defaults to 60 seconds
snmpinterval= <value>

*Whether or not to listen for TRAP messages. Defaults to false
listen_traps= <value>

*The TRAP port to listen on. Defaults to 162
trap_port= <value>

*The trap host. Defaults to localhost
trap_host= <value>

*List of MIB names to be loaded and applied to your objects
mib_names = <value>

*Python classname of custom response handler
response_handler= <value>

*Response Handler arguments string ,  key=value,key2=value2
response_handler_args= <value>
