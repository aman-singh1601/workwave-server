import jwt
import datetime
from keys.keys import secret_key

def tokengen(payload):
    payload['exp'] = datetime.datetime.utcnow() + datetime.timedelta(hours=3)
    token = jwt.encode(payload, secret_key, algorithm='HS256')
    return token

