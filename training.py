
import nltk
import random
from nltk.classify.scikitlearn import SklearnClassifier
import pickle

from sklearn.naive_bayes import MultinomialNB, BernoulliNB
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.svm import SVC, LinearSVC, NuSVC

from nltk.classify import ClassifierI, MaxentClassifier
from statistics import mode
from nltk.tokenize import word_tokenize

# Inheriting from NLTK's ClassifierI.
# Next,assigning the list of classifiers that are passed to our class to self._classifiers.
class VoteClassifier(ClassifierI):
    def __init__(self, *classifiers):
        self._classifiers = classifiers

    #Creating our own classify method.
    #After iterating we return mode(votes), which just returns the most popular vote.
    def classify(self, features):
        votes = []
        for c in self._classifiers:
            v = c.classify(features)
            votes.append(v)
        return mode(votes)

    #Defining another parameter, confidence.
    #Since we have algorithms voting, we can tally the votes for and against the winning vote, and call this "confidence.
    def confidence(self, features):
        votes = []
        for c in self._classifiers:
            v = c.classify(features)
            votes.append(v)

        choice_votes = votes.count(mode(votes))
        conf = choice_votes / len(votes)
        return conf

# Defining and Accessing the corporas.
# In total, approx 10,000 feeds to be trained and tested on.
short_pos = open("Corporas/positive.txt","r").read()
short_neg = open("Corporas/negative.txt","r").read()

# move this up here
all_words = []
documents = []


#  j is adject, r is adverb, and v is verb
#allowed_word_types = ["J","R","V"]
allowed_word_types = ["J"]

# Splitting by a new line.
for p in short_pos.split('\n'):
    documents.append( (p, "pos") )
    words = word_tokenize(p)
    pos = nltk.pos_tag(words)
    for w in pos:
        if w[1][0] in allowed_word_types:
            all_words.append(w[0].lower())

    
for p in short_neg.split('\n'):
    documents.append( (p, "neg") )
    words = word_tokenize(p)
    pos = nltk.pos_tag(words)
    for w in pos:
        if w[1][0] in allowed_word_types:
            all_words.append(w[0].lower())

# Pickling documents.
save_documents = open("Pickles/documents.pickle","wb")
pickle.dump(documents, save_documents)
save_documents.close()

# Frequency Distribution
all_words = nltk.FreqDist(all_words)


word_features = list(all_words.keys())[:5000]


save_word_features = open("Pickles/word_features5k.pickle","wb")
pickle.dump(word_features, save_word_features)
save_word_features.close()

# Adjusting the feature finding function, using tokenizing by word in the document.
def find_features(document):
    words = word_tokenize(document)
    features = {}
    for w in word_features:
        features[w] = (w in words)

    return features

featuresets = [(find_features(rev), category) for (rev, category) in documents]

# Shuffling
random.shuffle(featuresets)
print(len(featuresets))

# Partitioning the training and the testing sets.
testing_set = featuresets[10000:]
training_set = featuresets[:10000]

# Pickling the featuresets.
save_features = open("featuresets.pickle","wb")
pickle.dump(featuresets, save_features)
save_features.close()

NuSVC_classifier = SklearnClassifier(NuSVC())
NuSVC_classifier.train(training_set)
print("NuSVC classifier algo accuracy percent: ", (nltk.classify.accuracy(NuSVC_classifier, testing_set))*100)

save_classifier = open("Pickles/NuSVC5k.pickle","wb")
pickle.dump(NuSVC_classifier, save_classifier)
save_classifier.close()

# Training and successive pickling of the classifiers.
maxent_classifier = nltk.MaxentClassifier.train(training_set)
print("Maximum entropy classifier algo accuracy percent: ",(nltk.classify.accuracy(maxent_classifier, testing_set))*100)

save_classifier = open("Pickles/maxentclassifier5k.pickle","wb")
pickle.dump(maxent_classifier, save_classifier)
save_classifier.close()

classifier = nltk.NaiveBayesClassifier.train(training_set)
print("Original Naive Bayes Algo accuracy percent:", (nltk.classify.accuracy(classifier, testing_set))*100)
classifier.show_most_informative_features(15)


save_classifier = open("Pickles/originalnaivebayes5k.pickle","wb")
pickle.dump(classifier, save_classifier)
save_classifier.close()

MNB_classifier = SklearnClassifier(MultinomialNB())
MNB_classifier.train(training_set)
print("MNB_classifier accuracy percent:", (nltk.classify.accuracy(MNB_classifier, testing_set))*100)

save_classifier = open("Pickles/MNB_classifier5k.pickle","wb")
pickle.dump(MNB_classifier, save_classifier)
save_classifier.close()

BernoulliNB_classifier = SklearnClassifier(BernoulliNB())
BernoulliNB_classifier.train(training_set)
print("BernoulliNB_classifier accuracy percent:", (nltk.classify.accuracy(BernoulliNB_classifier, testing_set))*100)

save_classifier = open("Pickles/BernoulliNB_classifier5k.pickle","wb")
pickle.dump(BernoulliNB_classifier, save_classifier)
save_classifier.close()

LogisticRegression_classifier = SklearnClassifier(LogisticRegression())
LogisticRegression_classifier.train(training_set)
print("LogisticRegression_classifier accuracy percent:", (nltk.classify.accuracy(LogisticRegression_classifier, testing_set))*100)

save_classifier = open("Pickles/LogisticRegression_classifier5k.pickle","wb")
pickle.dump(LogisticRegression_classifier, save_classifier)
save_classifier.close()


LinearSVC_classifier = SklearnClassifier(LinearSVC())
LinearSVC_classifier.train(training_set)
print("LinearSVC_classifier accuracy percent:", (nltk.classify.accuracy(LinearSVC_classifier, testing_set))*100)

save_classifier = open("Pickles/LinearSVC_classifier5k.pickle","wb")
pickle.dump(LinearSVC_classifier, save_classifier)
save_classifier.close()



SGDC_classifier = SklearnClassifier(SGDClassifier())
SGDC_classifier.train(training_set)
print("SGDClassifier accuracy percent:",nltk.classify.accuracy(SGDC_classifier, testing_set)*100)

save_classifier = open("Pickles/SGDC_classifier5k.pickle","wb")
pickle.dump(SGDC_classifier, save_classifier)
save_classifier.close()

# Voting classifier.
voted_classifier = VoteClassifier(
                                  classifier,
                                  LinearSVC_classifier,
                                  MNB_classifier,
                                  BernoulliNB_classifier,
                                  LogisticRegression_classifier)

print("voted_classifier accuracy percent:", (nltk.classify.accuracy(voted_classifier, testing_set))*100)


