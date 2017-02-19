
#todo: add text stripping (stopwords)
#todo: add punctuation removal

from nltk.classify import NaiveBayesClassifier
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from nltk.corpus import opinion_lexicon
from nltk.tokenize import TweetTokenizer
import os

import nltk

class TweetClassifier:

    def __init__(self, test = False, corpus = 'trump'):

        self.stemmer = PorterStemmer()

        #removes common low content words that occur in english sentences
        self.english_stops = set([w.upper() for w in stopwords.words('english')])
        self.english_stops.add('RT')

        #positive adjectives (stemmed for consistency)
        self.positive_adj = set([self.stemmer.stem(w).upper() for w in opinion_lexicon.positive()])

        #negative adjectives (stemmed for consistency)
        self.negative_adj = set([self.stemmer.stem(w).upper() for w in opinion_lexicon.negative()])

        if(corpus == 'trump'):

            tweet_corpus = os.path.join(os.getcwd(), 'sentiment','trump_mini_corpus_labeled.txt')
            processed_tweets = self.load_tweet_corpus(tweet_corpus)
            self.classifier = self.train_classifier(processed_tweets, test=test)

        else:
            raise AssertionError('Unknown corpus requested: %s ' % corpus)

    def classify_tweet(self, raw_tweet_text):

        processed_tweet = self.clean_up_tweet(raw_tweet_text)
        word_features = self.word_feats(processed_tweet)

        return self.classifier.classify(word_features)

    def train_classifier(self, processed_tweets, test = False):

        if(test):

            extent = len(processed_tweets) * 3/4

            training_features = processed_tweets[:extent]
            test_features = processed_tweets[extent:]

            temp_class = NaiveBayesClassifier.train(training_features)

            print 'accuracy:',nltk.classify.accuracy(temp_class,test_features)
            temp_class.show_most_informative_features()

        return NaiveBayesClassifier.train(processed_tweets)

    def word_feats(self, words):

        output_dict = dict()

        pos_count = 0
        neg_count = 0

        for word in words:

            if(word in self.positive_adj):
                pos_count += 1

            if(word in self.negative_adj):
                neg_count += 1

            output_dict[word] = True

        if(pos_count > neg_count):
            output_dict['positive_features'] = True
        elif(pos_count < neg_count):
            output_dict['negative_features'] = True

        return output_dict

    def clean_up_tweet(self, tweet_text, stem=True):

        breaker = TweetTokenizer(strip_handles=True)

        words_components_to_ignore = {'/',':','@','HTTPS','.','...','..',
                                      'PRIME',
                                      'JAPAN',
                                      'SECRETARY',
                                      'MINISTER',
                                      'PENNSYLVANIA',
                                      'FLORIDA'}
        word_tokens_to_ignore = {'-'}

        tweet_text = tweet_text.replace('"','').replace('\'','').replace('(','').replace(')','').replace(',','')
        tweet_text = tweet_text.replace('American','America')

        tweet_words = breaker.tokenize(tweet_text)

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

            if(word not in self.english_stops):

                if(stem):
                    temp.append(self.stemmer.stem(word).upper())
                else:
                    temp.append(word.upper())

        tweet_words = temp

        return tweet_words

    def load_tweet_corpus(self, file_path):

        tweets = []
        with open(file_path,'rU') as f:

            for line in f:

                if(len(line.strip()) == 0):
                    continue

                tokens = line.strip().split('\t')
                text = tokens[1]
                sentiment = tokens[-1].strip('"')

                if(sentiment == '3'):
                    sentiment = 'neg'
                elif(sentiment == '1'):
                    sentiment = 'pos'
                else:
                    sentiment = 'pos'

                tweet_words = self.clean_up_tweet(text)
                tweets.append((self.word_feats(tweet_words),sentiment))

        return tweets

#print 'accuracy:', nltk.classify.util.accuracy(classifier, testfeats)
#classifier.show_most_informative_features(n=20)

if(__name__ == '__main__'):

    classifier = TweetClassifier(test=False, corpus='trump')
