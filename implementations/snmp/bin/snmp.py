'''
Modular Input Script

Copyright (C) 2012 Splunk, Inc.
All Rights Reserved

'''

import os,sys,logging
import xml.dom.minidom, xml.sax.saxutils
import time


SPLUNK_HOME = os.environ.get("SPLUNK_HOME")
sys.path.append(SPLUNK_HOME + "/etc/apps/snmp_ta/bin/pyasn1-0.1.6-py2.7.egg")
sys.path.append(SPLUNK_HOME + "/etc/apps/snmp_ta/bin/pysnmp-4.2.4-py2.7.egg")
sys.path.append(SPLUNK_HOME + "/etc/apps/snmp_ta/bin/pysnmp_mibs-0.1.4-py2.7.egg")
from pysnmp.entity.rfc3413.oneliner import cmdgen

#set up logging
logging.root
logging.root.setLevel(logging.ERROR)
formatter = logging.Formatter('%(levelname)s %(message)s')
#with zero args , should go to STD ERR
handler = logging.StreamHandler()
handler.setFormatter(formatter)
logging.root.addHandler(handler)


SCHEME = """<scheme>
    <title>SNMP</title>
    <description>Poll attributes from a device's SNMP interface</description>
    <use_external_validation>true</use_external_validation>
    <streaming_mode>xml</streaming_mode>
    <use_single_instance>false</use_single_instance>

    <endpoint>
        <args>    
            <arg name="name">
                <title>SNMP Input Name</title>
                <description>Name of this SNMP input</description>
            </arg>                  
            <arg name="destination">
                <title>Destination</title>
                <description>IP or hostname of the device you would like to query</description>
                <required_on_edit>false</required_on_edit>
                <required_on_create>true</required_on_create>
            </arg>
            <arg name="ipv6">
                <title>IP Version 6</title>
                <description>Whether or not this is an IP version 6 address. Defaults to false</description>
                <required_on_edit>false</required_on_edit>
                <required_on_create>false</required_on_create>
            </arg>
            <arg name="port">
                <title>Port</title>
                <description>The SNMP port. Defaults to 161</description>
                <required_on_edit>false</required_on_edit>
                <required_on_create>false</required_on_create>
            </arg>
            <arg name="snmp_version">
                <title>SNMP Version</title>
                <description>The SNMP Version , 1 or 2C, version 3 not currently supported. Defaults to 2C</description>
                <required_on_edit>false</required_on_edit>
                <required_on_create>false</required_on_create>
            </arg>
            <arg name="object_names">
                <title>Object Names</title>
                <description>1 or more Objects Names , comma delimited , in either textual(iso.org.dod.internet.mgmt.mib-2.system.sysDescr.0) or numerical(1.3.6.1.2.1.1.3.0) format</description>
                <required_on_edit>true</required_on_edit>
                <required_on_create>true</required_on_create>
            </arg>
            <arg name="communitystring">
                <title>Community String</title>
                <description>Community String used for authentication.Defaults to "public"</description>
                <required_on_edit>false</required_on_edit>
                <required_on_create>false</required_on_create>
            </arg>
            <arg name="snmpinterval">
                <title>Interval</title>
                <description>How often to run the SNMP query (in seconds). Defaults to 60 seconds</description>
                <required_on_edit>false</required_on_edit>
                <required_on_create>false</required_on_create>
            </arg>
            <arg name="do_bulk_get">
                <title>Perform GET BULK</title>
                <description>Whether or not to perform an SNMP GET BULK operation.This will retrieve all the object attributes in the sub tree of the declared OIDs.Be aware of potential performance issues , http://www.net-snmp.org/wiki/index.php/GETBULK. Defaults to false</description>
                <required_on_edit>false</required_on_edit>
                <required_on_create>false</required_on_create>
            </arg>
            <arg name="non_repeaters">
                <title>Non Repeaters (for GET BULK)</title>
                <description>The number of objects that are only expected to return a single GETNEXT instance, not multiple instances. Managers frequently request the value of sysUpTime and only want that instance plus a list of other objects.Defaults to 0</description>
                <required_on_edit>false</required_on_edit>
                <required_on_create>false</required_on_create>
            </arg>
            <arg name="max_repetitions">
                <title>Max Repetitions (for GET BULK)</title>
                <description>The number of objects that should be returned for all the repeating OIDs. Agent's must truncate the list to something shorter if it won't fit within the max-message size supported by the command generator or the agent.Defaults to 25</description>
                <required_on_edit>false</required_on_edit>
                <required_on_create>false</required_on_create>
            </arg>
        </args>
    </endpoint>
</scheme>
"""

