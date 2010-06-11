import urllib2

import oauth2

from poster.encode import multipart_encode, MultipartParam
from poster.streaminghttp import register_openers


class EchoRequest(oauth2.Request):
    def to_header(self, realm, auth_service_provider):
        headers = super(EchoRequest, self).to_header(realm=realm)
        return {'X-Verify-Credentials-Authorization': headers['Authorization'],
                'X-Auth-Service-Provider': auth_service_provider}
        
        
class Echo(object):
    def __init__(self, realm, auth_service_provider, consumer, token):
        if consumer is not None and not isinstance(consumer, oauth2.Consumer):
            raise ValueError("Invalid consumer.")

        if token is not None and not isinstance(token, oauth2.Token):
            raise ValueError("Invalid token.")

        self.consumer = consumer
        self.token = token
        self.method = oauth2.SignatureMethod_HMAC_SHA1()
        self.realm = realm
        self.auth_service_provider = auth_service_provider
        
    def set_signature_method(self, method):
        if not isinstance(method, SignatureMethod):
            raise ValueError("Invalid signature method.")

        self.method = method
    
    def request(self, uri, method="POST",
                body=None, headers=None):

        params = {
            'oauth_consumer_key': self.consumer.key,
            'oauth_signature_method': self.method.name,
            'oauth_token':self.token.key,
            'oauth_timestamp':oauth2.generate_timestamp(),
            'oauth_nonce':oauth2.generate_nonce(),
            'oauth_version':'1.0'
        }
    
        echo_request = EchoRequest(method="GET",
                                      url=self.auth_service_provider,
                                      parameters=params
                                      )
    
        signature=echo_request.sign_request(oauth2.SignatureMethod_HMAC_SHA1(),
                                                  self.consumer,
                                                  self.token)
    
        if not headers:
            headers={}
        headers.update(echo_request.to_header(self.realm, self.auth_service_provider))
        
        register_openers()
        datagen, heads = multipart_encode(body)
        headers.update(heads)
        req = urllib2.Request(uri, datagen, headers)
        response = urllib2.urlopen(req)
        return response
    