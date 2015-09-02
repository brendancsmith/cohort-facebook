#!/usr/bin/env python3

import util
import facebookclient
import plotting

from analytics import TextAnalytics


def main():
    FACEBOOK_TOKEN = util.get_env_var('FACEBOOK_TOKEN', 'Facebook User Access Token: ')
    AZURE_ACCOUNT_KEY = util.get_env_var('AZURE_ACCOUNT_KEY', 'Azure Account Key: ')

    # ----- Download Pringus Dingus -----

    fbClient = facebookclient.FacebookClient(FACEBOOK_TOKEN)
    comments = fbClient.download_chat(facebookclient.Nodes.PringusDingus)

    # I think empty comments are thumbs ups?
    nonEmptyComments = list(filter(lambda comment: 'message' in comment, comments))

    # ----- Simple Statistics -----

    plotUrls = [
        # plotting.num_comments_by_user(comments, 'pringus-dingus-commenters', auto_open=False),
        # plotting.num_comments_by_day(comments, 'pringus-dingus-days', auto_open=False),
        # plotting.avg_word_count_by_user(comments, 'pringus-dingus-avg-word-count-by-user-excl-empty', auto_open=False),
        # plotting.avg_word_count_by_user(nonEmptyComments, 'pringus-dingus-avg-word-count-by-user', auto_open=False),
        # plotting.longest_comment_by_users(nonEmptyComments, 'pringus-dingus-longest-comments', auto_open=False),
        # plotting.word_count_by_day(nonEmptyComments, 'pringus-dingus-word-count-by-day', auto_open=False),
        # plotting.verbosity_by_day(nonEmptyComments, 'pringus-dingus-verbosity-by-day', auto_open=False),
        plotting.daily_activity_by_user(comments, 'pringus-dingus-daily-activity-by-user', auto_open=True)
    ]
    print(plotUrls)

    # ----- Sentiment Analysis -----
    '''
    cachePath = os.path.join(tempfile.gettempdir(),
                             'sentiments_{}.pickle'.format(sources.FacebookChat.Nodes.PringusDingus))

    sentiments = shelve.open(cachePath, writeback=True)

    # TODO: batch sentiment
    try:
        textAnalytics = TextAnalytics(AZURE_ACCOUNT_KEY)
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
    '''


if __name__ == '__main__':
    main()