def do_validate():
    
    try:
        config = get_validation_config() 
        port=config.get("port")
        snmpinterval=config.get("snmpinterval")   
        max_repetitions=config.get("max_repetitions") 
        non_repeaters=config.get("non_repeaters") 
        
        validationFailed = False
    
        
        if not port is None and int(port) < 1:
            print_validation_error("Port value must be a positive integer")
            validationFailed = True
        if not non_repeaters is None and int(non_repeaters) < 0:
            print_validation_error("Non Repeaters value must be zero or a positive integer")
            validationFailed = True
        if not max_repetitions is None and int(max_repetitions) < 0:
            print_validation_error("Max Repetitions value must be zero or a positive integer")
            validationFailed = True
        if not snmpinterval is None and int(snmpinterval) < 1:
            print_validation_error("SNMP Polling interval must be a positive integer")
            validationFailed = True
        if validationFailed:
            sys.exit(2)
               
    except RuntimeError,e:
        logging.error("Looks like an error: %s" % str(e))
        sys.exit(1)
        raise   
     
    
def do_run():
    
    config = get_input_config() 
    #parameters with defaults
    destination=config.get("destination")
    port=int(config.get("port",161))
    communitystring=config.get("communitystring","public")
    snmpinterval=int(config.get("snmpinterval",60))   
    ipv6=int(config.get("ipv6",0))
    
    snmp_version=config.get("snmp_version","2C")
    mp_model_val=1
    if snmp_version == "1":
        mp_model_val=0
        
    
    object_names=config.get("object_names")
    oid_args = map(str,object_names.split(","))
    
    do_bulk=int(config.get("do_bulk_get",0))
    non_repeaters=int(config.get("non_repeaters",0))
    max_repetitions=int(config.get("max_repetitions",25))
        
    while True:      
        try:
            cmdGen = cmdgen.CommandGenerator()
         
            if ipv6:
                transport = cmdgen.Udp6TransportTarget((destination, port)) 
            else:
                transport = cmdgen.UdpTransportTarget((destination, port))  
                   
            if do_bulk and not snmp_version == "1":
                errorIndication, errorStatus, errorIndex, varBindTable = cmdGen.bulkCmd(
                cmdgen.CommunityData(communitystring,mpModel=mp_model_val),
                transport,
                non_repeaters, max_repetitions,
                *oid_args,lookupNames=True, lookupValues=True)
            else:
                errorIndication, errorStatus, errorIndex, varBinds = cmdGen.getCmd(
                cmdgen.CommunityData(communitystring,mpModel=mp_model_val),
                transport,
                *oid_args,
                lookupNames=True, lookupValues=True)
            
            
            if errorIndication:
                raise RuntimeError(errorIndication)
                logging.error(errorIndication)
            elif errorStatus:
                raise RuntimeError(errorStatus)
                logging.error(errorStatus)
            else:
                splunkevent =""
                
                if do_bulk:
                    for varBindTableRow in varBindTable:
                        for name, val in varBindTableRow:
                            splunkevent += '%s = "%s" ' % (name.prettyPrint(), val.prettyPrint()) 
                else:    
                    for name, val in varBinds:
                        splunkevent += '%s = "%s" ' % (name.prettyPrint(), val.prettyPrint())
                   
                   
                    
                print_xml_single_instance_mode(splunkevent)
                sys.stdout.flush()
                
            
            
            
        except RuntimeError,e:
            logging.error("Looks like an error: %s" % str(e))
            sys.exit(1)
            raise    
                    
        time.sleep(float(snmpinterval))
        

