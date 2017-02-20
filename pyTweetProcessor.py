from multiprocessing import Queue
from pyTwitterListener import TweetListener
from pyTextAnalyzer import TweetClassifier
import twitter
import os
import time
import itertools

class TweetProcessor:

    def __init__(self, debug=True):

        self.api = self.generate_api_object()
        self.tweet_queue = Queue()
        self.listener = TweetListener(self.api, self.tweet_queue)
        self.classifier = TweetClassifier()
        self.debug_status = debug

        self.time_window = 1800 #seconds

        self.situation_normal = 1
        self.situation_raised = 2
        self.situation_alert  = 3
        self.situation_redalert = 4
        self.situation_pinnacle_nucflash = 5

    def generate_api_object(self):

        try:

            (consumer_key, consumer_secret, access_key, access_secret) = self.get_credentials()

        except:

            import os

            consumer_key = os.environ['consumer_key'.upper()]
            consumer_secret = os.environ['consumer_secret'.upper()]
            access_key = os.environ['access_token_key'.upper()]
            access_secret = os.environ['access_token_secret'.upper()]

        api = twitter.Api(consumer_key=consumer_key,
                          consumer_secret=consumer_secret,
                          access_token_key=access_key,
                          access_token_secret=access_secret)

        return api

    def get_credentials(self):

        credential_file = os.path.join(os.path.split(__file__)[0],
                                       'secret',
                                       'api.key')

        with open (credential_file,'rU') as f:

            consumer_key = f.readline().strip()
            consumer_secret = f.readline().strip()
            access_key = f.readline().strip()
            access_secret = f.readline().strip()

        return (consumer_key, consumer_secret, access_key, access_secret)

    def start(self):

        self.message_loop()

    def message_loop(self):

        self.listener.start()

        contiguous_negative_counter = 0
        time_recorded = time.time()
        time_to_reset = self.time_window

        tw_counter = 0

        while(True):

            if(tw_counter >= 144):
                tw_counter = 0

            try:
                message = self.tweet_queue.get(block=True, timeout=time_to_reset)
            except:
                self.react(contiguous_negative_counter, tw_counter)
                contiguous_negative_counter = 0
                time_recorded = time.time()
                tw_counter+=1
                continue

            if(time.time() - time_recorded > time_to_reset):
                self.react(contiguous_negative_counter, tw_counter)
                contiguous_negative_counter = 0
                time_recorded = time.time()
                tw_counter += 1

            (timestamp, text) = self.deconstruct_twitter_json(message)

            predicted_sentiment = self.classifier.classify_tweet(text)

            self.insert_tweet_into_db(timestamp, text, predicted_sentiment)

            if(predicted_sentiment == 'neg'):
                contiguous_negative_counter+=1

            print 'Negativity state: %i' % contiguous_negative_counter
            print 'Last predicted states: %s' % predicted_sentiment

    def react(self, nc, marker):

        text = None

        if(nc <= self.situation_normal):
            text = 'Trump status: nominal, detected few or no upset tweets in past window'
        elif(nc > self.situation_normal and nc <= self.situation_raised ):
            text = 'Trump status: irritated, detected stream of %i annoyed tweets' % nc
        elif(nc > self.situation_raised and nc <= self.situation_alert):
            text = 'Trump status: anger rising, detected stream of %i angry tweets' % nc
        elif(nc > self.situation_alert and nc <= self.situation_redalert):
            text = 'Trump status: rage\'s cup runneth over, detected stream of %i enraged tweets' % nc
        elif(nc > self.situation_redalert and nc <= self.situation_pinnacle_nucflash):
            text = 'Trump status: crisis imminent or occurring, detected stream of %i furious tweets' % nc
        elif(nc > self.situation_pinnacle_nucflash):
            text = 'Trump status: PINNACLE NUCFLASH; run for the hills, detected stream of %i apoplectic tweets' % nc

        text = str(marker) + '. ' + text

        if(self.debug_status):
            print text
        else:
            self.api.PostUpdate(text)

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

    tw_process = TweetProcessor(debug=False)
    tw_process.start()