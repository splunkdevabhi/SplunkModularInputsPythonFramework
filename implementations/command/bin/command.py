'''
Modular Input Script

Copyright (C) 2012 Splunk, Inc.
All Rights Reserved

'''

import sys,logging,os,time,subprocess,re
import xml.dom.minidom, xml.sax.saxutils

#set up logging
logging.root
logging.root.setLevel(logging.ERROR)
formatter = logging.Formatter('%(levelname)s %(message)s')
#with zero args , should go to STD ERR
handler = logging.StreamHandler()
handler.setFormatter(formatter)
logging.root.addHandler(handler)

CMD_OUTPUT_HANDLER_INSTANCE = None

SCHEME = """<scheme>
    <title>Command</title>
    <description>Command input wrapper for executing commands and indexing the output</description>
    <use_external_validation>true</use_external_validation>
    <streaming_mode>xml</streaming_mode>
    <use_single_instance>false</use_single_instance>

    <endpoint>
        <args>    
            <arg name="name">
                <title>Command Input Name</title>
                <description>Name of this command input definition</description>
            </arg>
            <arg name="command_name">
                <title>Command Name</title>
                <description>Name of the system command if on the PATH (ps),  or if not , the full path to the command (/bin/ps).Environment variables in the format $VARIABLE$ can be included and they will be substituted ie: $SPLUNK_HOME$</description>
                <required_on_edit>true</required_on_edit>
                <required_on_create>true</required_on_create>
            </arg>
            <arg name="command_args">
                <title>Command Arguments</title>
                <description>Arguments string for the command.Environment variables in the format $VARIABLE$ can be included and they will be substituted ie: $SPLUNK_HOME$</description>
                <required_on_edit>false</required_on_edit>
                <required_on_create>false</required_on_create>
            </arg> 
            <arg name="streaming_output">
                <title>Streaming Output</title>
                <description>Whether or not the command output is streaming</description>
                <required_on_edit>false</required_on_edit>
                <required_on_create>false</required_on_create>
            </arg>      
            <arg name="execution_interval">
                <title>Command Execution Interval</title>
                <description>Interval time in seconds to execute the command</description>
                <required_on_edit>false</required_on_edit>
                <required_on_create>false</required_on_create>
            </arg>
            <arg name="output_handler">
                <title>Command Output Handler</title>
                <description>Python classname of custom command output handler</description>
                <required_on_edit>false</required_on_edit>
                <required_on_create>false</required_on_create>
            </arg>
            <arg name="output_handler_args">
                <title>Command Output Handler Arguments</title>
                <description>Command output handler arguments string ,  key=value,key2=value2</description>
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
        
        command_name=config.get("command_name")
        execution_interval=config.get("execution_interval")
        output_handler=config.get("output_handler")   
        
        validationFailed = False
    
        try:
            if not output_handler is None:
                module = __import__("outputhandlers")
                class_ = getattr(module,output_handler)
                instance = class_()
        except Exception,e:
            print_validation_error("Output Handler "+output_handler+" can't be instantiated")
            validationFailed = True
        try:
            if not execution_interval is None and int(execution_interval) < 1:
                print_validation_error("Execution interval must be a positive integer")
                validationFailed = True
        except Exception,e:
            print_validation_error("Execution interval must be an integer")
            validationFailed = True
        if not command_name is None and which(command_name) is None:
            print_validation_error("Command name "+command_name+" does not exist")
            validationFailed = True
        if validationFailed:
            sys.exit(2)
               
    except RuntimeError,e:
        logging.error("Looks like an error: %s" % str(e))
        sys.exit(1)
        raise   
     
def which(program):

    def is_exe(fpath):
        return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

    fpath, fname = os.path.split(program)
    if fpath:
        if is_exe(program):
            return program
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            path = path.strip('"')
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return exe_file

    return None
    
def do_run():
    config = get_input_config()  
    
    command_name=config.get("command_name")
    command_args=config.get("command_args")
    
    command_string = command_name
    if command_args:
        command_string = command_string+" "+command_args
     
    try:    
        env_var_tokens = re.findall("\$(?:\w+)\$",command_string)
        for token in env_var_tokens:
            command_string = command_string.replace(token,os.environ.get(token[1:-1]))
    except: 
        e = sys.exc_info()[1]
        logging.error("Looks like an error replacing environment variables: %s" % str(e))  
         
    streaming_output=int(config.get("streaming_output",0))
    
    execution_interval=int(config.get("execution_interval",60))
    
    cmd_output_handler_args={} 
    cmd_output_handler_args_str=config.get("output_handler_args")
    if not cmd_output_handler_args_str is None:
        cmd_output_handler_args = dict((k.strip(), v.strip()) for k,v in 
              (item.split('=') for item in cmd_output_handler_args_str.split(',')))
        
    cmd_output_handler=config.get("output_handler","DefaultCommandOutputHandler")
    module = __import__("outputhandlers")
    class_ = getattr(module,cmd_output_handler)

    global CMD_OUTPUT_HANDLER_INSTANCE
    CMD_OUTPUT_HANDLER_INSTANCE = class_(**cmd_output_handler_args)
    
    while True:
            
        try:
            proc = run_command(command_string)
            output_buffer = ""
            while True:
                line = proc.stdout.readline()
                if line != '':
                    if streaming_output :
                      handle_output(line.rstrip())
                    else :
                      output_buffer = output_buffer + line
                else:
                    break
            if not streaming_output:
                handle_output(output_buffer)    
            time.sleep(float(execution_interval))
        except RuntimeError,e:
            logging.error("Looks like an error: %s" % str(e))
            sys.exit(2) 
        
def run_command(command):
    return subprocess.Popen(command,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        
def handle_output(output): 
    
    try:  
        CMD_OUTPUT_HANDLER_INSTANCE(output)
        sys.stdout.flush()               
    except RuntimeError,e:
        logging.error("Looks like an error handling the command output: %s" % str(e))
        
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