# prints validation error data to be consumed by Splunk
def print_validation_error(s):
    print "<error><message>%s</message></error>" % xml.sax.saxutils.escape(s)
    
# prints XML stream
def print_xml_single_instance_mode(s):
    print "<stream><event><data>%s</data></event></stream>" % xml.sax.saxutils.escape(s)
    
# prints XML stream
def print_xml_multi_instance_mode(s,stanza):
    print "<stream><event stanza=""%s""><data>%s</data></event></stream>" % stanza,xml.sax.saxutils.escape(s)
    
# prints simple stream
def print_simple(s):
    print "%s\n" % s
    
def usage():
    print "usage: %s [--scheme|--validate-arguments]"
    logging.error("Incorrect Program Usage")
    sys.exit(2)

def do_scheme():
    print SCHEME

#read XML configuration passed from splunkd, need to refactor to support single instance mode
def get_input_config():
    config = {}

    try:
        # read everything from stdin
        config_str = sys.stdin.read()

        # parse the config XML
        doc = xml.dom.minidom.parseString(config_str)
        root = doc.documentElement
        conf_node = root.getElementsByTagName("configuration")[0]
        if conf_node:
            logging.debug("XML: found configuration")
            stanza = conf_node.getElementsByTagName("stanza")[0]
            if stanza:
                stanza_name = stanza.getAttribute("name")
                if stanza_name:
                    logging.debug("XML: found stanza " + stanza_name)
                    config["name"] = stanza_name

                    params = stanza.getElementsByTagName("param")
                    for param in params:
                        param_name = param.getAttribute("name")
                        logging.debug("XML: found param '%s'" % param_name)
                        if param_name and param.firstChild and \
                           param.firstChild.nodeType == param.firstChild.TEXT_NODE:
                            data = param.firstChild.data
                            config[param_name] = data
                            logging.debug("XML: '%s' -> '%s'" % (param_name, data))

        checkpnt_node = root.getElementsByTagName("checkpoint_dir")[0]
        if checkpnt_node and checkpnt_node.firstChild and \
           checkpnt_node.firstChild.nodeType == checkpnt_node.firstChild.TEXT_NODE:
            config["checkpoint_dir"] = checkpnt_node.firstChild.data

        if not config:
            raise Exception, "Invalid configuration received from Splunk."

        
    except Exception, e:
        raise Exception, "Error getting Splunk configuration via STDIN: %s" % str(e)

    return config

#read XML configuration passed from splunkd, need to refactor to support single instance mode
def get_validation_config():
    val_data = {}

    # read everything from stdin
    val_str = sys.stdin.read()

    # parse the validation XML
    doc = xml.dom.minidom.parseString(val_str)
    root = doc.documentElement

    logging.debug("XML: found items")
    item_node = root.getElementsByTagName("item")[0]
    if item_node:
        logging.debug("XML: found item")

        name = item_node.getAttribute("name")
        val_data["stanza"] = name

        params_node = item_node.getElementsByTagName("param")
        for param in params_node:
            name = param.getAttribute("name")
            logging.debug("Found param %s" % name)
            if name and param.firstChild and \
               param.firstChild.nodeType == param.firstChild.TEXT_NODE:
                val_data[name] = param.firstChild.data

    return val_data

if __name__ == '__main__':
      
    if len(sys.argv) > 1:
        if sys.argv[1] == "--scheme":           
            do_scheme()
        elif sys.argv[1] == "--validate-arguments":
            do_validate()
        else:
            usage()
    else:
        do_run()
        
    sys.exit(0)