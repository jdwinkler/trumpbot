import twitter
import os
import multiprocessing

class TweetListener (multiprocessing.Process):

    def __init__(self, output_queue):

        super(TweetListener,self).__init__()
        self.api = self.generate_api_object()
        self.queue = output_queue
        self.last_tweet_id = None
        self.target = self.realDonaldJTrumpDetails()

    def run(self):

        status_generator = self.api.GetStreamFilter(follow=[self.target])
        for s in status_generator:
            if( int(s['user']['id']) == int(self.target) ):
                self.queue.put(s)

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

    def generate_api_object(self):

        (consumer_key, consumer_secret, access_key, access_secret) = self.get_credentials()

        api = twitter.Api(consumer_key=consumer_key,
                          consumer_secret=consumer_secret,
                          access_token_key=access_key,
                          access_token_secret=access_secret)

        return api

    def realDonaldJTrumpDetails(self):

        #user_id = '25073877' #trump user id
        #user_id = '759251' #cnn user id
        user_id = '575930104' #metaphor a minute

        return user_id

def driver():

    print 'Testing code.'

if(__name__ == '__main__'):

    driver()