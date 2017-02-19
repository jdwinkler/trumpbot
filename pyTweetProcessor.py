from multiprocessing import Queue
import psycopg2
import psycopg2.extras
from pyTwitterListener import TweetListener
from pyTextAnalyzer import TweetClassifier
import os
import time

class TweetProcessor:

    def __init__(self):

        self.tweet_queue = Queue()
        self.listener = TweetListener(self.tweet_queue)
        self.classifier = TweetClassifier()

        username, password  = self.get_db_credentials()

        self.connection = psycopg2.connect(database='trump',
                                      user=username,
                                      password=password)

        self.cursor = self.connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

        self.situation_normal = 2
        self.situation_raised = 5
        self.situation_alert  = 7
        self.situation_redalert = 9
        self.situation_pinnacle_nucflash = 15

    def __del__(self):

        self.cursor.close()
        self.connection.commit()
        self.connection.close()

    def get_db_credentials(self):

        self_location = os.path.split(__file__)[0]

        file_path = os.path.join(self_location,'secret','db.key')

        with open(file_path,'rU') as f:

            username = f.readline().strip()
            password = f.readline().strip()

        return (username, password)

    def start(self):

        self.message_loop()

    def message_loop(self):

        self.listener.start()

        contiguous_negative_counter = 0
        previous_sentiment = 'pos'
        time_recorded = time.time()
        time_to_reset = 1800 #seconds to reset negative counter

        while(True):

            try:
                message = self.tweet_queue.get(block=True, timeout=time_to_reset)
            except:
                self.react(contiguous_negative_counter)
                contiguous_negative_counter = 0
                time_recorded = time.time()
                continue

            if(time.time() - time_recorded > time_to_reset):
                self.react(contiguous_negative_counter)
                contiguous_negative_counter = 0
                time_recorded = time.time()

            (timestamp, text) = self.deconstruct_twitter_json(message)

            predicted_sentiment = self.classifier.classify_tweet(text)

            self.insert_tweet_into_db(timestamp, text, predicted_sentiment)

            if(predicted_sentiment == 'neg' and previous_sentiment == 'neg'):
                contiguous_negative_counter+=1
            else:
                contiguous_negative_counter =0

    def react(self, nc):

        if(nc <= self.situation_normal):
            print 'Trump status: nominal, detected few or no upset tweets in past window'
        elif(nc > self.situation_normal and nc <= self.situation_raised ):
            print 'Trump status: irritated, detected stream of %i annoyed tweets' % nc
        elif(nc > self.situation_raised and nc <= self.situation_alert):
            print 'Trump status: anger rising, detected stream of %i angry tweets' % nc
        elif(nc > self.situation_alert and nc <= self.situation_redalert):
            print 'Trump status: rage\'s cup runneth over, detected stream of %i enraged tweets' % nc
        elif(nc > self.situation_redalert and nc <= self.situation_pinnacle_nucflash):
            print 'Trump status: crisis imminent or occurring, detected stream of %i furious tweets' % nc
        elif(nc > self.situation_pinnacle_nucflash):
            print 'Trump status: PINNACLE NUCFLASH; run for the hills, detected stream of %i apoplectic tweets' % nc

    def insert_tweet_into_db(self, timestamp, text, sentiment):

        self.cursor.execute('select to_timestamp(%s, %s) as creation_time', (timestamp, 'DY Mon DD HH24:MI:SS +0000 YYYY'))

        converted_postgres_timestamp = self.cursor.fetchone()['creation_time']

        print converted_postgres_timestamp, text, sentiment

        sql_query = 'insert into tweets (created, tweet, sentiment) VALUES (%s, %s, %s)'

        try:

            self.cursor.execute(sql_query, (converted_postgres_timestamp, text, sentiment))
            self.connection.commit()
            success = True

        except Exception, err:

            print 'DB exception: cannot insert recorded tweet'
            print err.message
            print 'Skipping...'
            success = False

        return success

    def deconstruct_twitter_json(self, tweet_dict):

        time_created = tweet_dict['created_at']

        text = tweet_dict['text']

        return (time_created, text)

if __name__ == '__main__':

    tw_process = TweetProcessor()
    tw_process.start()