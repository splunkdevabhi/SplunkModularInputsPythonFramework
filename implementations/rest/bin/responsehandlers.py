#add your custom response handler class to this module
import json
import datetime

#the default handler , does nothing , just passes the raw output directly to STDOUT
class DefaultResponseHandler:
    
    def __init__(self,**args):
        pass
        
    def __call__(self, response_object,raw_response_output,response_type,req_args,endpoint):
        cookies = response_object.cookies
        if cookies:
            req_args["cookies"] = cookies        
        print_xml_stream(raw_response_output)
          
#template
class MyResponseHandler:
    
    def __init__(self,**args):
        pass
        
    def __call__(self, response_object,raw_response_output,response_type,req_args,endpoint):        
        print_xml_stream("foobar")

'''various example handlers follow'''
        
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

class QualysGuardActivityLog:
    '''Response handler for QualysGuard activity log.'''

    def __init__(self,**args):
        pass

    def __call__(self, response_object,raw_response_output,response_type,req_args,endpoint):
        if not "params" in req_args:
            req_args["params"] = {}
        date_from = (datetime.datetime.now() - datetime.timedelta(minutes=1)).strftime("%Y-%m-%dT%H:%M:%SZ")
        req_args["params"]["date_from"] = date_from
        print_xml_stream(raw_response_output) 
                          
class FourSquareCheckinsEventHandler:
    
    def __init__(self,**args):
        pass
        
    def __call__(self, response_object,raw_response_output,response_type,req_args,endpoint):
        if response_type == "json":        
            output = json.loads(raw_response_output)
            last_created_at = 0
            for checkin in output["response"]["checkins"]["items"]:
                print_xml_stream(json.dumps(checkin)) 
                if "createdAt" in checkin:
                    created_at = checkin["createdAt"]
                    if created_at > last_created_at:
                        last_created_at = created_at
            if not "params" in req_args:
                req_args["params"] = {}
            
            req_args["params"]["afterTimestamp"] = last_created_at
                      
        else:
            print_xml_stream(raw_response_output) 
            
class ThingWorxTagHandler:
    
    def __init__(self,**args):
        pass
        
    def __call__(self, response_object,raw_response_output,response_type,req_args,endpoint):
        if response_type == "json":        
            output = json.loads(raw_response_output)
            for row in output["rows"]:
                print_xml_stream(json.dumps(row))                      
        else:
            print_xml_stream(raw_response_output) 
            
class FireEyeEventHandler:
    
    def __init__(self,**args):
        pass
        
    def __call__(self, response_object,raw_response_output,response_type,req_args,endpoint):
        if response_type == "json":        
            output = json.loads(response_object.content)
            last_display_id = -1
            for alert in output["alerts"]:
                print_xml_stream(json.dumps(alert))  
                if "displayId" in alert:
                    display_id = alert["displayId"]
                    if display_id > last_display_id:
                        last_display_id = display_id
            if not "params" in req_args:
                req_args["params"] = {}
            
            if last_display_id > -1:
                req_args["params"]["offset"] = last_display_id

        else:
            print_xml_stream(raw_response_output) 
              
          
class BugsenseErrorsEventHandler:
    
    def __init__(self,**args):
        pass
        
    def __call__(self, response_object,raw_response_output,response_type,req_args,endpoint):
        if response_type == "json":        
            output = json.loads(raw_response_output)
            
            for error in output["data"]:
                print_xml_stream(json.dumps(error))   
        else:
            print_xml_stream(raw_response_output)

class MyCustomHandler:
    
    def __init__(self,**args):
        pass
        
    def __call__(self, response_object,raw_response_output,response_type,req_args,endpoint):
        
        req_args["data"] = 'What does the fox say'   
         
        print_xml_stream(raw_response_output)
                               

