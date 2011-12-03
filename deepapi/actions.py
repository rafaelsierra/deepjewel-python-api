# -*- encoding: utf-8 -*-
import simplejson
import urllib, urllib2

DOMAIN = 'http://ec2-107-22-86-216.compute-1.amazonaws.com'
ITEM_URL = '%s/api/item.json'%(DOMAIN)
CAT_URL = '%s/api/category.json'%(DOMAIN)
RECOMMEND_URL='%s/api/recommend.json'%(DOMAIN)
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

class MissingKeyError(Exception):
    pass

class InvalidKeyError(Exception):
    pass

def validate_key(function):
    '''Decorator used to check if key is set before calling HTTP, and checking if
    there's some error related to a invalid key'''
    def decorator(self, *args, **kwargs):
        if not self._key:
            raise MissingKeyException('You must set your key before interacting with the server')
        try:
            return function(self, *args, **kwargs)
        except urllib2.HTTPError, e:
            if e.code == 401:
                raise InvalidKeyError('Your key is invalid')
            raise
    return decorator

class Client(object):
    def set_key(self, key):
        self._key = key
        
    @validate_key
    def send(self, category, data, text):
        params = {
            'category': category,
            'my_data': data,
            'text': text,
        }
        request = DJRequest(ITEM_URL)
        request.set_method('POST')
        request.add_data(urllib.urlencode(params))
        request.set_key(self._key)
        response = request.open()
        # Python 2.4 compatible return
        return {200:True, 201:True}.get(response.code, False)

    @validate_key
    def recommend(self, category, text):
        params = {
            'category': category,
            'text': text,
        }
        request = DJRequest(RECOMMEND_URL)
        request.set_method('POST')
        request.add_data(urllib.urlencode(params))
        request.set_key(self._key)
        response = request.open()
        if response.code == 200:
            return simplejson.load(response)
        return None
            
        
