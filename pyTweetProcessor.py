from multiprocessing import Queue
from pyTwitterListener import TweetListener
from pyTextAnalyzer import TweetClassifier
import os
import time

class TweetProcessor:

    def __init__(self):

        self.tweet_queue = Queue()
        self.listener = TweetListener(self.tweet_queue)
        self.classifier = TweetClassifier()

        self.time_window = 600 #seconds

        self.situation_normal = 2
        self.situation_raised = 5
        self.situation_alert  = 7
        self.situation_redalert = 9
        self.situation_pinnacle_nucflash = 15

    def start(self):

        self.message_loop()

    def message_loop(self):

        self.listener.start()

        contiguous_negative_counter = 0
        time_recorded = time.time()
        time_to_reset = self.time_window

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

            if(predicted_sentiment == 'neg'):
                contiguous_negative_counter+=1

            print 'Negativity state: %i' % contiguous_negative_counter
            print 'Last predicted states: %s' % predicted_sentiment

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

        try:

            with open('TrumpDB.file','w') as f:
                f.write('\t'.join([timestamp, text, sentiment]) + '\n')

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