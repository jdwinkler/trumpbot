import psycopg2
import psycopg2.extras
import twitter
import os

def insert_tweet_into_db(timestamp, text):

    'DY Mon DD HH24:MI:SS +0000 YYYY'

def deconstruct_twitter_json(tweet_dict):

    time_created = tweet_dict['created_at']

    text = tweet_dict['text']

    return (time_created, text)

def get_credentials():

    credential_file = os.path.join(os.path.split(__file__)[0], 'secret','api.key')

    with open (credential_file,'rU') as f:

        consumer_key = f.readline().strip()
        consumer_secret = f.readline().strip()
        access_key = f.readline().strip()
        access_secret = f.readline().strip()

    return (consumer_key, consumer_secret, access_key, access_secret)

def realDonaldJTrumpDetails():

    user_id = 'realDonaldTrump'

    return user_id

def generate_api_object():

    (consumer_key, consumer_secret, access_key, access_secret) = get_credentials()

    api = twitter.Api(consumer_key=consumer_key,
                      consumer_secret=consumer_secret,
                      access_token_key=access_key,
                      access_token_secret=access_secret)

    return api

def extract_tweets_from_user(username, output_file_name):

    import pickle

    api = generate_api_object()

    stored_tweet_objects = []


    max_id =  None
    prev_max_id = 0

    while(prev_max_id != max_id):

        djt_timeline = api.GetUserTimeline(screen_name=username,
                                           count=200,
                                           max_id=max_id)

        stored_tweet_objects.extend(djt_timeline)

        prev_max_id = max_id

        max_id = djt_timeline[-1].id

    pickle.dump(stored_tweet_objects,open(output_file_name,'wb'))

if(__name__ == '__main__'):

    import pickle
    import codecs

    pickle_path = os.path.join(os.getcwd(),'sentiment','DJT Twitter Status Objects.obj')

    stored_djt_statuses = pickle.load(open(pickle_path,'rb'))

    seen_already = set()

    filtered_statuses = []

    for status in stored_djt_statuses:

        if(status.id not in seen_already):
            filtered_statuses.append(status)
            seen_already.add(status.id)

    print len(filtered_statuses), len(stored_djt_statuses)

    strings_to_replace = [(u'\u2026','...')]

    print u'\u2026'

    with codecs.open('trump_mini_corpus.txt','w',encoding='ascii') as f:

        for status in filtered_statuses:

            text = status.text.encode('ascii','ignore')

            try:
                f.write('\t'.join([str(status.id), text.replace('\n',' ')]) + '\n')
            except:
                print text
