from deepapi.clients import XapianConsumer
from deepapi.base import MissingKeyError, InvalidKeyError

client = XapianConsumer()
send = client.send
send_user_info = client.send_user_info
recommend = client.recommend
set_key = client.set_key

__all__ = ['recommend', 'send', 'send_user_info', 'set_key',
            'InvalidKeyError', 'MissingKeyError']
