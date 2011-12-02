# -*- encoding: utf-8 -*-
import urllib, urllib2

ITEM_URL = 'http://api-beta.deepjewel.com/api/item.json'
CAT_URL = 'http://api-beta.deepjewel.com/api/category.json'
KEY = None

class DJRequest(urllib2.Request):
    '''Custom request so we can set what HTTP method will be used'''
    def set_method(self, method):
        self._method = method.upper()

    def get_method(self):
        return self._method

    def set_key(self, key):
        self.add_header('X-DeepJewel-Key', key)

    def open(self):
        return urllib2.urlopen(self)

def key(key):
    global KEY
    KEY=key
        
def send(category, data, text):
    request = DJRequest(ITEM_URL)
    request.set_method('POST')
    request.set_key(key)
    request.open()
    # Python 2.4 compatible
    return {200:True, 201:True}.get(request.code, False)


def recommend():
    pass #WIP
