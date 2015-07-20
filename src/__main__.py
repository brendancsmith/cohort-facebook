#!/usr/bin/env python3

import os
import time
import sys
import pickle
import tempfile
import util
import sources

from nodes import PringusDingus


def print_inplace(line):
    sys.stdout.write('\r' + line)
    sys.stdout.flush()


def main():
    FACEBOOK_TOKEN = util.get_env_var('FACEBOOK_TOKEN', 'Facebook User Access Token: ')

    #-----

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




if __name__ == '__main__':
    main()
