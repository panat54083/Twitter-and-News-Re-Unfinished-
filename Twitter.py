
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
        self.no_retweet = True # Don't get retweet

    def get_tweet_by_query(self, query, lang, day):

        query = self.get_retweet_or_not(query)

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
            tweet_location = self.get_location(tweet)

            print(tweet_text)
    def get_retweet_or_not(self, query):
        if self.no_retweet:
            return query+ " -filter:retweets" 
        else:
            return query+ " filter:retweets" 

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

    def get_location(self, tweet): 
        if type(tweet) is tweepy.models.Status:
            tweet = tweet.__dict__
        # get the place from the place data inside the tweet dictionary
        place = tweet['user'].location
        try:
            place = place.split(', ')[-1].upper()
            return place
        except :
            return None

if "__main__" == __name__:
    a = twitter()
    
    a.get_tweet_by_query('#Covid', 'en', '2022-04-06')

