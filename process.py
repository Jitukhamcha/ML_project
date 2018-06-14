import nltk
import re,csv
import pickle
import sys
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem.porter import PorterStemmer
import sentimental_analysis as senti


def handle_emojis(tweet):
    # Smile -- :), : ), :-), (:, ( :, (-:, :')
    tweet = re.sub(r'(:\s?\)|:-\)|\(\s?:|\(-:|:\'\))', ' EMO_POS ', tweet)
    # Laugh -- :D, : D, :-D, xD, x-D, XD, X-D
    tweet = re.sub(r'(:\s?D|:-D|x-?D|X-?D)', ' EMO_POS ', tweet)
    # Love -- <3, :*
    tweet = re.sub(r'(<3|:\*)', ' EMO_POS ', tweet)
    # Wink -- ;-), ;), ;-D, ;D, (;,  (-;
    tweet = re.sub(r'(;-?\)|;-?D|\(-?;)', ' EMO_POS ', tweet)
    # Sad -- :-(, : (, :(, ):, )-:
    tweet = re.sub(r'(:\s?\(|:-\(|\)\s?:|\)-:)', ' EMO_NEG ', tweet)
    # Cry -- :,(, :'(, :"(
    tweet = re.sub(r'(:,\(|:\'\(|:"\()', ' EMO_NEG ', tweet)
    return tweet


def preprocessing(dataSet):

    processed_data = []

    #Make a list of all the Stopwords to be removed
    #stopwords = generateStopWordList()

    #For every TWEET in the dataset do,
    for tweet in dataSet:

        temp_tweet = tweet
        # Replaces URLs with the word URL
        tweet = re.sub(r'((www\.[\S]+)|(https?://[\S]+))', ' URL ',tweet)
        tweet.replace(temp_tweet, tweet)

        # Remove RT (retweet)
        tweet = re.sub(r'\brt\b', '', tweet)
        tweet.replace(temp_tweet, tweet)

        # Strip space, " and ' from tweet
        tweet = tweet.strip(' "\'')
        tweet.replace(temp_tweet, tweet)

        # Replace emojis with either EMO_POS or EMO_NEG
        tweet = handle_emojis(tweet)
        tweet.replace(temp_tweet, tweet)

        #Convert @username to USER_MENTION
        tweet = re.sub('@[^\s]+','USER_MENTION',tweet).lower()
        tweet.replace(temp_tweet, tweet)

        #Remove the unnecessary white spaces
        tweet = re.sub('[\s]+',' ', tweet)
        tweet.replace(temp_tweet,tweet)

        #Replace #HASTAG with only the word by removing the HASH (#) symbol
        tweet = re.sub(r'#([^\s]+)', r'\1', tweet)
        tweet.replace(temp_tweet, tweet)

        #Replace all the numeric terms
        tweet = re.sub('[0-9]+', "",tweet)
        tweet.replace(temp_tweet,tweet)

        #Remove all the STOP WORDS
        stop_words = set(stopwords.words('english'))
        for sw in stop_words:
            if sw in tweet:
                tweet = re.sub(r'\b' + sw + r'\b'+" ","",tweet)
        tweet.replace(temp_tweet, tweet)

        stopword_blacklist=['url','avengersinfinitywar','user_mention','https','http','rt']
        for sw in stopword_blacklist:
            if sw in tweet:
                tweet = re.sub(r'\b' + sw + r'\b' + " ", "", tweet)
        tweet.replace(temp_tweet, tweet)

        #Replace all Punctuations
        tweet = re.sub('[^a-zA-z ]',"",tweet)
        tweet.replace(temp_tweet,tweet)

        #Remove additional white spaces
        tweet = re.sub('[\s]+',' ', tweet)
        tweet.replace(temp_tweet,tweet)
        # Replace multiple spaces with a single space
        tweet = re.sub(r'\s+', ' ', tweet)
        tweet.replace(temp_tweet, tweet)

        # Remove punctuation
        tweet = tweet.strip('\'"?!,.():;')
        tweet.replace(temp_tweet, tweet)
        # Convert more than 2 letter repetitions to 2 letter
        # funnnnny --> funny
        tweet = re.sub(r'(.)\1+', r'\1\1', tweet)
        tweet.replace(temp_tweet, tweet)
        # Remove - & '
        tweet = re.sub(r'(-|\')', '', tweet)
        tweet.replace(temp_tweet, tweet)


        #Save the Processed Tweet after data cleansing
        processed_data.append(tweet)
    print("returninga data")
    return processed_data


if __name__ == '__main__':

    dataSet = open("infinity.csv").readlines()

    print("Preprocessing in progress ...")

    pre_data = preprocessing(dataSet)
    print("printing data")
    print(pre_data)
    #saving preprocessed data in txt file
    thefile = open('pre_data1.txt', 'w')
    for item in pre_data:
        thefile.write("%s\n" % item)

    #passing processed data as argument
    input = open("pre_data1.txt")
    filename = input.readline()
  #  print(senti.sentiment("fucking dumb movie"))
    print("process on going...")
    print(senti.sentiment(filename))

    # #dataset1 = open("nishan.txt").readlines()
    # #jungle_processed = preprocessing(dataset1)
    #
    # print(jungle_processed)
    # thefile1 = open('infinity.txt','w')
    # for item in jungle_processed:
    #     thefile1.write("%s\n" % item)
    #
    # input= open("jungle_processed.txt")
    # file1= input.readline()
    # print(senti.sentiment(file1))









