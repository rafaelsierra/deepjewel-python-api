from deepapi.actions import Client, MissingKeyError, InvalidKeyError

client = Client()
send = client.send
recommend = client.recommend
set_key = client.set_key

__all__ = ['recommend', 'send', 'key', 'InvalidKeyError', 'MissingKeyError']
