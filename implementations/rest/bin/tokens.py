#define token functions for substitution in endpoint URL
#/someurl/foo/$sometoken$/goo -> /someurl/foo/zoo/goo

# functions can return a scalar or a list
# if a scalar is returned , then a single URL request will be made
# if a list is returned , then (n) URL requests will be made , where (n) is the 
# length of the list
# multiple requests will get executed in parallel threads

import datetime

def sometoken():
    return 'zoo'

def sometokenlist():
    return ['goo','foo','zoo']

def datetoday():
    today = datetime.date.today()
    return today.strftime('%Y-%m-%d')


