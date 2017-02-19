from multiprocessing import Queue
import psycopg2
import psycopg2.extras
from pyTwitterListener import TweetListener
import os

class TweetProcessor:

    def __init__(self, cursor):

        self.cursor = cursor
        self.tweet_queue = Queue()
        self.listener = TweetListener(self.tweet_queue)

        connection = psycopg2.connect(database='trump')

    def get_db_credentials(self):

        self_location = os.path.split(__file__)[0]

        file_path = os.path.join(self_location,'secret','db.key')

        with open(file_path,'rU') as f:

            username = f.readline().strip()
            password = f.readline().strip()

    def start(self):

        self.message_loop()

    def message_loop(self):

        self.listener.start()

        while(True):

            message = self.tweet_queue.get(block=True)
            print message

    def insert_tweet_into_db(self, timestamp, text):

        'DY Mon DD HH24:MI:SS +0000 YYYY'
        return None

    def deconstruct_twitter_json(self, tweet_dict):

        time_created = tweet_dict['created_at']

        text = tweet_dict['text']

        return (time_created, text)

if __name__ == '__main__':

    tw_process = TweetProcessor(None)
    tw_process.start()