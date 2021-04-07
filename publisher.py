import json
from config import *

INVALID_MESSAGE = "INVALID COMMAND"


class User:
    def __init__(self, user_name, user_role):
        try:
            if user_role == 'admin':
                admin_users.add(user_name)
                print(f"{user_name} added in admins")
            else:
                non_admin_users.add(user_name)
                print(f"{user_name} added in users")

        except Exception as e:
            print(f"Add User failed. Error Message : {e} ")
    
    @staticmethod
    def remove_user(user_to_be_removed):
        try:
            if user_to_be_removed in admin_users:
                admin_users.remove(user_to_be_removed)
                print(f"{user_to_be_removed} removed from admins")
            elif user_to_be_removed in non_admin_users:
                non_admin_users.remove(user_to_be_removed)
                print(f"{user_to_be_removed} removed from users")

        except Exception as e:
            print(f"Error in removing user. Error Message : {e}")


class Topic:
    def __init__(self, topic_name):
        self.topic_name = topic_name
    
    def create_topic(self):
        try:
            topic_path = os.path.join(TOPICS_DIR, self.topic_name)
            if not os.path.exists(topic_path):
                os.makedirs(topic_path)
                topic_subscribers[self.topic_name] = set()
                print(f"{self.topic_name} topic created")
            else:
                print(f"{self.topic_name} topic already exists")

        except Exception as e:
            print(f"Topic creation failed. Error Message : {e}")
    
    def subscribe_topic(self, user_name):
        try:
            topic_subscribers[self.topic_name].add(user_name)
            topics_of_user[user_name].add(self.topic_name)
            print(f"{user_name} subscribed to {self.topic_name}")

        except Exception as e:
            print(f"Topic subcribption failed. Error Message : {e}")
    
    @staticmethod
    def view_subscribed_topics(user_name):
        try:
            print(f"Topics subscribed by {user_name} are ")
            for topic in topics_of_user[user_name]:
                print(topic, end=" ")
            print()

        except Exception as e:
            print("Error in viewing subscribed topics. Error Message : {e}")
    
    def remove_topic(self):
        try:
            if self.topic_name in topic_subscribers:
                users_list = topic_subscribers[self.topic_name]
                # Removing topics from all subscribed users
                for user_name in users_list:
                    if self.topic_name in topics_of_user[user_name]:
                        topic_subscribers[self.topic_name].remove(self.topic_name)

                del topic_subscribers[self.topic_name]
            else:
                print(f"{self.topic_name} doesn't exists")

        except Exception as e:
            print(f"Error in Removing topic. Error Message : {e}")
    
    def add_event_in_topic(self, event_id, event_text):
        if self.topic_name not in topic_subscribers:
            print(f"{self.topic_name} doesn't exists")
            return
        
        topic_path = os.path.join(TOPICS_DIR, self.topic_name)

        if event_id  in topic_event_ids[self.topic_name]:
            print(f"{event_id} already present inside the topic.")
        
        topic_event_ids[self.topic_name].add(event_id)

        file_path = os.path.join(topic_path, f"{event_id}.txt")

        with open(file_path, 'w+') as msg_file:
            msg_file.write(event_text)

class Event:
    def __init__(self, event_message):
        self.event_message = event_message
    
    def post_event(self):
        try:
            event_id = self.event_message.get('id', None)
            if event_id == None:
                print("Event Id is missing in message body")
                return
            
            topic_name = self.event_message.get('topicName', None)
            if topic_name == None:
                print("Topic Name is missing in message body")
                return
            
            event_text = self.event_message.get('text', None)
            if event_text == None:
                print("Text is missing in message body")
                return
            
            topic = Topic(topic_name)
            topic.add_event_in_topic(event_id, event_text)
            
        except Exception as e:
            print(f"Error in posting Event. Error Messag : {e}")


if __name__ == "__main__":
    for command in command_types:
        print(command)
    
    while True:
        commands = input("Enter commands in one of the above format : ").split()

        if commands == ['exit']:
            break

        commands_len = len(commands)
        operation_type = commands[0]

        if operation_type == 'addUser':
            if commands_len == 3:
                user = User(commands[1], commands[2])
            else:
                print(INVALID_MESSAGE)
        
        elif operation_type == 'addTopic':
            if commands_len == 3:
                user_name, topic_name = commands[1], commands[2]
                if user_name in admin_users:
                    topic = Topic(topic_name)
                    topic.create_topic()
                else:
                    print("only admin users can add topics. You are not an admin.")
            else:
                print(INVALID_MESSAGE)
        
        elif operation_type == 'subscribeTopic':
            if commands_len == 3:
                user_name, topic_name = commands[1], commands[2]
                topic = Topic(topic_name)
                topic.subscribe_topic(user_name)
            else:
                print(INVALID_MESSAGE)
        
        elif operation_type == 'viewSubscribedTopics':
            if commands_len == 2:
                user_name = commands[1]
                Topic.view_subscribed_topics(user_name)
            else:
                print(INVALID_MESSAGE)
        
        elif operation_type == 'removeUser':
            if commands_len == 3:
                user_to_be_removed, user_name = command[1], commands[2]
                if user_name in admin_users:
                    if user_name == user_to_be_removed:
                        print("You cannot remove yourself")
                    else:
                        User.remove_user(user_to_be_removed)
                else:
                    print("Only admin can perform this opertaion, you are not an admin.")
            else:
                print(INVALID_MESSAGE)
        
        elif operation_type == 'removeTopic':
            if commands_len == 3:
                user_name, topic_name =  commands[1], commands[2]
                if user_name in admin_users:
                    topic = Topic(topic_name)
                    topic.remove_topic()
                else:
                    print("only admin users can remove topics. You are not an admin.")
            else:
                print(INVALID_MESSAGE)
        
        elif operation_type == 'postEvent':
            print("COMMANDS", commands)
            if commands_len == 2:
                message = json.loads(commands[1])
                event = Event(message)
                event.post_event()
            else:
                print(INVALID_MESSAGE)            
        
        print("ADMINS : ", admin_users)
        print("USERS : ", non_admin_users)
        print("TOPICS : ", topic_subscribers)
        print("USER TOPIC : ", topics_of_user)
