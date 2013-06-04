[rest://<name>]

* REST API Endpoint URL
endpoint= <value>

* Authentication type [none | basic | digest | oauth1 | oauth2 ]
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
oauth2_expires_in= <value>
oauth2_refresh_token= <value>
oauth2_refresh_url= <value>
oauth2_client_id= <value>

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



