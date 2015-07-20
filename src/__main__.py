#!/usr/bin/env python3

import os
import pickle
import tempfile
import util
import sources

from nodes import PringusDingus
from analytics import TextAnalytics




def main():
    FACEBOOK_TOKEN = util.get_env_var('FACEBOOK_TOKEN', 'Facebook User Access Token: ')
    ACCOUNT_KEY = util.get_env_var('AZURE_ACCOUNT_KEY', 'Azure Account Key: ')

    #----- Download Pringus Dingus -----

    cachePath = os.path.join(tempfile.gettempdir(), 'comments_{}.pickle'.format(PringusDingus.ID))

    comments = None
    try:
        cacheFile = open(cachePath, 'r')
    except IOError:
        fbSource = sources.Facebook(FACEBOOK_TOKEN)
        comments = fbSource.download_messenger_chat(PringusDingus)

        with open(cachePath, 'w+') as cacheFile:
            pickle.dump(comments, cacheFile, pickle.HIGHEST_PROTOCOL)
    else:
        comments = pickle.load(cacheFile)
        cacheFile.close()

    #----- Sentiment Analysis -----

    textAnalytics = TextAnalytics(ACCOUNT_KEY)
    for comment in comments:
        if 'message' in comment:  # thumbs don't have messages or something
            message = comment['message']
            sentiment = textAnalytics.get_sentiment(message)
            print(message, sentiment)


if __name__ == '__main__':
    main()
