#!/usr/bin/env python3

import os
import tempfile
import util
import time
import sources
import cache

from analytics import TextAnalytics


def main():
    FACEBOOK_TOKEN = util.get_env_var('FACEBOOK_TOKEN', 'Facebook User Access Token: ')
    ACCOUNT_KEY = util.get_env_var('AZURE_ACCOUNT_KEY', 'Azure Account Key: ')

    # ----- Download Pringus Dingus -----

    # read Cache

    # get pages of Pringus Dingus

    pringusDingus = None

    pringusDingusSource = sources.CacheBackedFacebookChat(
        sources.FacebookChat.Nodes.PringusDingus,
        FACEBOOK_TOKEN)

    comments = []
    with pringusDingusSource.download_chat_pages() as pringusDingus:

        for chatPage in pringusDingus:
            filterEmptyComments = lambda page: [comment for comment in page
                                                if 'message' in comment]
            chatPage = filterEmptyComments(chatPage)
            comments += chatPage
            time.sleep(1.1)

    # ----- Sentiment Analysis -----

    cachePath = os.path.join(tempfile.gettempdir(),
                             'sentiments_{}.pickle'.format(sources.FacebookChat.Nodes.PringusDingus))

    sentiments = cache.read(cachePath) or {}

    # TODO: batch sentiment
    try:
        textAnalytics = TextAnalytics(ACCOUNT_KEY)
        for comment in comments:
            if comment['id'] not in sentiments:
                sentiment = textAnalytics.get_sentiment(comment['message'])
                sentiments[comment['id']] = sentiment
                print("Analyzed", comment['message'], sentiment)
            else:
                print("Read", comment['message'], sentiments[comment['id']])
    except (Exception, KeyboardInterrupt):
        cache.write(cachePath, sentiments)
        raise
    else:
        cache.write(cachePath, sentiments)


if __name__ == '__main__':
    main()
