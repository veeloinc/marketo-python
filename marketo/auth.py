import hmac
import hashlib
import datetime

import rfc3339


def sign(message, encryption_key):
    digest = hmac.new(encryption_key, message, hashlib.sha1)
    return digest.hexdigest().lower()


def header(user_id, encryption_key):
    timestamp = rfc3339.rfc3339(datetime.datetime.now())
    signature = sign(timestamp + user_id, encryption_key)
    return u"<env:Header><ns1:AuthenticationHeader>" \
           u"<mktowsUserId>{user_id}</mktowsUserId>" \
           u"<requestSignature>{signature}</requestSignature>" \
           u"<requestTimestamp>{timestamp}</requestTimestamp>" \
           u"</ns1:AuthenticationHeader></env:Header>".format(user_id=user_id,
                                                              signature=signature,
                                                              timestamp=timestamp)
