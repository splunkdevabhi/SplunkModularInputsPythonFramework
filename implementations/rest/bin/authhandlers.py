from requests.auth import AuthBase
import hmac
import base64
import hashlib
import urlparse
import urllib

#add your custom auth handler class to this module

#template
class MyCustomAuth(AuthBase):
    def __init__(self,**args):
        # setup any auth-related data here
        #self.username = args['username']
        #self.password = args['password']
        pass
        
    def __call__(self, r):
        # modify and return the request
        #r.headers['foouser'] = self.username
        #r.headers['foopass'] = self.password
        return r
    

class MyUnifyAuth(AuthBase):
     def __init__(self,**args):
         self.username = args['username']
         self.password = args['password']
         self.url = args['url']
         pass
 
     def __call__(self, r):
         login_url = '%s?username=%s&login=login&password=%s' % self.url,self.username,self.password
         login_response = requests.get(login_url)
         cookies = login_response.cookies
         if cookies:
            r.cookies = cookies
         return r
         
#example of adding a client certificate    
class MyAzureCertAuthHAndler(AuthBase):
    def __init__(self,**args):
        self.cert = args['certPath']
        pass
        
    def __call__(self, r):
        r.cert = self.cert
        return r
    
#example of adding a client certificate    
class GoogleBigQueryCertAuthHandler(AuthBase):
    def __init__(self,**args):
        self.cert = args['certPath']
        pass
        
    def __call__(self, r):
        r.cert = self.cert
        return r
    
#cloudstack auth example
class CloudstackAuth(AuthBase):
    def __init__(self,**args):
        # setup any auth-related data here
        self.apikey = args['apikey']
        self.secretkey = args['secretkey']
        pass
        
    def __call__(self, r):
        # modify and return the request
    
        parsed = urlparse.urlparse(r.url)
        url = parsed.geturl().split('?',1)[0]
        url_params= urlparse.parse_qs(parsed.query)
        
        #normalize the list value
        for param in url_params:
            url_params[param] = url_params[param][0]
        
        url_params['apikey'] = self.apikey
        
        keys = sorted(url_params.keys())

        sig_params = []
        for k in keys:
            sig_params.append(k + '=' + urllib.quote_plus(url_params[k]).replace("+", "%20"))
       
        query = '&'.join(sig_params)

        signature = base64.b64encode(hmac.new(
            self.secretkey,
            msg=query.lower(),
            digestmod=hashlib.sha1
        ).digest())

        
        query += '&signature=' + urllib.quote_plus(signature)

        r.url = url + '?' + query
        
        return r