from requests.auth import AuthBase
import hmac
import base64
import hashlib
import urlparse
import urllib

class TeslaAuth(AuthBase):
    
    auth_path = "/login"
    
    def __init__(self,**args):
        # setup any auth-related data here
        self.username = args['user']
        self.password = args['password']
        self.api_base = args['api_base']
        
        
    def __call__(self, r):
        # modify and return the request
        if not r.cookies:
            cookies = {}
            
            r1 = requests.get(self.api_base+auth_path)
            session_cookie = r1.cookies['_s_portal_session'] 
            
            values = {'user_session[email]':self.username,'user_session[password]':self.password}
            r2 = requests.post(self.api_base+self.auth_path,data=values) 
            credentials_cookie = r2.cookies['user_credentials'] 
            
            cookies = {'_s_portal_session':session_cookie,'user_credentials':credentials_cookie} 
            r.cookies = cookies

        return r
