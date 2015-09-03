from collections import Counter, defaultdict
from datetime import datetime
from statistics import mean

from dateutil.parser import parse as parse_datetime
from dateutil import rrule


def num_comments_by_user(comments):
    commenters = (comment['from']['name'] for comment in comments)
    counter = Counter(commenters)

    return counter


def num_comments_by_day(comments):
    datetimes = datetimes(comments)

    counter = Counter(dt.date() for dt in datetimes)

    first_day = min(counter.keys())
    last_day = datetime.now().date()
    all_dates = (dt.date() for dt in rrule.rrule(rrule.DAILY,
                                                 dtstart=first_day,
                                                 until=last_day))

    for date in all_dates:
        if date not in counter:
            counter[date] = 0

    return counter


def avg_word_count_by_user(comments, default_word_count=1):
    wordCountsByUser = defaultdict(list)

    for comment in comments:
        name = comment['from']['name']

        words = None
        if 'message' not in comment:
            words = default_word_count
        else:
            words = len(comment['message'].split())

        wordCountsByUser[name].append(words)

    avgWordCountByUser = dict((user, mean(wordCounts))
                              for user, wordCounts in wordCountsByUser.items())

    return avgWordCountByUser


def longest_comment_by_users(comments):
    longestCommentByUser = defaultdict(int)

    commentsByUser = defaultdict(list)

    for comment in comments:
        name = comment['from']['name']
        commentsByUser[name].append(comment)

    for name, comments in commentsByUser.items():

        commentLengths = (len(comment['message']) for comment in comments)
        maxCommentLength = max(commentLengths)

        longestCommentByUser[name] = maxCommentLength

    return longestCommentByUser


def word_count_by_day(comments):
    wordCountsByDay = defaultdict(int)

    for comment in comments:
        timestamp = comment['created_time']
        date = parse_datetime(timestamp).date()

        words = len(comment['message'].split())

        wordCountsByDay[date] += words

    first_day = min(wordCountsByDay.keys())
    last_day = datetime.now().date()
    all_dates = (dt.date() for dt in rrule.rrule(rrule.DAILY,
                                                 dtstart=first_day,
                                                 until=last_day))
    for date in all_dates:
        if date not in wordCountsByDay:
            wordCountsByDay[date] = 0

    return wordCountsByDay


def daily_activity_by_user(comments):
    first_day = min(parse_datetime(comment['created_time']).date() for comment in comments)
    last_day = datetime.now().date()
    all_dates = [dt.date() for dt in rrule.rrule(rrule.DAILY,
                                                 dtstart=first_day,
                                                 until=last_day)]
    activityByUser = defaultdict(list)
    for comment in comments:
        user = comment['from']['name']

        timestamp = comment['created_time']
        date = parse_datetime(timestamp).date()

        activityByUser[user].append(date)

    make_blank_counter = lambda: Counter(dict(zip(all_dates, [0] * len(all_dates))))

    dailyActivityByUser = {}
    for user, activity in activityByUser.items():
        dailyActivityByUser[user] = make_blank_counter()
        dailyActivityByUser[user].update(activity)

    return dailyActivityByUser


def datetimes(comments):
    timestamps = (comment['created_time'] for comment in comments)
    datetimes = map(parse_datetime, timestamps)
    return datetimes
