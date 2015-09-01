#!/usr/bin/env python3

import os
import tempfile
import util
import time
import shelve
import sources

from analytics import TextAnalytics


def main():
    FACEBOOK_TOKEN = util.get_env_var('FACEBOOK_TOKEN', 'Facebook User Access Token: ')
    ACCOUNT_KEY = util.get_env_var('AZURE_ACCOUNT_KEY', 'Azure Account Key: ')

    # ----- Download Pringus Dingus -----

    fbClient = sources.FacebookClient(FACEBOOK_TOKEN)
    pringusDingus = fbClient.get_chat_node(sources.Nodes.PringusDingus)

    cachePath = os.path.join(tempfile.gettempdir(),
                             'comments_{}.pickle'.format(sources.Nodes.PringusDingus))
    print("cachePath: {}".format(cachePath))

    '''
    comments = []
    with pringusDingusSource.download_chat_pages() as pringusDingus:

        for chatPage in pringusDingus:
            filterEmptyComments = lambda page: [comment for comment in page
                                                if 'message' in comment]
            chatPage = filterEmptyComments(chatPage)
            comments += chatPage
            time.sleep(1.1)
    '''

    comments = shelve.open(cachePath, writeback=True)

    if not comments:
        comments = pringusDingus.get_comments()

    comments.close()

    pass

    # ----- Sentiment Analysis -----

    cachePath = os.path.join(tempfile.gettempdir(),
                             'sentiments_{}.pickle'.format(sources.FacebookChat.Nodes.PringusDingus))

    sentiments = shelve.open(cachePath, writeback=True)

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
        sentiments.close()
        raise
    else:
        sentiments.close()


if __name__ == '__main__':
    main()
