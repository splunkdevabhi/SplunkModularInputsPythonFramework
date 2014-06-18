'''
EMC CEPA Modular Input Script

Copyright (C) 2014 Splunk, Inc.
All Rights Reserved

'''

import sys,logging,traceback,urllib
import xml.dom.minidom, xml.sax.saxutils
from twisted.web import server, resource
from twisted.internet import reactor

#set up logging
logging.root
logging.root.setLevel(logging.ERROR)
formatter = logging.Formatter('%(levelname)s %(message)s')
#with zero args , should go to STD ERR
handler = logging.StreamHandler()
handler.setFormatter(formatter)
logging.root.addHandler(handler)

SCHEME = """<scheme>
    <title>EMC CEPA</title>
    <description>EMC CEPA</description>
    <use_external_validation>true</use_external_validation>
    <streaming_mode>xml</streaming_mode>
    <use_single_instance>false</use_single_instance>

    <endpoint>
        <args>    
            <arg name="name">
                <title>Name of this EMC CEPA input</title>
                <description>Name of this EMC CEPA input</description>
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
    
    http_port=config.get("http_port")
    http_bind_address=config.get("http_bind_address",'')
     
    try :
        reactor.listenTCP(int(http_port), server.Site(CepaResource()),interface=http_bind_address)
        reactor.run()
        
    except: # catch *all* exceptions
        e = sys.exc_info()[1]
        logging.error("Error running the CEPA HTTP Server: %s" % str(e))  


class CepaResource(resource.Resource):
    
    isLeaf = True
    
    def _ok_response(self, message,request):
        
        bytebuf = message.encode("utf-16")
        request.setResponseCode(200)
        request.setHeader('Content-Length', len(bytebuf))
        request.setHeader('Content-Type', 'text/xml; charset=utf-16')
        request.write(bytebuf)
 
    def render_GET(self,request):
        logging.error("GET method for path %s is not supported, docs specify PUT path" % request.path)
 
    def render_PUT(self,request):
        
        if request.path == '/':
            try:
                put_body = request.content.read()
                put_body_decoded = urllib.unquote(put_body).decode("utf-16")
                
                if '<RegisterRequest />' in put_body_decoded:
                    response_content = '<RegisterResponse><EndPoint guid="8bff877d-39bd-4b56-80ce-8b7884711d3f" friendlyName="Splunk" version="1.0" desc="CEPP Server AUDIT App" /><Filter protocol="0"><EventTypeFilter value="0xFFFFFFFFFFFFFFFFFFFFFFFF" adminEvents="0x80000000" /></Filter></RegisterResponse>'
                    self._ok_response(response_content,request)

                elif '<HeartBeatRequest />' in put_body_decoded:
                    response_content = 'hbStatus=0&xml=<HeartBeatResponse />'
                    self._ok_response(response_content,request)

                elif '<CheckEventRequest>' in put_body_decoded:
                    print_xml_stream(put_body_decoded)
                    sys.stdout.flush()
                    response_content = 'ntStatus=0&xml=<CheckEventResponse />'
                    self._ok_response(response_content,request)

                else:
                   logging.error("PUT request content is not supported: %s" % put_body_decoded)

            except: #catch *all* exceptions
                    #send errors to splunkd.log
                    e = sys.exc_info()[1]
                    logging.error("Exception handling PUT request.Body Content: %s" % put_body_decoded)
                    logging.error(traceback.format_exc())
        else:
            logging.error("PUT path %s is not recognized" % self.path)

    def render_POST(self,request):
        logging.error("POST method for path %s is not supported, docs specify PUT path" % request.path)  


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
