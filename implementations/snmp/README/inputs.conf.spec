[snmp://<name>]

*IP or hostname of the device you would like to query
destination= <value>

*Whether or not this is an IP version 6 address. Defaults to false.
ipv6= <value>

*The SNMP port. Defaults to 161
port= <value>

*The SNMP Version , 1 or 2C, version 3 not currently supported. Defaults to 2C
snmp_version= <value>

*1 or more Object Names , comma delimited , in either textual(iso.org.dod.internet.mgmt.mib-2.system.sysDescr.0) or numerical(1.3.6.1.2.1.1.3.0) format.
object_names= <value>

*Whether or not to perform an SNMP GET BULK operation.This will retrieve all the object attributes in the sub tree of the declared OIDs.Be aware of potential performance issues , http://www.net-snmp.org/wiki/index.php/GETBULK. Defaults to false.
do_bulk_get= <value>

*The number of objects that are only expected to return a single GETNEXT instance, not multiple instances. Managers frequently request the value of sysUpTime and only want that instance plus a list of other objects.Defaults to 0. 
non_repeaters= <value>

*The number of objects that should be returned for all the repeating OIDs. Agent's must truncate the list to something shorter if it won't fit within the max-message size supported by the command generator or the agent.Defaults to 25.
max_repetitions= <value>

*Community String used for SNMP version 1 and 2C authentication.Defaults to "public"
communitystring= <value>

*How often to run the SNMP query (in seconds). Defaults to 60 seconds
snmpinterval= <value>

*Whether or not to listen for TRAP messages. Defaults to false
listen_traps= <value>

*The TRAP port to listen on. Defaults to 162
trap_port= <value>

*The trap host. Defaults to localhost
trap_host= <value>
