import base64
import json
import urllib2
import urllib
import util


class TextAnalytics(object):

    BASE_URL = 'https://api.datamarket.azure.com/data.ashx/amla/text-analytics/v1'

    def __init__(self, accountKey):
        self.accountKey = accountKey
        self.creds = base64.b64encode('AccountKey:' + self.accountKey)

    def request(self, url):
        headers = {'Content-Type': 'application/json', 'Authorization': ('Basic '+ self.creds)}
        req = urllib2.Request(url, None, headers)
        response = urllib2.urlopen(req)
        result = response.read()
        obj = json.loads(result)
        return obj

    def get_sentiment(self, text):
        params = {'Text': text.encode('utf-8')}
        url = self.BASE_URL + '/GetSentiment?' + urllib.urlencode(params)
        sentiment = self.request(url)
        return sentiment['Score']

    def get_key_phrases(self, text):
        params = {'Text': text.encode('utf-8')}
        url = self.BASE_URL + '/GetKeyPhrases?' + urllib.urlencode(params)
        keyPhrases = self.request(url)
        return keyPhrases['KeyPhrases']
