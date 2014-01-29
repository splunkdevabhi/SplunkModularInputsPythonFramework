#add your custom response handler class to this module
import json
import datetime
#the default handler , does nothing , just passes the raw output directly to STDOUT
class DefaultResponseHandler:
    
    def __init__(self, **args):
        pass
        
    def __call__(self, response_object, raw_response_output, response_type, req_args, endpoint):        
        print_xml_stream(raw_response_output)
          

class MyCustomTeslaHandler:
    
    def __init__(self, **args):
        pass
        
    def __call__(self, response_object, raw_response_output, response_type, req_args, endpoint):
        
        req_args["data"] = 'What does the fox say'           
        print_xml_stream(raw_response_output)
                                                                    
                                                                             
#HELPER FUNCTIONS
    
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
