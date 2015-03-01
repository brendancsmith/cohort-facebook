#!/usr/bin/env python3

import facebook
import os
import time
import sys

from getpass import getpass
from nodes import PringusDingus


def get_token():
    # Read the FACEBOOK_TOKEN environment variable,
    # or ask for it if none is set.

    # On Mac OS X, this can be temporarily set via:
    #     FACEBOOK_TOKEN=<user access token here>
    # Or more permanently via:
    #     launchctl setenv FACEBOOK_TOKEN <user access token here>

    token = os.environ.get('FACEBOOK_TOKEN')
    if not token:
        token = getpass('Facebook User Access Token: ')

    return token


def print_inplace(line):
    sys.stdout.write('\r' + line)
    sys.stdout.flush()


def main():
    graph = facebook.GraphAPI(get_token())

    pagedComments = graph.get_connections(PringusDingus.ID,
                                          'comments',
                                          limit=100,  # FB sticks to 29/30
                                          paging=True)

    print('Fetching messages from Pringus Dingus...')
    comments = []
    numRead = 0
    for commentsPage in pagedComments:
        comments += commentsPage
        numRead += len(commentsPage)

        print_inplace('{} messages read.'.format(numRead))

        # FB's rate limit is ~600 requests per 600 seconds,
        # but I still exceeded it at a sleep of 1 second.
        # TODO: implement error handling for exceeding the limit
        time.sleep(1.1)

    print()
    print(comments)


if __name__ == '__main__':
    main()
