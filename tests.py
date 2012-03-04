import unittest
import deepapi
import time
import sys

class MissingKeyException(Exception):
    pass

class TestSendData(unittest.TestCase):
    def test_01(self): # Set key
        # To run the tests we need a valid key
        try:
            self.key = sys.stdin.read().strip()
            if not self.key:
                self.key = raw_input('Enter your DeepJewel Key: ')
            deepapi.set_key(self.key)
        except IndexError, e:
            raise MissingKeyException('You must run the test with an extra argument: Your DeepJewel Key')

    def test_02(self): # Send Data
        # This is your product.id or post.id or user.screen_name or whatever 
        # you think is useful, anything up to 500 chars
        your_data = '1234' 
        text = '''this is what your item is compound of, the bigger the text, 
the better, currently the max text size is 10MB, which is pretty huge. And as
 you can see, there's no need to do any parsing or anything like that, 
everything will be parsed at the server side\nNew lines\ttabs, everything,
 just send the raw text and everything will be ok'''
        # Categories are a very useful functionality, it will keep your items
        # into separated "boxes" so you can recommend only one type of item
        #(like news or products)
        # The category format is: lang|name
        # In which lang options are: de, en, es, fr, it, pt. It is very important
        # you set the correct language of your category, so DeepJewel can stem
        # use a correct set of stopwords, increasing your recommendations relevance
        category = 'en|post'
        # Yet we have a endpoint to create categories, you can just send
        # what is the category of this item and DeepJewel will create it
        # if needed

        # And then we send the text
        created = deepapi.send(category, your_data, text)
        # Simple like that :)
        self.assertTrue(created)
    
    def test_03(self): # Recommend
        # It may take some seconds to flush data into database
        time.sleep(1)
        response = deepapi.recommend('en|post', '''Here again we send what text we want to
base our recommendation, useful texts are user timeline, user feed, product description
blog post and other relevant information''')
        # Recommendations will always be relevant sorted, first result
        # being the most relevant and last the least
        # Inspect this return to get more information
        self.assertEqual(response[0]['your_data'], '1234')
        

if __name__ == '__main__':
    unittest.main()
