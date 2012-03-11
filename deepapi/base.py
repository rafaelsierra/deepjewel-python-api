# -*- encoding: utf-8 -*-
import urllib2

DOMAIN = 'http://177.71.179.67:8000'
ITEM_URL = '%s/api/item.json' % (DOMAIN)
USER_URL = '%s/api/user.json' % (DOMAIN)
CAT_URL = '%s/api/category.json' % (DOMAIN)
RECOMMEND_URL = '%s/api/recommend.json' % (DOMAIN)
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
    '''Decorator used to check if key is set before calling HTTP,
        and checking if there's some error related to a invalid key'''
    def decorator(self, *args, **kwargs):
        if not self._key:
            raise MissingKeyError('You must set your key before ' +
                        'interacting with the server')
        try:
            return function(self, *args, **kwargs)
        except urllib2.HTTPError, e:
            if e.code == 401:
                raise InvalidKeyError('Your key is invalid')
            raise
    decorator.__doc__ = function.__doc__
    return decorator


class Consumer(object):

    def __init__(self, user_category='en|user'):
        self.user_category = user_category

    def set_key(self, key):
        '''You can only use this API with your key'''
        self._key = key

    @validate_key
    def send(self, category, data, text, add_info=False):
        '''
        Send some item to DeepJewel.

        Parameters
        ----------
        category: The category of your item
        data: How is this item identified in your system,
            must always be something unique inside this `category`
            so you can get this item inside your database
        text: All the text you have about your item
        add_info (default: True) : Use this to control
        whether you are sending new information or resending
        all information about your item

        '''
        raise NotImplementedError('It must be implemented.')

    @validate_key
    def send_user_info(self, identifier, text, add_info=True):
        '''
        Send some user info about your user, anytime your user
        provide you some information (like tweets or posts)
        you call this function to update DeepJewel about
        your user's profile.

        Parameters
        ----------

        identifier - This is what identifies who is this user
         to your system, you can use login, ID, email, or any
         other unique information about your user.
         If you wish to send login or email, make sure that they
         are unique even when removed anything that is not letters
         or numbers, if you are not sure just send your user ID.
         In case you send logins and they allow dashes or underscores,
         "some_users" will became equal "someusers".

        Again, if you are unsure what you should send, use ID.

        text - What your user just added of information about himself

        add_info (default: True) - Use this to control whether you are
        sending new information or resending all information about your user
        category (default en|user) - In what category you want to store
        your users under. You may want change this at least to another
        language.

        '''
        raise NotImplementedError('It must be implemented.')

    @validate_key
    def recommend(self, identifier, category):
        '''
        Fetches user recommendations from `category`.
        User must be the same thing you always sent to
        DeepJewel with send_user_info and category is what
        you intent to recommend.

        Parameters
        ----------

        identifier - This is what identifies who is this user
         to your system, you can use login, ID, email, or any
         other unique information about your user.
         If you wish to send login or email, make sure that they
         are unique even when removed anything that is not letters
         or numbers, if you are not sure just send your user ID.
         In case you send logins and they allow dashes or underscores,
         "some_users" will became equal "someusers".

        category: The category of your item

        Returns
        -------
        Returns a list of dictionaries like this:
            [
                {
                    'your_data': '', # This is what you sent as `data`
                                     from deepapi.send(),
                    'relevance': 0.0, # Float from 0.0 to 1.0 with how
                                 much this item may be relevant to your user
                    'category': '', # Category, in witch category this item
                                     was found (equals `category`)
                                (this will be an awesome feature in the future)
                },
                {...}
            ]
        '''
        raise NotImplementedError('It must be implemented.')
