import os
from collections import defaultdict

CWD = os.getcwd()
TOPICS_DIR = os.path.join(CWD, 'TOPICS')

# Making Directory to store all topics
if not os.path.exists(TOPICS_DIR):
    os.mkdir(TOPICS_DIR)

# Set to store all admins user_names
admin_users = set()

# Set to store non admin users
non_admin_users = set()

# Set to store event id's
topic_event_ids = defaultdict(set)

# Dictionary to store set of user_names for the subcribed topic id
topic_subscribers = defaultdict(set)

# Dictionary to store topics subscribed by particular user
topics_of_user = defaultdict(set)


command_types = [
    'addUser <userName> <role> : To add user/admin',
    'addTopic <user_name> <topic_name>',
    'subscribeTopic <user_name> <topic_name>',
    'viewSubscribedTopics userName : To view topics subscribed by user',
    'removeUser <user_name : user to be removed> <user_name : user performing the command>\n'
    'removeTopic <user_name> <topic_name> : removing topic\n'
    'postEvent <message : json format with keys(id, topicName, text) WITHOUT SPACE in message> : To post a event in a topic\n'
    'exit : To stop system\n'
]
