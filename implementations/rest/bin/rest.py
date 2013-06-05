'''
Modular Input Script

Copyright (C) 2012 Splunk, Inc.
All Rights Reserved

'''

import sys,logging,os,time
import xml.dom.minidom

SPLUNK_HOME = os.environ.get("SPLUNK_HOME")


#dynamically load in any eggs in /etc/apps/snmp_ta/bin
egg_dir = SPLUNK_HOME + "/etc/apps/rest_ta/bin/"

sys.path.append(egg_dir + "uuid-1.30")
sys.path.append(egg_dir + "splunklib")

for filename in os.listdir(egg_dir):
    if filename.endswith(".egg"):
        sys.path.append(egg_dir + filename) 
       
import requests,json
from requests.auth import HTTPBasicAuth
from requests.auth import HTTPDigestAuth
from requests_oauthlib import OAuth1
from requests_oauthlib import OAuth2
from oauthlib.oauth2 import WebApplicationClient 
           
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
            <arg name="auth_type">
                <title>Authentication Type</title>
                <description>Authentication method to use : none | basic | digest | oauth1 | oauth2</description>
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
            <arg name="oauth2_expires_in">
                <title>OAUTH 2 Expiration Time</title>
                <description>OAUTH 2 expiration time</description>
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
            <arg name="oauth2_client_id">
                <title>OAUTH 2 Client ID</title>
                <description>OAUTH 2 client ID</description>
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
            <arg name="index_error_response_codes">
                <title>Index Error Responses</title>
                <description>Whether or not to index error response codes : true | false</description>
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
    #params
    
    endpoint=config.get("endpoint")
    
    #none | basic | digest | oauth1 | oauth2
    auth_type=config.get("auth_type","none")
    
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
    oauth2_expires_in=config.get("oauth2_expires_in")
    oauth2_refresh_token=config.get("oauth2_refresh_token")
    oauth2_refresh_url=config.get("oauth2_refresh_url")
    oauth2_client_id=config.get("oauth2_client_id","splunk_rest")
    
    http_header_propertys={}
    http_header_propertys_str=config.get("http_header_propertys")
    if not http_header_propertys_str is None:
        http_header_propertys = dict((k.strip(), v.strip()) for k,v in 
              (item.split('=') for item in http_header_propertys_str.split(',')))
       
    url_args={} 
    url_args_str=config.get("url_args")
    if not url_args_str is None:
        url_args = dict((k.strip(), v.strip()) for k,v in 
              (item.split('=') for item in url_args_str.split(',')))
        
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
        
    
    request_timeout=int(config.get("request_timeout",30))
    
    backoff_time=int(config.get("backoff_time",10))
    
    polling_interval=int(config.get("polling_interval",60))
    
    index_error_response_codes=int(config.get("index_error_response_codes",0))
    
    
    try: 
        auth=None
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
            token["expires_in"] = oauth2_expires_in
            client = WebApplicationClient(oauth2_client_id)
            auth = OAuth2(client, token=token,auto_refresh_url=oauth2_refresh_url,token_updater=oauth2_token_updater)
   
   
        req_args = {"verify" : False ,"stream" : bool(streaming_request) , "timeout" : float(request_timeout)}

        if auth:
            req_args["auth"]= auth
        if url_args:
            req_args["params"]= url_args
        if http_header_propertys:
            req_args["headers"]= http_header_propertys
        if proxies:
            req_args["proxies"]= proxies

            
        while True:
            
            try:
                r = requests.get(endpoint,**req_args)
            except requests.exceptions.Timeout,e:
                logging.error("HTTP Request Timeout error: %s" % str(e))
                time.sleep(float(backoff_time))
                continue
            try:
                r.raise_for_status()
                if streaming_request:
                    for line in r.iter_lines():
                        if line:
                            handle_output(line)  
                else:                    
                    handle_output(r.text)
            except requests.exceptions.HTTPError,e:
                error_output = r.text
                error_http_code = r.status_code
                if index_error_response_codes:
                    error_event=""
                    error_event += 'http_error_code = %s error_message = %s' % (error_http_code.prettyPrint(), error_output.prettyPrint()) 
                    print_xml_single_instance_mode(error_event)
                    sys.stdout.flush()
                logging.error("HTTP Request error: %s" % str(e))
                time.sleep(float(backoff_time))
                continue
                                 
            time.sleep(float(polling_interval))
            
    except RuntimeError,e:
        logging.error("Looks like an error: %s" % str(e))
        sys.exit(2) 

def oauth2_token_updater(token):
  #TODO , persist updated token back to input stanza via REST ???
  foo={}
            
def handle_output(output): 
    
    try:
        print_xml_single_instance_mode(output)
        sys.stdout.flush()  
    except RuntimeError,e:
        logging.error("Looks like an error writing out the event to Splunk: %s" % str(e))

# prints validation error data to be consumed by Splunk
def print_validation_error(s):
    print "<error><message>%s</message></error>" % encodeXMLText(s)
    
# prints XML stream
def print_xml_single_instance_mode(s):
    print "<stream><event><data>%s</data></event></stream>" % encodeXMLText(s)
    
# prints XML stream
def print_xml_multi_instance_mode(s,stanza):
    print "<stream><event stanza=""%s""><data>%s</data></event></stream>" % stanza,encodeXMLText(s)
    
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
