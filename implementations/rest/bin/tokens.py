#define token functions for substitution in endpoint URL
# /someurl/foo/$sometoken$/goo -> /someurl/foo/zoo/goo
import datetime

def sometoken():
    return 'zoo'

def datetoday():
    today = datetime.date.today()
    return today.strftime('%Y-%m-%d')


