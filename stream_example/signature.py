import hmac
import hashlib
import base64

WEB_ID = "843d68ff-61fe-4bce-a347-9c17275e3665"
WEB_KEY = "Abg8D9wQnNh4GwjA"
SECRET = "ZYHSBDJZ45fRe6qFBATfRxMerPFMHBN564MfjpQPq4dqfAtz9jaTxnHBjCBX88pA"

def get_signature(timestamp):
    fullsec = timestamp + WEB_ID + WEB_KEY
    
    msg = fullsec.encode('utf-8')
    secret = SECRET.encode('utf-8')

    hashed = hmac.new(secret, msg, hashlib.sha256).digest()
    encoded_string = base64.b64encode(hashed)

    return encoded_string.decode('utf-8')