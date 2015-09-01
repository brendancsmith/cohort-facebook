# Standard Modules

import os
import shelve
import tempfile
import time

# Installed/External Modules

import facebook

# Project Modules
import util
from util import AttrDict


Nodes = AttrDict({
    'PringusDingus': '1475782379372580'
})


class FacebookClient(object):

    def __init__(self, graphApiToken):
        self.token = graphApiToken

    def get_chat_node(self, node):
        graph = facebook.GraphAPI(self.token)

        return FacebookChat(graph, node)


class FacebookChat(object):

    # FB's rate limit is ~600 requests per 600 seconds,
    # but I still exceeded it at a sleep of 1 second.
    # TODO: implement error handling for exceeding the limit
    throttleRate = 1.2

    def __init__(self, graph, node):
        self.node = node

        self.pages = graph.get_connections(self.node,
                                           'comments',
                                           limit=100,  # FB still sticks to 29/30
                                           paging=True)

    def get_comments(self):  # TODO: get rid of output in favor of progress callback
        print('Fetching messages from Pringus Dingus...')
        comments = []
        numRead = 0
        for commentsPage in self.pages:
            comments += commentsPage
            numRead += len(commentsPage)

            util.print_inplace('{} messages read.'.format(numRead))

            time.sleep(self.throttleRate)

        return comments


'''
class CacheBackedFacebookChat(FacebookChat):

    def __init__(self, node, graphApiToken):
        super().__init__(node, graphApiToken)

        self.cachePath = os.path.join(tempfile.gettempdir(),
                                      'comments_{}.pickle'.format(node))

        self.cache = shelve.open(self.cachePath)

    def download_chat_pages(self):
        if self.cache:
            def paginate_cached_comments():
                yield self.cache.values()

            pages = paginate_cached_comments()
            return self.CacheGuard(self.cache, pages)

        else:
            def intercept_pages(pages):
                for page in pages:
                    self.cache.update({comment['id']: comment for comment in page})
                    yield page

            pages = intercept_pages(super().download_chat_pages())

            return self.CacheGuard(self.cache, pages)
'''
