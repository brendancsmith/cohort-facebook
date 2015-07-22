import base64
import json
import urllib


class TextAnalytics(object):

    BASE_URL = 'https://api.datamarket.azure.com/data.ashx/amla/text-analytics/v1'

    def __init__(self, accountKey):
        encode_b64 = lambda s: base64.b64encode(s.encode('utf-8')).decode('utf-8')
        self.creds = encode_b64('AccountKey:' + accountKey)

    def request(self, url):
        headers = {'Content-Type': 'application/json', 'Authorization': ('Basic ' + self.creds)}
        req = urllib.request.Request(url, None, headers)
        response = urllib.request.urlopen(req)
        result = response.read().decode('utf-8')
        obj = json.loads(result)
        return obj

    def get_sentiment(self, text):
        params = {'Text': text.encode('utf-8')}
        url = self.BASE_URL + '/GetSentiment?' + urllib.parse.urlencode(params)
        sentiment = self.request(url)
        return sentiment['Score']

    def get_key_phrases(self, text):
        params = {'Text': text.encode('utf-8')}
        url = self.BASE_URL + '/GetKeyPhrases?' + urllib.parse.urlencode(params)
        keyPhrases = self.request(url)
        return keyPhrases['KeyPhrases']
