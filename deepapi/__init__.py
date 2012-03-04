from deepapi.actions import Client, MissingKeyError, InvalidKeyError

client = Client()
send = client.send
send_user_info = client.send_user_info
recommend = client.recommend
set_key = client.set_key

__all__ = ['recommend', 'send', 'send_user_info', 'set_key', 'InvalidKeyError', 'MissingKeyError']
