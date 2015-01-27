'''
Modular Input Script

Copyright (C) 2012 Splunk, Inc.
All Rights Reserved

'''

import sys,logging,os,time,re
import xml.dom.minidom
import tokens

SPLUNK_HOME = os.environ.get("SPLUNK_HOME")

RESPONSE_HANDLER_INSTANCE = None
SPLUNK_PORT = 8089
STANZA = None
SESSION_TOKEN = None
REGEX_PATTERN = None

#dynamically load in any eggs in /etc/apps/snmp_ta/bin
EGG_DIR = SPLUNK_HOME + "/etc/apps/rest_ta/bin/"

for filename in os.listdir(EGG_DIR):
    if filename.endswith(".egg"):
        sys.path.append(EGG_DIR + filename) 
       
import requests,json
from requests.auth import HTTPBasicAuth
from requests.auth import HTTPDigestAuth
from requests_oauthlib import OAuth1
from requests_oauthlib import OAuth2Session
from oauthlib.oauth2 import WebApplicationClient 
from requests.auth import AuthBase
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
    <title>REST</title>
    <description>REST API input for polling data from RESTful endpoints</description>
    <use_external_validation>true</use_external_validation>
    <streaming_mode>xml</streaming_mode>
    <use_single_instance>false</use_single_instance>

    <endpoint>
        <args>    
            <arg name="name">
                <title>REST input name</title>
                <description>Name of this REST input</description>
            </arg>
                   
            <arg name="endpoint">
                <title>Endpoint URL</title>
                <description>URL to send the HTTP GET request to</description>
                <required_on_edit>false</required_on_edit>
                <required_on_create>true</required_on_create>
            </arg>
            <arg name="http_method">
                <title>HTTP Method</title>
                <description>HTTP method to use.Defaults to GET. POST and PUT are not really RESTful for requesting data from the API, but useful to have the option for target APIs that are "REST like"</description>
                <required_on_edit>false</required_on_edit>
                <required_on_create>false</required_on_create>
            </arg>
            <arg name="request_payload">
                <title>Request Payload</title>
                <description>Request payload for POST and PUT HTTP Methods</description>
                <required_on_edit>false</required_on_edit>
                <required_on_create>false</required_on_create>
            </arg>
            <arg name="auth_type">
                <title>Authentication Type</title>
                <description>Authentication method to use : none | basic | digest | oauth1 | oauth2 | custom</description>
                <required_on_edit>false</required_on_edit>
                <required_on_create>true</required_on_create>
            </arg>
            <arg name="auth_user">
                <title>Authentication User</title>
                <description>Authentication user for BASIC or DIGEST auth</description>
                <required_on_edit>false</required_on_edit>
                <required_on_create>false</required_on_create>
            </arg>
            <arg name="auth_password">
                <title>Authentication Password</title>
                <description>Authentication password for BASIC or DIGEST auth</description>
                <required_on_edit>false</required_on_edit>
                <required_on_create>false</required_on_create>
            </arg>
            <arg name="oauth1_client_key">
                <title>OAUTH 1 Client Key</title>
                <description>OAUTH 1 client key</description>
                <required_on_edit>false</required_on_edit>
                <required_on_create>false</required_on_create>
            </arg>
            <arg name="oauth1_client_secret">
                <title>OAUTH 1 Client Secret</title>
                <description>OAUTH 1 client secret</description>
                <required_on_edit>false</required_on_edit>
                <required_on_create>false</required_on_create>
            </arg>
            <arg name="oauth1_access_token">
                <title>OAUTH 1 Access Token</title>
                <description>OAUTH 1 access token</description>
                <required_on_edit>false</required_on_edit>
                <required_on_create>false</required_on_create>
            </arg>
            <arg name="oauth1_access_token_secret">
                <title>OAUTH 1 Access Token Secret</title>
                <description>OAUTH 1 access token secret</description>
                <required_on_edit>false</required_on_edit>
                <required_on_create>false</required_on_create>
            </arg>
            <arg name="oauth2_token_type">
                <title>OAUTH 2 Token Type</title>
                <description>OAUTH 2 token type</description>
                <required_on_edit>false</required_on_edit>
                <required_on_create>false</required_on_create>
            </arg>
            <arg name="oauth2_access_token">
                <title>OAUTH 2 Access Token</title>
                <description>OAUTH 2 access token</description>
                <required_on_edit>false</required_on_edit>
                <required_on_create>false</required_on_create>
            </arg>
            <arg name="oauth2_refresh_token">
                <title>OAUTH 2 Refresh Token</title>
                <description>OAUTH 2 refresh token</description>
                <required_on_edit>false</required_on_edit>
                <required_on_create>false</required_on_create>
            </arg>
            <arg name="oauth2_refresh_url">
                <title>OAUTH 2 Token Refresh URL</title>
                <description>OAUTH 2 token refresh URL</description>
                <required_on_edit>false</required_on_edit>
                <required_on_create>false</required_on_create>
            </arg>
            <arg name="oauth2_refresh_props">
                <title>OAUTH 2 Token Refresh Propertys</title>
                <description>OAUTH 2 token refresh propertys : key=value,key2=value2</description>
                <required_on_edit>false</required_on_edit>
                <required_on_create>false</required_on_create>
            </arg>
            <arg name="oauth2_client_id">
                <title>OAUTH 2 Client ID</title>
                <description>OAUTH 2 client ID</description>
                <required_on_edit>false</required_on_edit>
                <required_on_create>false</required_on_create>
            </arg>
            <arg name="oauth2_client_secret">
                <title>OAUTH 2 Client Secret</title>
                <description>OAUTH 2 client secret</description>
                <required_on_edit>false</required_on_edit>
                <required_on_create>false</required_on_create>
            </arg>
            <arg name="http_header_propertys">
                <title>HTTP Header Propertys</title>
                <description>Custom HTTP header propertys : key=value,key2=value2</description>
                <required_on_edit>false</required_on_edit>
                <required_on_create>false</required_on_create>
            </arg>
            <arg name="url_args">
                <title>URL Arguments</title>
                <description>Custom URL arguments : key=value,key2=value2</description>
                <required_on_edit>false</required_on_edit>
                <required_on_create>false</required_on_create>
            </arg>
            <arg name="response_type">
                <title>Response Type</title>
                <description>Rest Data Response Type : json | xml | text</description>
                <required_on_edit>false</required_on_edit>
                <required_on_create>false</required_on_create>
            </arg>
            <arg name="streaming_request">
                <title>Streaming Request</title>
                <description>Whether or not this is a HTTP streaming request : true | false</description>
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
            <arg name="delimiter">
                <title>Delimiter</title>
                <description>Delimiter to use for any multi "key=value" field inputs</description>
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
            <arg name="custom_auth_handler">
                <title>Custom_Auth Handler</title>
                <description>Python classname of custom auth handler</description>
                <required_on_edit>false</required_on_edit>
                <required_on_create>false</required_on_create>
            </arg>
            <arg name="custom_auth_handler_args">
                <title>Custom_Auth Handler Arguments</title>
                <description>Custom Authentication Handler arguments string ,  key=value,key2=value2</description>
                <required_on_edit>false</required_on_edit>
                <required_on_create>false</required_on_create>
            </arg>
            <arg name="cookies">
                <title>Cookies</title>
                <description>Persist cookies in format key=value,key2=value2,...</description>
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
    
    original_endpoint=config.get("endpoint")
    
    http_method=config.get("http_method","GET")
    request_payload=config.get("request_payload")
    
    #none | basic | digest | oauth1 | oauth2
    auth_type=config.get("auth_type","none")
    
    #Delimiter to use for any multi "key=value" field inputs
    delimiter=config.get("delimiter",",")
    
    #for basic and digest
    auth_user=config.get("auth_user")
    auth_password=config.get("auth_password")
    
    #for oauth1
    oauth1_client_key=config.get("oauth1_client_key")
    oauth1_client_secret=config.get("oauth1_client_secret")
    oauth1_access_token=config.get("oauth1_access_token")
    oauth1_access_token_secret=config.get("oauth1_access_token_secret")
    
    #for oauth2
    oauth2_token_type=config.get("oauth2_token_type","Bearer")
    oauth2_access_token=config.get("oauth2_access_token")
    
    oauth2_refresh_token=config.get("oauth2_refresh_token")
    oauth2_refresh_url=config.get("oauth2_refresh_url")
    oauth2_refresh_props_str=config.get("oauth2_refresh_props")
    oauth2_client_id=config.get("oauth2_client_id")
    oauth2_client_secret=config.get("oauth2_client_secret")
    
    oauth2_refresh_props={}
    if not oauth2_refresh_props_str is None:
        oauth2_refresh_props = dict((k.strip(), v.strip()) for k,v in 
              (item.split('=',1) for item in oauth2_refresh_props_str.split(delimiter)))
    oauth2_refresh_props['client_id'] = oauth2_client_id
    oauth2_refresh_props['client_secret'] = oauth2_client_secret
        
    http_header_propertys={}
    http_header_propertys_str=config.get("http_header_propertys")
    if not http_header_propertys_str is None:
        http_header_propertys = dict((k.strip(), v.strip()) for k,v in 
              (item.split('=',1) for item in http_header_propertys_str.split(delimiter)))
       
    url_args={} 
    url_args_str=config.get("url_args")
    if not url_args_str is None:
        url_args = dict((k.strip(), v.strip()) for k,v in 
              (item.split('=',1) for item in url_args_str.split(delimiter)))
        
    #json | xml | text    
    response_type=config.get("response_type","text")
    
    streaming_request=int(config.get("streaming_request",0))
    
    http_proxy=config.get("http_proxy")
    https_proxy=config.get("https_proxy")
    
    proxies={}
    
    if not http_proxy is None:
        proxies["http"] = http_proxy   
    if not https_proxy is None:
        proxies["https"] = https_proxy 
        
    cookies={} 
    cookies_str=config.get("cookies")
    if not cookies_str is None:
        cookies = dict((k.strip(), v.strip()) for k,v in 
              (item.split('=',1) for item in cookies_str.split(delimiter)))
        
    request_timeout=int(config.get("request_timeout",30))
    
    backoff_time=int(config.get("backoff_time",10))
    
    polling_interval=int(config.get("polling_interval",60))
    
    index_error_response_codes=int(config.get("index_error_response_codes",0))
    
    response_filter_pattern=config.get("response_filter_pattern")
    
    if response_filter_pattern:
        global REGEX_PATTERN
        REGEX_PATTERN = re.compile(response_filter_pattern)
        
    response_handler_args={} 
    response_handler_args_str=config.get("response_handler_args")
    if not response_handler_args_str is None:
        response_handler_args = dict((k.strip(), v.strip()) for k,v in 
              (item.split('=',1) for item in response_handler_args_str.split(delimiter)))
        
    response_handler=config.get("response_handler","DefaultResponseHandler")
    module = __import__("responsehandlers")
    class_ = getattr(module,response_handler)

    global RESPONSE_HANDLER_INSTANCE
    RESPONSE_HANDLER_INSTANCE = class_(**response_handler_args)
   
    custom_auth_handler=config.get("custom_auth_handler")
    
    if custom_auth_handler:
        module = __import__("authhandlers")
        class_ = getattr(module,custom_auth_handler)
        custom_auth_handler_args={} 
        custom_auth_handler_args_str=config.get("custom_auth_handler_args")
        if not custom_auth_handler_args_str is None:
            custom_auth_handler_args = dict((k.strip(), v.strip()) for k,v in (item.split('=',1) for item in custom_auth_handler_args_str.split(delimiter)))
        CUSTOM_AUTH_HANDLER_INSTANCE = class_(**custom_auth_handler_args)
    
    
    try: 
        auth=None
        oauth2=None
        if auth_type == "basic":
            auth = HTTPBasicAuth(auth_user, auth_password)
        elif auth_type == "digest":
            auth = HTTPDigestAuth(auth_user, auth_password)
        elif auth_type == "oauth1":
            auth = OAuth1(oauth1_client_key, oauth1_client_secret,
                  oauth1_access_token ,oauth1_access_token_secret)
        elif auth_type == "oauth2":
            token={}
            token["token_type"] = oauth2_token_type
            token["access_token"] = oauth2_access_token
            token["refresh_token"] = oauth2_refresh_token
            token["expires_in"] = "5"
            client = WebApplicationClient(oauth2_client_id)
            oauth2 = OAuth2Session(client, token=token,auto_refresh_url=oauth2_refresh_url,auto_refresh_kwargs=oauth2_refresh_props,token_updater=oauth2_token_updater)
        elif auth_type == "custom" and CUSTOM_AUTH_HANDLER_INSTANCE:
            auth = CUSTOM_AUTH_HANDLER_INSTANCE
   
        req_args = {"verify" : False ,"stream" : bool(streaming_request) , "timeout" : float(request_timeout)}

        if auth:
            req_args["auth"]= auth
        if url_args:
            req_args["params"]= url_args
        if cookies:
            req_args["cookies"]= cookies
        if http_header_propertys:
            req_args["headers"]= http_header_propertys
        if proxies:
            req_args["proxies"]= proxies
        if request_payload and not http_method == "GET":
            req_args["data"]= request_payload
                          
                    
        while True:
                        
            if "params" in req_args:
                req_args_params_current = dictParameterToStringFormat(req_args["params"])
            else:
                req_args_params_current = ""
            if "cookies" in req_args:
                req_args_cookies_current = dictParameterToStringFormat(req_args["cookies"])
            else:
                req_args_cookies_current = ""    
            if "headers" in req_args: 
                req_args_headers_current = dictParameterToStringFormat(req_args["headers"])
            else:
                req_args_headers_current = ""
            if "data" in req_args:
                req_args_data_current = req_args["data"]
            else:
                req_args_data_current = ""
            
            #token replacement
            endpoint = replaceTokens(original_endpoint)
         
            try:
                if oauth2:
                    if http_method == "GET":
                        r = oauth2.get(endpoint,**req_args)
                    elif http_method == "POST":
                        r = oauth2.post(endpoint,**req_args) 
                    elif http_method == "PUT":
                        r = oauth2.put(endpoint,**req_args)       
                else:
                    if http_method == "GET":
                        r = requests.get(endpoint,**req_args)
                    elif http_method == "POST":
                        r = requests.post(endpoint,**req_args) 
                    elif http_method == "PUT":
                        r = requests.put(endpoint,**req_args) 
                        
            except requests.exceptions.Timeout,e:
                logging.error("HTTP Request Timeout error: %s" % str(e))
                time.sleep(float(backoff_time))
                continue
            except Exception as e:
                logging.error("Exception performing request: %s" % str(e))
                time.sleep(float(backoff_time))
                continue
            try:
                r.raise_for_status()
                if streaming_request:
                    for line in r.iter_lines():
                        if line:
                            handle_output(r,line,response_type,req_args,endpoint)  
                else:                    
                    handle_output(r,r.text,response_type,req_args,endpoint)
            except requests.exceptions.HTTPError,e:
                error_output = r.text
                error_http_code = r.status_code
                if index_error_response_codes:
                    error_event=""
                    error_event += 'http_error_code = %s error_message = %s' % (error_http_code, error_output) 
                    print_xml_single_instance_mode(error_event)
                    sys.stdout.flush()
                logging.error("HTTP Request error: %s" % str(e))
                time.sleep(float(backoff_time))
                continue
            
            
            if "data" in req_args:   
                checkParamUpdated(req_args_data_current,req_args["data"],"request_payload")
            if "params" in req_args:
                checkParamUpdated(req_args_params_current,dictParameterToStringFormat(req_args["params"]),"url_args")
            if "headers" in req_args:
                checkParamUpdated(req_args_headers_current,dictParameterToStringFormat(req_args["headers"]),"http_header_propertys")
            if "cookies" in req_args:
                checkParamUpdated(req_args_cookies_current,dictParameterToStringFormat(req_args["cookies"]),"cookies")
                                 
            time.sleep(float(polling_interval))
            
    except RuntimeError,e:
        logging.error("Looks like an error: %s" % str(e))
        sys.exit(2) 

