import facebook

from getpass import getpass

token = getpass('User Access Token: ')

graph = facebook.GraphAPI(token)
friends = graph.get_connections("me", "friends")

friend_list = [friend['name'] for friend in friends['data']]

print friend_list
