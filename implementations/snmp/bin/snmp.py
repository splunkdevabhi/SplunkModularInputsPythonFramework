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
            <arg name="port">
                <title>Port</title>
                <description>The SNMP port. Defaults to 161</description>
                <required_on_edit>false</required_on_edit>
                <required_on_create>false</required_on_create>
            </arg>
            <arg name="mib">
                <title>MIB</title>
                <description>The MIB that contains the OID to query. Defaults to "SNMPv2-MIB"</description>
                <required_on_edit>false</required_on_edit>
                <required_on_create>false</required_on_create>
            </arg>
            <arg name="oid">
                <title>OID</title>
                <description>The OID that you want to query. Defaults to "sysDescr"</description>
                <required_on_edit>false</required_on_edit>
                <required_on_create>false</required_on_create>
            </arg>
            <arg name="snmpindex">
                <title>SNMP Index</title>
                <description>The index of the OID to query. Defaults to 0</description>
                <required_on_edit>false</required_on_edit>
                <required_on_create>false</required_on_create>
            </arg>
            <arg name="communitystring">
                <title>Community String</title>
                <description>Community String used for authentication</description>
                <required_on_edit>false</required_on_edit>
                <required_on_create>true</required_on_create>
            </arg>
            <arg name="snmpinterval">
                <title>Interval</title>
                <description>How often to run the SNMP query (in seconds). Defaults to 60 seconds</description>
                <required_on_edit>false</required_on_edit>
                <required_on_create>false</required_on_create>
            </arg>
            
        </args>
    </endpoint>
</scheme>
"""

def do_validate():
    config = get_validation_config() 
    #TODO
    #if error , print_validation_error & sys.exit(2) 
    
def do_run():
    
    config = get_input_config() 
    #parameters with defaults
    destination=config.get("destination")
    port=config.get("port",161)
    mib=config.get("mib","SNMPv2-MIB")
    oid=config.get("oid","sysDescr")
    snmpindex=config.get("snmpindex",0)
    communitystring=config.get("communitystring","public")
    snmpinterval=config.get("snmpinterval",60)     
    
    while True:      
        try:
            cmdGen = cmdgen.CommandGenerator()
        
            
            errorIndication, errorStatus, errorIndex, varBinds = cmdGen.getCmd(
                cmdgen.CommunityData(communitystring),
                cmdgen.UdpTransportTarget((destination, port)),
                cmdgen.MibVariable(mib, oid, snmpindex),
                '.1.3.6.1.2.1.1.3.0',
                lookupNames=True, lookupValues=True
            )
            if errorIndication:
                raise RuntimeError(errorIndication)
                logging.error(errorIndication)
            elif errorStatus:
                raise RuntimeError(errorStatus)
                logging.error(errorStatus)
            else:
                splunkevent =""
                
                for name, val in varBinds:
                    splunkevent += '%s = "%s" ' % (name.prettyPrint(), val.prettyPrint())
                    
                print_xml_single_instance_mode(splunkevent)
                sys.stdout.flush()

        except RuntimeError:
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