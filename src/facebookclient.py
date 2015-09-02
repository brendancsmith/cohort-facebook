# Standard Modules
import time

# Installed/External Modules

import facebook

# Project Modules
from util import AttrDict
import cache


Nodes = AttrDict({
    'PringusDingus': '1475782379372580'
})


class FacebookClient(object):

    def __init__(self, graphApiToken):
        self.graph = facebook.GraphAPI(graphApiToken)

    def download_chat(self, node):
        self.cacheManager = CacheManager(self.graph, node, 'comments')

        comments = self.cacheManager.download_connections()
        return comments


class CacheManager(object):

    # FB's rate limit is ~600 requests per 600 seconds,
    # but I still exceeded it at a sleep of 1 second.
    # TODO: implement error handling for exceeding the limit
    throttleRate = 1.5

    def __init__(self, graph, node, connectionName):
        self.graph = graph
        self.node = node
        self.connectionName = connectionName

        self.cacheLabel = 'node_{}_{}'.format(node, connectionName)

    def download_connections(self):
        self.cache = cache.find(self.cacheLabel)

        try:
            if self.cache:
                self._update_cache()
                self._backfill_cache()
            else:
                self._fill_cache()
        except:
            self.cache.close()
            raise
        else:
            connections = [self.cache[key] for key in sorted(self.cache)]
            self.cache.close()
            return connections

    def _fill_cache(self):
        pages = self._request_pages()
        self._cache_pages(pages)

    def _backfill_cache(self):
        firstPageIndex = min(self.cache.keys())

        # print('backfilling from:', firstPageIndex)

        # TODO: always re-caches the first connection
        pages = self._request_pages(until=firstPageIndex)
        self._cache_pages(pages)

    def _update_cache(self):
        lastPageIndex = max(self.cache.keys())

        # print('updating to:', lastPageIndex)

        pages = self._request_pages(since=lastPageIndex)
        self._cache_pages(pages)

    def _cache_pages(self, pages):
        for page in pages:
            for connection in page:
                pageIndex = self._get_connection_index(connection)
                self.cache[pageIndex] = connection

            time.sleep(self.throttleRate)
            # TODO: catch GraphAPIError instead of sleeping
            #       need to make sure it won't skip pages

    def _get_connection_index(self, connection):
        return connection['id'].split('_')[1]

    def _request_pages(self, **kwargs):
        return self.graph.get_connections(self.node,
                                          self.connectionName,
                                          limit=100,  # FB still sticks to 29/30
                                          paging=True,
                                          **kwargs)

    '''
    def _extract_paging_tokens(self, page):
        # from urllib.parse import urlparse, parse_qs

        previousUrl = page['paging']['previous']
        query = urlparse(previousUrl).query
        [sinceToken] = parse_qs(query)['since']

        nextUrl = page['paging']['next']
        query = urlparse(nextUrl).query
        [untilToken] = parse_qs(query)['until']

        return untilToken, sinceToken
    '''
