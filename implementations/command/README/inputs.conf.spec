[command://<name>]

*command name , environment variables in the format $VARIABLE$ can be included and they will be substituted ie: $SPLUNK_HOME$
command_name= <value>

*command args, environment variables in the format $VARIABLE$ can be included and they will be substituted ie: $SPLUNK_HOME$
command_args= <value>

*whether or not command output is streaming or not
streaming_output = <value>

*in seconds
execution_interval= <value>

*Python classname of custom command output handler
output_handler= <value>

*Command output handler arguments string ,  key=value,key2=value2
output_handler_args= <value>