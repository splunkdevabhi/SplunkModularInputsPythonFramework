'''
Tesla Modular Input Script

Copyright (C) 2012 Splunk, Inc.
All Rights Reserved

'''

import sys, logging, os, time, re
import xml.dom.minidom

SPLUNK_HOME = os.environ.get("SPLUNK_HOME")

RESPONSE_HANDLER_INSTANCE = None
SPLUNK_PORT = 8089
STANZA = None
SESSION_TOKEN = None
REGEX_PATTERN = None

#dynamically load in any eggs in /etc/apps/tesla_ta/bin
EGG_DIR = SPLUNK_HOME + "/etc/apps/tesla_ta/bin/"

for filename in os.listdir(EGG_DIR):
    if filename.endswith(".egg"):
        sys.path.append(EGG_DIR + filename) 
       
import requests, json
from splunklib.client import connect
from splunklib.client import Service

           
#set up logging
logging.root
logging.root.setLevel(logging.ERROR)
formatter = logging.Formatter('%(levelname)s %(message)s')
#with zero args , should go to STD ERR
handler = logging.StreamHandler()
handler.setFormatter(formatter)
logging.root.addHandler(handler)

SCHEME = """<scheme>
    <title>Tesla</title>
    <description>Tesla input for polling data from My Tesla</description>
    <use_external_validation>true</use_external_validation>
    <streaming_mode>xml</streaming_mode>
    <use_single_instance>false</use_single_instance>

    <endpoint>
        <args>    
            <arg name="name">
                <title>Tesla input name</title>
                <description>Name of this Tesla input</description>
            </arg> 
            <arg name="vehicle_id">
                <title>Tesla Vehicle ID</title>
                <description>Tesla Vehicle ID</description>
                <required_on_edit>false</required_on_edit>
                <required_on_create>false</required_on_create>
            </arg> 
            <arg name="api_base">
                <title>Base URL</title>
                <description>Base URL to send the HTTP GET request to</description>
                <required_on_edit>false</required_on_edit>
                <required_on_create>true</required_on_create>
            </arg>                  
            <arg name="endpoint">
                <title>Endpoint Path</title>
                <description>Endpoint Path to send the HTTP GET request to</description>
                <required_on_edit>false</required_on_edit>
                <required_on_create>true</required_on_create>
            </arg>
            <arg name="user">
                <title>My Tesla User</title>
                <description>My Tesla User</description>
                <required_on_edit>false</required_on_edit>
                <required_on_create>true</required_on_create>
            </arg>
            <arg name="password">
                <title>My Tesla Password</title>
                <description>My Tesla Password</description>
                <required_on_edit>false</required_on_edit>
                <required_on_create>true</required_on_create>
            </arg>
            <arg name="cookie_s_portal_session">
                <title>Session Cookie</title>
                <description>Session Cookie</description>
                <required_on_edit>false</required_on_edit>
                <required_on_create>false</required_on_create>
            </arg>
            <arg name="cookie_user_credentials">
                <title>Credentials Cookie</title>
                <description>Credentials Cookie</description>
                <required_on_edit>false</required_on_edit>
                <required_on_create>false</required_on_create>
            </arg>
            <arg name="http_proxy">
                <title>HTTP Proxy Address</title>
                <description>HTTP Proxy Address</description>
                <required_on_edit>false</required_on_edit>
                <required_on_create>false</required_on_create>
            </arg>
            <arg name="https_proxy">
                <title>HTTPs Proxy Address</title>
                <description>HTTPs Proxy Address</description>
                <required_on_edit>false</required_on_edit>
                <required_on_create>false</required_on_create>
            </arg>
            <arg name="request_timeout">
                <title>Request Timeout</title>
                <description>Request Timeout in seconds</description>
                <required_on_edit>false</required_on_edit>
                <required_on_create>false</required_on_create>
            </arg>
            <arg name="backoff_time">
                <title>Backoff Time</title>
                <description>Time in seconds to wait for retry after error or timeout</description>
                <required_on_edit>false</required_on_edit>
                <required_on_create>false</required_on_create>
            </arg>
            <arg name="polling_interval">
                <title>Polling Interval</title>
                <description>Interval time in seconds to poll the endpoint</description>
                <required_on_edit>false</required_on_edit>
                <required_on_create>false</required_on_create>
            </arg>
            <arg name="index_error_response_codes">
                <title>Index Error Responses</title>
                <description>Whether or not to index error response codes : true | false</description>
                <required_on_edit>false</required_on_edit>
                <required_on_create>false</required_on_create>
            </arg>
            <arg name="response_handler">
                <title>Response Handler</title>
                <description>Python classname of custom response handler</description>
                <required_on_edit>false</required_on_edit>
                <required_on_create>false</required_on_create>
            </arg>
            <arg name="response_handler_args">
                <title>Response Handler Arguments</title>
                <description>Response Handler arguments string ,  key=value,key2=value2</description>
                <required_on_edit>false</required_on_edit>
                <required_on_create>false</required_on_create>
            </arg>
            <arg name="response_filter_pattern">
                <title>Response Filter Pattern</title>
                <description>Python Regex pattern, if present , responses must match this pattern to be indexed</description>
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
    
    #setup some globals
    server_uri = config.get("server_uri")
    global SPLUNK_PORT
    global STANZA
    global SESSION_TOKEN 
    SPLUNK_PORT = server_uri[18:]
    STANZA = config.get("name")
    SESSION_TOKEN = config.get("session_key")
   
    #params
    
    vehicle_id = config.get("vehicle_id")
    api_base = config.get("api_base")
    api_path = config.get("endpoint")
    
    if vehicle_id:
        api_path_resolved = api_path.replace('{vehicle_id}', vehicle_id);
        endpoint = api_base + api_path_resolved
    else:
        endpoint = api_base + api_path

    http_method = config.get("http_method", "GET")
    
    
    user = config.get("user")
    password = config.get("password")
    
    cookie_s_portal_session = config.get("cookie_s_portal_session")
    cookie_user_credentials = config.get("cookie_user_credentials")

   
    response_type = config.get("response_type", "json")
    
    http_proxy = config.get("http_proxy")
    https_proxy = config.get("https_proxy")
    
    proxies = {}
    
    if not http_proxy is None:
        proxies["http"] = http_proxy   
    if not https_proxy is None:
        proxies["https"] = https_proxy 
        
    
    request_timeout = int(config.get("request_timeout", 30))
    
    backoff_time = int(config.get("backoff_time", 10))
    
    polling_interval = int(config.get("polling_interval", 60))
    
    index_error_response_codes = int(config.get("index_error_response_codes", 0))
    
    response_filter_pattern = config.get("response_filter_pattern")
    
    if response_filter_pattern:
        global REGEX_PATTERN
        REGEX_PATTERN = re.compile(response_filter_pattern)
        
    response_handler_args = {} 
    response_handler_args_str = config.get("response_handler_args")
    if not response_handler_args_str is None:
        response_handler_args = dict((k.strip(), v.strip()) for k, v in 
              (item.split('=') for item in response_handler_args_str.split(delimiter)))
        
    response_handler = config.get("response_handler", "DefaultResponseHandler")
    module = __import__("responsehandlers")
    class_ = getattr(module, response_handler)

    global RESPONSE_HANDLER_INSTANCE
    RESPONSE_HANDLER_INSTANCE = class_(**response_handler_args)
   

    try: 
            
        req_args = {"verify" : False , "timeout" : float(request_timeout)}

        
        if proxies:
            req_args["proxies"] = proxies

        cookies = {}
        if cookie_s_portal_session and cookie_user_credentials:
            cookies = {'_s_portal_session':cookie_s_portal_session, 'user_credentials':cookie_user_credentials} 
            req_args["cookies"] = cookies
                         
                    
        while True:
                        
            if "cookies" in req_args:
                req_args_cookies_current = dictParameterToStringFormat(req_args["cookies"])
            else:
                req_args_cookies_current = ""
            
             
            try:

                if not "cookies" in req_args:
                    
                    #requests will role this out into form url encoded format
                    req_args['data'] = {'user_session[email]':user, 'user_session[password]':password}
                    login_url = api_base + '/login'
                    #perform auth request
                    r = requests.post(login_url, **req_args)
                    
                    #get the auth cookies
                    credentials_cookie = r.cookies['user_credentials'] 
                    session_cookie = r.cookies['_s_portal_session']
                    del req_args['data']
                    
                    #set the auth cookies for API requests
                    cookies = {'_s_portal_session':session_cookie, 'user_credentials':credentials_cookie} 
                    req_args['cookies'] = cookies
                    
                #perform API request
                r = requests.get(endpoint, **req_args)
                
            except requests.exceptions.Timeout, e:
                logging.error("HTTP Request Timeout error: %s" % str(e))
                time.sleep(float(backoff_time))
                continue
            except Exception as e:
                logging.error("Exception performing request: %s" % str(e))
                time.sleep(float(backoff_time))
                continue
            try:
                r.raise_for_status()
                handle_output(r, r.text, response_type, req_args, endpoint)
            except requests.exceptions.HTTPError, e:
                #reset for reauth
                if 'cookies' in req_args:
                    del req_args['cookies']
                error_output = r.text
                error_http_code = r.status_code
                if index_error_response_codes:
                    error_event = ""
                    error_event += 'http_error_code = %s error_message = %s' % (error_http_code, error_output) 
                    print_xml_single_instance_mode(error_event)
                    sys.stdout.flush()
                logging.error("HTTP Request error: %s" % str(e))
                time.sleep(float(backoff_time))
                continue
            
            
            if "cookies" in req_args:   
                checkCookiesUpdated(req_args_cookies_current, dictParameterToStringFormat(req_args["cookies"]), req_args["cookies"])
                              
            time.sleep(float(polling_interval))
            
    except RuntimeError, e:
        logging.error("Looks like an error: %s" % str(e))
        sys.exit(2) 
     
def checkCookiesUpdated(cached, current, cookies):
    
    if not (cached == current):
        try:
            args = {'host':'localhost', 'port':SPLUNK_PORT, 'token':SESSION_TOKEN}
            service = Service(**args)   
            item = service.inputs.__getitem__(STANZA[8:])
            item.update(**{'cookie_s_portal_session':cookies['_s_portal_session'], 'cookie_user_credentials':cookies['user_credentials']})
        except RuntimeError, e:
            logging.error("Looks like an error updating the modular input parameter cookies")   
        
                       
def dictParameterToStringFormat(parameter):
    
    if parameter:
        return ''.join('{}={},'.format(key, val) for key, val in parameter.items())[:-1] 
    else:
        return None
    
            
def handle_output(response, output, type, req_args, endpoint): 
    
    try:
        if REGEX_PATTERN:
            search_result = REGEX_PATTERN.search(output)
            if search_result == None:
                return   
        RESPONSE_HANDLER_INSTANCE(response, output, type, req_args, endpoint)
        sys.stdout.flush()               
    except RuntimeError, e:
        logging.error("Looks like an error handle the response output: %s" % str(e))

# prints validation error data to be consumed by Splunk
def print_validation_error(s):
    print "<error><message>%s</message></error>" % encodeXMLText(s)
    
# prints XML stream
def print_xml_single_instance_mode(s):
    print "<stream><event><data>%s</data></event></stream>" % encodeXMLText(s)
    
# prints simple stream
def print_simple(s):
    print "%s\n" % s

def encodeXMLText(text):
    text = text.replace("&", "&amp;")
    text = text.replace("\"", "&quot;")
    text = text.replace("'", "&apos;")
    text = text.replace("<", "&lt;")
    text = text.replace(">", "&gt;")
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
        
        session_key_node = root.getElementsByTagName("session_key")[0]
        if session_key_node and session_key_node.firstChild and session_key_node.firstChild.nodeType == session_key_node.firstChild.TEXT_NODE:
            data = session_key_node.firstChild.data
            config["session_key"] = data 
            
        server_uri_node = root.getElementsByTagName("server_uri")[0]
        if server_uri_node and server_uri_node.firstChild and server_uri_node.firstChild.nodeType == server_uri_node.firstChild.TEXT_NODE:
            data = server_uri_node.firstChild.data
            config["server_uri"] = data   
            
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
