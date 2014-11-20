'''
Cisco Meraki Modular Input Script

Copyright (C) 2012 Splunk, Inc.
All Rights Reserved

'''

import sys,logging,json,signal
import xml.dom.minidom, xml.sax.saxutils
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import SocketServer
import urllib 

#set up logging
logging.root
logging.root.setLevel(logging.ERROR)
formatter = logging.Formatter('%(levelname)s %(message)s')
#with zero args , should go to STD ERR
handler = logging.StreamHandler()
handler.setFormatter(formatter)
logging.root.addHandler(handler)

SCHEME = """<scheme>
    <title>Cisco Meraki</title>
    <description>Cisco Meraki</description>
    <use_external_validation>true</use_external_validation>
    <streaming_mode>xml</streaming_mode>
    <use_single_instance>false</use_single_instance>

    <endpoint>
        <args>    
            <arg name="name">
                <title>Name of this Meraki input</title>
                <description>Name of this Meraki input</description>
            </arg>
                   
            <arg name="http_port">
                <title>HTTP Web Server Port</title>
                <description>Port on which to listen for incoming HTTP requests</description>
                <required_on_edit>false</required_on_edit>
                <required_on_create>true</required_on_create>
            </arg>
            <arg name="http_bind_address">
                <title>HTTP Web Server Bind Address</title>
                <description>Host address to bind to for this HTTP server</description>
                <required_on_edit>false</required_on_edit>
                <required_on_create>false</required_on_create>
            </arg>
            <arg name="meraki_secret">
                <title>Meraki Client Secret</title>
                <description>Meraki Client Secret</description>
                <required_on_edit>false</required_on_edit>
                <required_on_create>true</required_on_create>
            </arg>
            <arg name="meraki_validator">
                <title>Meraki Client Validator</title>
                <description>Meraki Client Validator</description>
                <required_on_edit>false</required_on_edit>
                <required_on_create>true</required_on_create>
            </arg>
            <arg name="api_version">
                <title>CMX API Version</title>
                <description>CMX API Version</description>
                <required_on_edit>false</required_on_edit>
                <required_on_create>true</required_on_create>
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
    global meraki_validator
    global meraki_secret
    global api_version

    config = get_input_config()  
    
    http_port=config.get("http_port",80)
    http_bind_address=config.get("http_bind_address",'')
    meraki_validator=config.get("meraki_validator")
    meraki_secret=config.get("meraki_secret")
    api_version=config.get("api_version","1.0")
    
    try :
        server_address = (http_bind_address, int(http_port))
        httpd = HTTPServer(server_address, MerakiHandler)
        httpd.serve_forever()   
    except: # catch *all* exceptions
        httpd.server_close()
        e = sys.exc_info()[1]
        logging.error("Error running the Meraki HTTP Server: %s" % str(e))
        sys.exit(0)  
 
class MerakiHandler(BaseHTTPRequestHandler):


    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
 
    def do_GET(self):
        if self.path == '/events' :
            try:
                self._set_headers()
                self.wfile.write(meraki_validator)
            except: # catch *all* exceptions
                e = sys.exc_info()[1]
                logging.error("Exception handling GET request for /events")
        else :    
            logging.error("GET path %s is not recognised" % self.path ) 
 
    def do_POST(self):
        if self.path == '/events' :
            try:
                content_len = int(self.headers.getheader('content-length'))
                post_body = self.rfile.read(content_len)
                post_body_decoded = urllib.unquote(post_body).decode("utf8")
                if api_version == '2.0':
                    content = json.loads(post_body_decoded)
                    request_secret = content["secret"]
                    if request_secret == meraki_secret :
                        for observation in content["data"]["observations"]:
                            observation["apMac"] = content["data"]["apMac"]
                            print_xml_stream(json.dumps(observation))
                            sys.stdout.flush()
                    else :    
                       logging.error("Request Secret %s does not match" % request_secret )        
                elif api_version == '1.0':        
                    post_params = dict((k.strip(), v.strip()) for k,v in (item.split('=') for item in post_body_decoded.split('&')))
                    content = json.loads(post_params["data"])
                    request_secret = content["secret"]
                    if request_secret == meraki_secret :
                        for probing_event in content["probing"]:
                            print_xml_stream(json.dumps(probing_event))
                            sys.stdout.flush()
                    else :    
                       logging.error("Request Secret %s does not match" % request_secret )
            except: # catch *all* exceptions
                e = sys.exc_info()[1]
                logging.error("Exception handling POST request for /events.Body Content : %s" % post_body)
        else :    
            logging.error("POST path %s is not recognised" % self.path )   



# prints validation error data to be consumed by Splunk
def print_validation_error(s):
    print "<error><message>%s</message></error>" % xml.sax.saxutils.escape(s)
    
# prints XML stream
def print_xml_stream(s):
    print "<stream><event unbroken=\"1\"><data>%s</data><done/></event></stream>" % encodeXMLText(s)



def encodeXMLText(text):
    text = text.replace("&", "&amp;")
    text = text.replace("\"", "&quot;")
    text = text.replace("'", "&apos;")
    text = text.replace("<", "&lt;")
    text = text.replace(">", "&gt;")
    text = text.replace("\n", "")
    return text
    
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

def signal_handler(signal, frame):
        #exit this script
        sys.exit(0)

        
signal.signal(signal.SIGINT, signal_handler)

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
