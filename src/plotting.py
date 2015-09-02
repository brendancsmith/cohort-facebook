import chatstats

from plotly import plotly as pyplot
from plotly.graph_objs import Bar, Data, Scatter


def num_comments_by_user(comments, **kwargs):
    numCommentsByUser = chatstats.num_comments_by_user(comments)

    x, y = zip(*reversed(numCommentsByUser.most_common()))

    data = Data([
        Bar(
            x=x,
            y=y
        )
    ])

    plotUrl = pyplot.plot(data, share='secret', filename='pringus-dingus-commenters', **kwargs)
    return plotUrl


def num_comments_by_day(comments, **kwargs):
    numCommentsByDay = chatstats.num_comments_by_day(comments)

    x, y = zip(*sorted(numCommentsByDay.items()))

    trace = Scatter(
        x=x,
        y=y,
        mode='lines'
    )

    plotUrl = pyplot.plot([trace], share='secret', filename='pringus-dingus-days', **kwargs)
    return plotUrl