def replaceTokens(raw_string):

    try:    
        substitution_tokens = re.findall("\$(?:\w+)\$",raw_string)
        for token in substitution_tokens:
            raw_string =  raw_string.replace(token,getattr(tokens,token[1:-1])())
        return raw_string    
    except: 
        e = sys.exc_info()[1]
        logging.error("Looks like an error substituting tokens: %s" % str(e))  
               
         
def checkParamUpdated(cached,current,rest_name):
    
    if not (cached == current):
        try:
            args = {'host':'localhost','port':SPLUNK_PORT,'token':SESSION_TOKEN}
            service = Service(**args)   
            item = service.inputs.__getitem__(STANZA[7:])
            item.update(**{rest_name:current})
        except RuntimeError,e:
            logging.error("Looks like an error updating the modular input parameter %s: %s" % (rest_name,str(e),))   
        
                       
def dictParameterToStringFormat(parameter):
    
    if parameter:
        return ''.join('{}={},'.format(key, val) for key, val in parameter.items())[:-1] 
    else:
        return None
    
def oauth2_token_updater(token):
    
    try:
        args = {'host':'localhost','port':SPLUNK_PORT,'token':SESSION_TOKEN}
        service = Service(**args)   
        item = service.inputs.__getitem__(STANZA[7:])
        item.update(oauth2_access_token=token["access_token"],oauth2_refresh_token=token["refresh_token"])
    except RuntimeError,e:
        logging.error("Looks like an error updating the oauth2 token: %s" % str(e))

            
def handle_output(response,output,type,req_args,endpoint): 
    
    try:
        if REGEX_PATTERN:
            search_result = REGEX_PATTERN.search(output)
            if search_result == None:
                return   
        RESPONSE_HANDLER_INSTANCE(response,output,type,req_args,endpoint)
        sys.stdout.flush()               
    except RuntimeError,e:
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
