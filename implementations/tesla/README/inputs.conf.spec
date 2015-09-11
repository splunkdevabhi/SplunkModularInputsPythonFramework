[tesla://<name>]

* Tesla Vehicle ID
vehicle_id = <value>

* Username (email) for My Tesla
user = <value>

* Password for My Tesla
password = <value>

* Client ID
client_id  = <value>

* Client Secret
client_secret  = <value>

* Tesla OAuth URL
oauth_url = <value>

* Tesla REST API Base URL
api_base = <value>

* Tesla REST API Endpoint Path
endpoint = <value>

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




