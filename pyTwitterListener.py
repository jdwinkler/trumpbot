import os
import multiprocessing

class TweetListener (multiprocessing.Process):

    def __init__(self, api, output_queue):

        super(TweetListener,self).__init__()
        self.api = api
        self.queue = output_queue
        self.last_tweet_id = None
        self.target = self.realDonaldJTrumpDetails()

    def run(self):

        status_generator = self.api.GetStreamFilter(follow=[self.target])
        for s in status_generator:
            if( int(s['user']['id']) == int(self.target) ):
                self.queue.put(s)

    def realDonaldJTrumpDetails(self):

        #user_id = '25073877' #trump user id
        #user_id = '759251' #cnn user id
        user_id = '575930104' #metaphor a minute

        return user_id

def driver():

    print 'Testing code.'

if(__name__ == '__main__'):

    driver()