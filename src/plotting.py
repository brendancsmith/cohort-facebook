import operator

import chatstats

from plotly import plotly as pyplot
from plotly.graph_objs import Bar, Data, Scatter, Heatmap, Layout, Figure

# TODO: make a Plotter class or something, and make auto_open False by default


def _sort_by_values(d):
    return sorted(d.items(), key=lambda item: item[1])


def num_comments_by_user(comments, filename, **kwargs):
    numCommentsByUser = chatstats.num_comments_by_user(comments)

    x, y = zip(*reversed(numCommentsByUser.most_common()))

    data = Data([
        Bar(
            x=x,
            y=y
        )
    ])

    plotUrl = pyplot.plot(data, share='secret', filename=filename, **kwargs)
    return plotUrl


def num_comments_by_day(comments, filename, **kwargs):
    numCommentsByDay = chatstats.num_comments_by_day(comments)

    x, y = zip(*sorted(numCommentsByDay.items()))

    data = Data([
        Bar(
            x=x,
            y=y
        )
    ])

    plotUrl = pyplot.plot(data, share='secret', filename=filename, **kwargs)
    return plotUrl


def avg_word_count_by_user(comments, filename, **kwargs):
    avgWordCountByUser = chatstats.avg_word_count_by_user(comments)

    sortedItems = _sort_by_values(avgWordCountByUser)
    x, y = zip(*sortedItems)

    data = Data([
        Bar(
            x=x,
            y=y
        )
    ])

    plotUrl = pyplot.plot(data, share='secret', filename=filename, **kwargs)
    return plotUrl


def longest_comment_by_users(comments, filename, **kwargs):
    longestCommentByUsers = chatstats.longest_comment_by_users(comments)

    sortedItems = _sort_by_values(longestCommentByUsers)
    x, y = zip(*sortedItems)

    data = Data([
        Bar(
            x=x,
            y=y
        )
    ])

    plotUrl = pyplot.plot(data, share='secret', filename=filename, **kwargs)
    return plotUrl


def word_count_by_day(comments, filename, **kwargs):
    wordCountsByDay = chatstats.word_count_by_day(comments)

    sortedItems = _sort_by_values(wordCountsByDay)
    x, y = zip(*sortedItems)

    data = Data([
        Bar(
            x=x,
            y=y
        )
    ])

    plotUrl = pyplot.plot(data, share='secret', filename=filename, **kwargs)
    return plotUrl


# --- HYBRID


def verbosity_by_day(comments, filename, **kwargs):
    numCommentsByDay = chatstats.num_comments_by_day(comments)
    wordCountsByDay = chatstats.word_count_by_day(comments)

    assert len(wordCountsByDay) == len(numCommentsByDay)

    verbosityByDay = {}

    for key in numCommentsByDay:
        try:
            verbosity = wordCountsByDay[key] / numCommentsByDay[key]
        except ZeroDivisionError:
            if wordCountsByDay[key] != 0:
                raise RuntimeError("How did we get words with 0 messages?")
            else:
                verbosity = 0
        finally:
            verbosityByDay[key] = verbosity

    x, y = zip(*sorted(verbosityByDay.items()))

    data = Data([
        Bar(
            x=x,
            y=y
        )
    ])

    plotUrl = pyplot.plot(data, share='secret', filename=filename, **kwargs)
    return plotUrl


# ------


def daily_activity_by_user(comments, filename, **kwargs):
    dailyActivityByUser = chatstats.daily_activity_by_user(comments)

    def sort_by_full_name(fullName):
        names = fullName.split()
        return [names[-1]] + [names[:-1]]

    users = list(sorted(dailyActivityByUser.keys(), key=sort_by_full_name, reverse=True))
    dates = sorted(list(dailyActivityByUser[users[0]].keys()))

    z = []

    for user in users:
        dailyActivity = dailyActivityByUser[user]
        new_row = []
        for date, activity in sorted(dailyActivity.items()):
            new_row.append(activity)
        z.append(new_row)

    data = Data([
        Heatmap(
            z=z,
            x=dates,
            y=users,
            colorscale='YIGnBu',
        )
    ])

    layout = Layout(title='Messages per day',
                    xaxis=dict(ticks='', nticks=36),
                    yaxis=dict(ticks=''))

    fig = Figure(data=data, layout=layout)

    plotUrl = pyplot.plot(fig, filename='datetime-heatmap', validate=False)
    return plotUrl
