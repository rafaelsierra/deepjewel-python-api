
from base import Consumer
from base import validate_key
from base import DJRequest, ITEM_URL, RECOMMEND_URL
from deepapi.utils import urlencode
import simplejson


class XapianConsumer(Consumer):
    def __init__(self, user_category='en|user'):
        self.user_category = user_category

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
        params = {
            'category': category,
            'my_data': data,
            'text': text,
        }
        if add_info:
            params['add_info'] = 1

        request = DJRequest(ITEM_URL)
        request.set_method('POST')
        request.add_data(urlencode(params))
        request.set_key(self._key)
        response = request.open()
        # Python 2.4 compatible return
        return {200: True, 201: True}.get(response.code, False)

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
        return self.send(self.user_category, identifier, text, add_info)

    @validate_key
    def recommend(self, user, category):
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
        params = {
            'category': category,
            'user': user,
            'user_category': self.user_category,
        }
        request = DJRequest(RECOMMEND_URL)
        request.set_method('POST')
        request.add_data(urlencode(params))
        request.set_key(self._key)
        response = request.open()
        if response.code == 200:
            return simplejson.load(response)
        return None
