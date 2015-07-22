# Standard Modules

import os
import tempfile
import time

# Installed/External Modules

import facebook

# Project Modules
import cache
import util
from util import AttrDict


class FacebookChat(object):

    Nodes = AttrDict({
        'PringusDingus': '1475782379372580'
    })

    def __init__(self, node, graphApiToken):
        self.node = node
        self.token = graphApiToken

    def download_chat(self):
        print('Fetching messages from Pringus Dingus...')
        comments = []
        numRead = 0
        for commentsPage in self.download_chat_pages():
            comments += commentsPage
            numRead += len(commentsPage)

            util.print_inplace('{} messages read.'.format(numRead))

            # FB's rate limit is ~600 requests per 600 seconds,
            # but I still exceeded it at a sleep of 1 second.
            # TODO: implement error handling for exceeding the limit
            time.sleep(1.1)

        return comments

    def download_chat_pages(self):
        graph = facebook.GraphAPI(self.token)

        pagedComments = graph.get_connections(self.node,
                                              'comments',
                                              limit=100,  # FB sticks to 29/30
                                              paging=True)

        return pagedComments


class CacheBackedFacebookChat(FacebookChat):

    def __init__(self, node, graphApiToken):
        super().__init__(node, graphApiToken)

        self.cachePath = os.path.join(tempfile.gettempdir(),
                                      'comments_{}.pickle'.format(node))
        self.cache = cache.read(self.cachePath) or {}

        self.bypassingSource = bool(self.cache)

    class CacheGuard(object):

        def __init__(self, source, content):
            self.source = source
            self.content = content

        def __enter__(self):
            return self.content

        def __exit__(self, type, value, traceback):
            self.source.close()

    def download_chat_pages(self):
        if self.bypassingSource:
            def paginate_cached_comments():
                yield self.cache.values()

            pages = paginate_cached_comments()
            return self.CacheGuard(self, pages)

        else:
            def intercept_pages(pages):
                for page in pages:
                    self.cache.update({comment['id']: comment for comment in page})
                    yield page

            pages = intercept_pages(super().download_chat_pages())

            return self.CacheGuard(self, pages)

    def close(self):
        if not self.bypassingSource:
            cache.write(self.cachePath, self.cache)
