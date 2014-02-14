[rest://<name>]

* REST API Endpoint URL
endpoint= <value>

* HTTP Method (GET,POST,PUT)
http_method = <value>

* Request Payload for POST and PUT
request_payload = <value>

* Authentication type [none | basic | digest | oauth1 | oauth2 | custom ]
auth_type= <value>

* for basic/digest
auth_user= <value>

* for basic/digest
auth_password= <value>

*oauth1 params
oauth1_client_key= <value>
oauth1_client_secret= <value>
oauth1_access_token= <value>
oauth1_access_token_secret= <value>

*oauth2 params
oauth2_token_type= <value>
oauth2_access_token= <value>
oauth2_refresh_token= <value>
oauth2_refresh_url= <value>
oauth2_refresh_props= <value>
oauth2_client_id= <value>
oauth2_client_secret= <value>

* prop=value, prop2=value2
http_header_propertys= <value>

* arg=value, arg2=value2
url_args= <value>

* Response type [json | text]
response_type= <value>

* true | false
streaming_request= <value>

* ie: (http://10.10.1.10:3128 or http://user:pass@10.10.1.10:3128 or https://10.10.1.10:1080 etc...)
http_proxy= <value>
https_proxy= <value>

*in seconds
request_timeout= <value>

* time to wait for reconnect after timeout or error
backoff_time = <value>

*in seconds
polling_interval= <value>

* whether or not to index http error response codes
index_error_response_codes= <value>

*Python classname of custom response handler
response_handler= <value>

*Response Handler arguments string ,  key=value,key2=value2
response_handler_args= <value>

*Python Regex pattern, if present , the response will be scanned for this match pattern, and indexed if a match is present
response_filter_pattern = <value>

*Python classname of custom auth handler
custom_auth_handler= <value>

*Custom Authentication Handler arguments string ,  key=value,key2=value2
custom_auth_handler_args= <value>

*Delimiter to use for any multi "key=value" field inputs
delimiter= <value>

*For persisting Cookies
cookies= <value>





