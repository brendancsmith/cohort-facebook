#!/usr/bin/env python3

import os
import pickle
import tempfile
import util
import sources

from nodes import PringusDingus
from analytics import TextAnalytics


def read_cache(path):
    try:
        cacheFile = open(path, 'r')
    except IOError:
        return None
    else:
        obj = pickle.load(cacheFile)
        cacheFile.close()
        return obj


def write_cache(path, obj):
    with open(path, 'w+') as cacheFile:
        pickle.dump(obj, cacheFile, pickle.HIGHEST_PROTOCOL)


def main():
    FACEBOOK_TOKEN = util.get_env_var('FACEBOOK_TOKEN', 'Facebook User Access Token: ')
    ACCOUNT_KEY = util.get_env_var('AZURE_ACCOUNT_KEY', 'Azure Account Key: ')

    #----- Download Pringus Dingus -----

    cachePath = os.path.join(tempfile.gettempdir(), 'comments_{}.pickle'.format(PringusDingus.ID))

    comments = read_cache(cachePath)
    if not comments:
        fbSource = sources.Facebook(FACEBOOK_TOKEN)
        comments = fbSource.download_messenger_chat(PringusDingus)
        comments = {comment['id']: comment for comment in comments}
        write_cache(cachePath, comments)

    #----- Data Pruning -----

    # thumbs don't have messages or something
    comments = {commentId: comment for commentId, comment in comments.items()
                if 'message' in comment}

    #----- Sentiment Analysis -----

    cachePath = os.path.join(tempfile.gettempdir(), 'sentiments_{}.pickle'.format(PringusDingus.ID))

    sentiments = read_cache(cachePath) or {}

    #TODO: batch sentiment
    try:
        textAnalytics = TextAnalytics(ACCOUNT_KEY)
        for commentId in comments:
            if commentId not in sentiments:
                message = comments[commentId]['message']
                sentiment = textAnalytics.get_sentiment(message)
                sentiments[commentId] = sentiment
                print("Analyzed", message, sentiment)
            else:
                print("Read", comments[commentId]['message'], sentiments[commentId])
    except (Exception, KeyboardInterrupt):
        write_cache(cachePath, sentiments)
        raise
    else:
        write_cache(cachePath, sentiments)


if __name__ == '__main__':
    main()
