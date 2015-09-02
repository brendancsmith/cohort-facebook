import chatstats

from plotly import plotly as pyplot
from plotly.graph_objs import Data, Bar


def num_comments_by_user(comments, **kwargs):
    numCommentsByUser = chatstats.num_comments_by_user(comments)

    sortedTuples = [item for item in sorted(numCommentsByUser.items(), key=lambda item: item[1])]
    x, y = zip(*sortedTuples)

    data = Data([
        Bar(
            x=x,
            y=y
        )
    ])

    plotUrl = pyplot.plot(data, share='secret', filename='pringus-dingus-commenters', **kwargs)
    return plotUrl


# def num_comments_by_day(comments):
