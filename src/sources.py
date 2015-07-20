import facebook
import util
import time


class Facebook(object):

    def __init__(self, graphApiToken):
        self.token = graphApiToken

    def download_messenger_chat(self, node):
        graph = facebook.GraphAPI(self.token)

        pagedComments = graph.get_connections(node.ID,
                                              'comments',
                                              limit=100,  # FB sticks to 29/30
                                              paging=True)

        print('Fetching messages from Pringus Dingus...')
        comments = []
        numRead = 0
        for commentsPage in pagedComments:
            comments += commentsPage
            numRead += len(commentsPage)

            util.print_inplace('{} messages read.'.format(numRead))

            # FB's rate limit is ~600 requests per 600 seconds,
            # but I still exceeded it at a sleep of 1 second.
            # TODO: implement error handling for exceeding the limit
            time.sleep(1.1)

        return comments
