from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import json
import sentimental_analysis as s

#consumer key, consumer secret, access token, access secret.
ckey="RAxIgCbN2wSCD9MJHtXYUBF0x"
csecret="Rw46XsfBZ3A4HZQdjj8OGSNA2Ens6aME3yF7VG4v9wiIVwxlsW"
atoken="3184832665-wksGoxXmvAUCuZyvRRMvlMA1etVC4kHd6ARfavt"
asecret="zPJnCmrKBygp9taHAmG1oHJt2UyxISM7U6yMnuTstgMcj"


class listener(StreamListener):

    def on_data(self, data):

        all_data = json.loads(data)
        tweet = all_data["text"]
        sentiment_value, confidence = s.sentiment(tweet)
        print(tweet, sentiment_value, confidence)

        if confidence*100 >= 60:
            output = open("twitter-out.txt","a")
            output.write(sentiment_value)
            output.write('\n')
            output.close()

        return True
    def on_error(self, status):
        print(status)

auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)

twitterStream = Stream(auth, listener())
twitterStream.filter(track=["avengerinfinity"])
