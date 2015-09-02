from collections import Counter
from datetime import datetime

from dateutil.parser import parse as parse_datetime
from dateutil import rrule


def num_comments_by_user(comments):
    commenters = (comment['from']['name'] for comment in comments)
    counter = Counter(commenters)

    return counter


def num_comments_by_day(comments):
    timestamps = (comment['created_time'] for comment in comments)
    datetimes = map(parse_datetime, timestamps)

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
