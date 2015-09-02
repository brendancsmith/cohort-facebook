from collections import Counter


def num_comments_by_user(comments):
    commenters = (comment['from']['name'] for comment in comments)
    counter = Counter(commenters)

    return dict(counter)


# def num_comments_by_day(comments):
