import nltk.classify.util
from nltk.classify import NaiveBayesClassifier
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from nltk.corpus import opinion_lexicon
from nltk.tokenize import TweetTokenizer
import os

stemmer = PorterStemmer()

positive_adj = set([stemmer.stem(w).upper() for w in opinion_lexicon.positive()])
negative_adj = set([stemmer.stem(w).upper() for w in opinion_lexicon.negative()])

def word_feats(words):

    output_dict = dict()

    pos_count = 0
    neg_count = 0

    for word in words:

        if(word in positive_adj):
            pos_count += 1

        if(word in negative_adj):
            neg_count += 1

        output_dict[word] = True

    if(pos_count > neg_count):
        output_dict['positive_features'] = True
    elif(pos_count < neg_count):
        output_dict['negative_features'] = True

    return output_dict

def load_tweet_corpus(file_path):

    breaker = TweetTokenizer(strip_handles=True)

    english_stops = set([w.upper() for w in stopwords.words('english')])
    english_stops.add('RT')

    words_components_to_ignore = {'/',':','@','HTTPS','.','...','..',
                                  'PRIME',
                                  'JAPAN',
                                  'SECRETARY',
                                  'MINISTER',
                                  'PENNSYLVANIA',
                                  'FLORIDA'}
    word_tokens_to_ignore = {'-'}

    tweets = []
    with open(file_path,'rU') as f:

        for line in f:

            if(len(line.strip()) == 0):
                continue

            tokens = line.strip().split('\t')
            text = tokens[1].strip().replace('"','').replace('\'','').replace('(','').replace(')','').replace(',','')
            text = text.replace('American','America')
            sentiment = tokens[-1].strip('"')

            if(sentiment == '3'):
                sentiment = 'neg'
            elif(sentiment == '1'):
                sentiment = 'neu'
            else:
                sentiment = 'pos'

            tweet_words = breaker.tokenize(text)

            temp = []

            for word in tweet_words:

                skip = False

                word = word.upper()

                for ignore_token in words_components_to_ignore:
                    if(ignore_token in word):
                        skip = True

                for ignore_token in word_tokens_to_ignore:
                    if(ignore_token == word):
                        skip = True

                if(len(word) < 2):
                    skip = True

                if(skip):
                    continue

                if(word not in english_stops):
                    temp.append(stemmer.stem(word).upper())

            tweet_words = temp

            tweets.append((tweet_words,sentiment))

    return tweets

tweet_corpus = os.path.join(os.getcwd(), 'sentiment','trump_mini_corpus_labeled.txt')

negative_features = []
neutral_features = []
positive_features = []

processed_tweets = load_tweet_corpus(tweet_corpus)

for (tweet, sentiment) in processed_tweets:

    if(sentiment == 'neg'):
        negative_features.append((word_feats(tweet),sentiment))
    elif(sentiment == 'neu'):
        positive_features.append((word_feats(tweet),'pos'))
    else:
        positive_features.append((word_feats(tweet),sentiment))

negcutoff = len(negative_features)*3/4
neucutoff = len(neutral_features)*3/4
poscutoff = len(positive_features)*3/4

trainfeats = negative_features[:negcutoff] + positive_features[:poscutoff] + neutral_features[:neucutoff]
testfeats = negative_features[negcutoff:] + positive_features[poscutoff:] + neutral_features[neucutoff:]
print 'train on %d instances, test on %d instances' % (len(trainfeats), len(testfeats))

classifier = NaiveBayesClassifier.train(trainfeats)
#print 'accuracy:', nltk.classify.util.accuracy(classifier, testfeats)
#classifier.show_most_informative_features(n=20)