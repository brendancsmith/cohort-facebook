#!/usr/bin/env python3
import facebook
import os
from getpass import getpass

PRINGUS_DINGUS = '1475782379372580'


def get_token():
    # Read the FACEBOOK_TOKEN environment variable,
    # or ask for it if none is set.

    # On Mac OS X, this can be temporarily set via:
    #     launchctl setenv FACEBOOK_TOKEN <user access token here>

    token = os.environ.get('FACEBOOK_TOKEN')
    if not token:
        token = getpass('Facebook User Access Token: ')

    return token


def main():
    graph = facebook.GraphAPI(get_token())

    pringusDingus = graph.get_object(PRINGUS_DINGUS)
    print(pringusDingus['comments'])


if __name__ == '__main__':
    main()