class TwitterEventHandler:

    def __init__(self,**args):
        pass

    def __call__(self, response_object,raw_response_output,response_type,req_args,endpoint):       
            
        if response_type == "json":        
            output = json.loads(raw_response_output)
            last_tweet_indexed_id = 0
            for twitter_event in output["statuses"]:
                print_xml_stream(json.dumps(twitter_event))
                if "id_str" in twitter_event:
                    tweet_id = twitter_event["id_str"]
                    if tweet_id > last_tweet_indexed_id:
                        last_tweet_indexed_id = tweet_id
            
            if not "params" in req_args:
                req_args["params"] = {}
            
            req_args["params"]["since_id"] = last_tweet_indexed_id
                       
        else:
            print_xml_stream(raw_response_output)
     

                
class AutomaticEventHandler:

    def __init__(self,**args):
        pass

    #process the received JSON array     
    def process_automatic_response(data):
    
        output = json.loads(data)
        last_end_time = 0
                    
        for event in output:
            #each element of the array is written to Splunk as a seperate event
            print_xml_stream(json.dumps(event))
            if "end_time" in event:
                #get and set the latest end_time
                end_time = event["end_time"]
                if end_time > last_end_time:
                    last_end_time = end_time
        return last_end_time

    def __call__(self, response_object,raw_response_output,response_type,req_args,endpoint):       
            
        if response_type == "json":
            last_end_time = 0
            
            #process the response from the orginal request
            end_time = process_automatic_response(raw_response_output)
            
            #set the latest end_time
            if end_time > last_end_time:
                last_end_time = end_time
             
            #follow any pagination links in the response    
            next_link = response_object.links["next"] 
                   
            while next_link:
                next_response = requests.get(next_link)       
                end_time = process_automatic_response(next_response.text)  
                #set the latest end_time 
                if end_time > last_end_time:
                    last_end_time = end_time  
                next_link = next_response.links["next"]
                        
            if not "params" in req_args:
                req_args["params"] = {}
            
            #set the start URL attribute for the next request
            #the Mod Input will persist this to inputs.conf for you
            req_args["params"]["start"] = last_end_time
                       
        else:
            print_xml_stream(raw_response_output)
            
            
            
class OpenstackTelemetryHandler:

    def __init__(self,**args):
        pass

    def __call__(self, response_object,raw_response_output,response_type,req_args,endpoint):       
            
        if response_type == "json":        
            output = json.loads(raw_response_output)
            timestamp = 0
            for counter in output:
                print_xml_stream(json.dumps(counter))
                if "timestamp" in counter:
                    temp_timestamp = counter["timestamp"]
                    if temp_timestamp > timestamp:
                        timestamp = temp_timestamp
            
            if not "params" in req_args:
                req_args["params"] = {}
            
            req_args["params"]["q.value"] = timestamp
                       
        else:
            print_xml_stream(raw_response_output)


class JSONArrayHandler:

    def __init__(self,**args):
        pass

    def __call__(self, response_object,raw_response_output,response_type,req_args,endpoint):
        if response_type == "json":
            output = json.loads(raw_response_output)

            for entry in output:
                print_xml_stream(json.dumps(entry))
        else:
            print_xml_stream(raw_response_output)
                                      

class FlightInfoEventHandler:
    
    def __init__(self,**args):
        pass
        
    def __call__(self, response_object,raw_response_output,response_type,req_args,endpoint):
        if response_type == "json":        
            output = json.loads(raw_response_output)
            for flight in output["FlightInfoResult"]["flights"]:
                print_xml_stream(json.dumps(flight)) 
                
                      
        else:
            print_xml_stream(raw_response_output) 
            
class AlarmHandler:
    
    def __init__(self,**args):
        pass
        
    def __call__(self, response_object,raw_response_output,response_type,req_args,endpoint):
        if response_type == "xml": 
            import xml.etree.ElementTree as ET
            alarm_list = ET.fromstring(encodeXMLText(raw_response_output))
            for alarm in alarm_list:
                alarm_xml_str = ET.tostring(alarm, encoding='utf8', method='xml')
                print_xml_stream(alarm_xml_str)               
                      
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