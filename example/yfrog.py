import os

from oauth2 import Token, Consumer
from oauth2.clients.echo import Echo

# YFROG documentation http://code.google.com/p/imageshackapi/wiki/TwitterAuthentication
TWITTER_REALM='http://api.twitter.com/'
TWITTER_VERIFY_CREDENTIALS_XML="https://api.twitter.com/1/account/verify_credentials.xml"
TWITTER_CONSUMER_KEY="CONSUMER KEY"
TWITTER_CONSUMER_SECRET="CONSUMER SECRET"
ACCESS_TOKEN_KEY='ACCESS TOKEN KEY'
ACCESS_TOKEN_SECRET='ACCESS TOKEN SECRET'

YFROG_API_KEY="API KEY"
YFROG_API_URL="https://yfrog.com/api/xauth_upload"

FILE_PATH="minime.jpg"

def upload_to_yfrog(file_path):
    token = Token(ACCESS_TOKEN_KEY, ACCESS_TOKEN_SECRET)
    consumer = Consumer(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET)
    
    body = {
        'key':YFROG_API_KEY,
        'message': "Test Echo OAuth",
        'media':open(file_path, 'rb')
    }
    
    echo = Echo(realm=TWITTER_REALM,
                auth_service_provider=TWITTER_VERIFY_CREDENTIALS_XML,
                consumer=consumer, token=token)
    
    return echo.request(uri=YFROG_API_URL, body=body)

if __name__ == '__main__':
    response = upload_to_yfrog(file_path=FILE_PATH)
    print response.read()