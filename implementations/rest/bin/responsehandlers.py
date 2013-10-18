#add your custom response handler class to this module
import json
#the default handler , does nothing , just passes the raw output directly to STDOUT
class DefaultResponseHandler:
    
    def __init__(self,**args):
        pass
        
    def __call__(self, response_object,raw_response_output,response_type,req_args,endpoint):        
        print_xml_stream(raw_response_output)
          
        
        
class MyResponseHandler:
    
    def __init__(self,**args):
        pass
        
    def __call__(self, response_object,raw_response_output,response_type,req_args,endpoint):        
        print_xml_stream("foobar")

class BoxEventHandler:
    
    def __init__(self,**args):
        pass
        
    def __call__(self, response_object,raw_response_output,response_type,req_args,endpoint):
        if response_type == "json":        
            output = json.loads(raw_response_output)
            if not "params" in req_args:
                req_args["params"] = {}
            if "next_stream_position" in output:    
                req_args["params"]["stream_position"] = output["next_stream_position"]
            for entry in output["entries"]:
                print_xml_stream(json.dumps(entry))   
        else:
            print_xml_stream(raw_response_output)  

class FourSquareCheckinsEventHandler:
    
    def __init__(self,**args):
        pass
        
    def __call__(self, response_object,raw_response_output,response_type,req_args,endpoint):
        if response_type == "json":        
            output = json.loads(raw_response_output)
            
            for checkin in output["response"]["checkins"]["items"]:
                print_xml_stream(json.dumps(checkin))   
        else:
            print_xml_stream(raw_response_output)  
 
class TwitterEventHandler:
    
    def __init__(self,**args):
        pass
        
    def __call__(self, response_object,raw_response_output,response_type,req_args,endpoint):
        if response_type == "json":        
            output = json.loads(raw_response_output)
            
            for tweet in output["statuses"]:
                print_xml_stream(json.dumps(tweet))   
        else:
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