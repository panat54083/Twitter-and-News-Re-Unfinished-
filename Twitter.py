
import secret
import tweepy
class twitter:
    def __init__(self) -> None:
        
        #authentication
        self.consumer_key = secret.twitter_consumer_key
        self.consumer_secret = secret.twitter_consumer_secret
        self.access_token =  secret.twitter_access_token
        self.access_token_secret =  secret.twitter_access_token_secret
        
        # tweepy configuration 
        self.auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
        self.auth.set_access_token(self.access_token, self.access_token_secret)
        self.api = tweepy.API(self.auth, wait_on_rate_limit=True)
    
        # searching configuration
        self.count = 100
        self.items = 100
        self.type = 'recent' # recent mixed popular
        self.mode = 'extended' # extended or compatibility mode

    def get_tweet_by_query(self, query, lang, day):

        for tweet in tweepy.Cursor(self.api.search_tweets,
                            q = query,
                            lang =lang,
                            count =self.count, 
                            result_type = self.type, 
                            tweet_mode = self.mode,
                            until = day
                            ).items(self.items):
            # get Text                
            tweet_text = self.get_text(tweet)
            tweet_date = self.get_date(tweet)
            tweet_re_count = self.get_retweet_count(tweet)
            tweet_source = self.get_source(tweet)
            

            print(tweet_source)
    
    def get_text(self, tweet):
        try: # for extended mode
            return tweet.full_text
        except: # for compatibility mode
            return tweet.text

    def get_date(self, tweet):
        date = tweet.created_at
        # date = date.strftime("%Y-%m-%d, %H:%M:%S")
        return date
    
    def get_retweet_count(self, tweet): # get number of retweet
        return tweet.retweet_count
    
    def get_source(self, tweet): # what type of tool that tweet or retweet
        return tweet.source 

if "__main__" == __name__:
    a = twitter()
    a.get_tweet_by_query('#Covid', 'en', '2022-04-06')

