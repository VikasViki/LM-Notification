import os
from config import *

def print_subscribed_messages():
    for topic_name, user_names_list in topic_subscribers.items():
        for user_name in user_names_list:
            curr_output = {'topic': topic_name, 'sentTo': user_name, 'message': ''}
            topic_path = os.path.join(TOPICS_DIR, topic_name)
            for file_name in os.listdir(topic_path):
                with open(file_name, 'r') as msg_file:
                    curr_output['message'] = msg_file.read()
            print(curr_output)
    print("All topics Processed")


if __name__ == "__main__":
    while True:
        print_subscribed_messages()