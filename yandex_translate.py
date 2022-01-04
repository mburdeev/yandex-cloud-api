import requests
from datetime import datetime, timedelta


# iamToken: token, received_at, expires_at

OAUTH_TOKEN = 'AQAAAAAKDHwbAATuwck16sT8qEumlQz7WgDBfo4'

class IamToken:

    API_URL = 'https://iam.api.cloud.yandex.net/iam/v1/tokens'

    def __init__(self, oauth_token=None):
        self.oauth_token = OAUTH_TOKEN
        self.token_request()

    def token_request(self):
        params = {'yandexPassportOauthToken': self.oauth_token}
        response = requests.post(IamToken.API_URL, json=params)
        response_data = response.json()
        self._token = response_data['iamToken']
        self.expires_at = response_data['expiresAt'] # TODO Parse expiresAt
        self.received_at = datetime.now()

    @property
    def token(self):
        if self.received_at - datetime.now() > timedelta(hours=1):
            self.token_request()

        return self._token
        

def test_IamToken():
    iamtoken = IamToken()
    return iamtoken.token

# params = {'yandexPassportOauthToken': 'AQAAAAAKDHwbAATuwck16sT8qEumlQz7WgDBfo4'}
# response = requests.post('https://iam.api.cloud.yandex.net/iam/v1/tokens', json=params)
# response.json()
# {'iamToken': 't1.9euelZqeic2ZjJSai8nMlZ7Pj5jHmO3rnpWajJGWkM2Pk46KyomdjI7Ox8vl8_ccXDNx-e9JZEQX_d3z91wKMXH570lkRBf9.WsBvVVl1qZxBMBh40TC6SdPiJU3XkrutcfIVN8Us8Gp0Q4SakHYjik3AJgGDmS9Il349BwUtloy0rX29q_BACw', 'expiresAt': '2022-01-04T03:10:27.755944886Z'}


def debug_request():
    IAM_TOKEN = 't1.9euelZqemp6Zjpeays2ZyYybnpOWi-3rnpWajJGWkM2Pk46KyomdjI7Ox8vl8_cYAzVx-e8zFGZp_d3z91gxMnH57zMUZmn9.BtFRN3s-K9bQtgukPeI8On-es_Z9NEoZ5PbURwMwFioJSnWgd9mrv6FzkSyXi3XkyuoTkfXRdZyL6Smmg7NMAw'
    folder_id = 'b1gonrd7tr8h9gfl8t7u'
    target_language = 'ru'
    texts = ["Hello", "World"]

    body = {
        "targetLanguageCode": target_language,
        "texts": texts,
        "folderId": folder_id,
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer {0}".format(IAM_TOKEN)
    }

    response = requests.post('https://translate.api.cloud.yandex.net/translate/v2/translate',
        json = body,
        headers = headers
    )

    print(response.text)