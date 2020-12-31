import os
import tweepy
import time
import json
import pandas as pd
import os
import config


CONSUMER_KEY = config.CONSUMER_KEY
CONSUMER_SECRET = config.CONSUMER_SECRET
ACCESS_KEY = config.ACCESS_KEY
ACCESS_SECRET = config.ACCESS_SECRET

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)
FILE_NAME = 'last_seen_id.txt'
#Establish Arrays to store text
msgs = []
msg =[]
already_unfollowed = []
already_followed = []
#Establish the Desired HashTag
hashtag = '#BTC'
 #Create the column for tweet content
df = pd.DataFrame(columns=['text', 'user-id'])
#Set Display length to 90
pd.options.display.max_colwidth = 45

    #Reading the Last Seen tweet from the file
def read_last_seen(FILE_NAME):
    file_read = open(FILE_NAME, 'r')
    last_seen_id = int(file_read.read().strip())
    file_read.close()
    return last_seen_id

#Storing the Last seen tweet from the file
def store_last_seen(FILE_NAME, last_seen_id):
    file_write = open(FILE_NAME, 'w')
    file_write.write(str(last_seen_id))
    file_write.close()
    return


def unfollow():
        for user in reversed(already_followed):
            api.destroy_friendship(user)
            already_unfollowed.append(user)
        for user in already_unfollowed:
            already_followed.remove(user)

def run():
    for tweetContent in tweepy.Cursor(api.search, q=hashtag+'-filter:retweets', rpp=300, lang="en", tweet_mode='extended').items(50):
        msg = [tweetContent.full_text, tweetContent.user.screen_name]
        msg = tuple(msg)
        msgs.append(msg)
        api.create_friendship(tweetContent.user.screen_name)
        already_followed.append(tweetContent.user.screen_name)
        time.sleep(30)  
    dff = pd.DataFrame(already_followed)
    df = pd.DataFrame(msgs)
    print(dff.to_string())
    print(df.to_string())
    print('All the users whove recently tweeted about BTC have been followed')
    store_last_seen(FILE_NAME, tweetContent.id)

#loop to constantly run the bot
true = True
while(true):
    # Run and Wait 4 hours 4/24HRS
    run()
    time.sleep(14400)
    # Run and Wait 4 Hours 8/24HRS
    run()
    time.sleep(14400)
    # Run and Wait 4 Hours 12/24HRS
    run()
    time.sleep(14400)
    # Run and Wait 4 Hours 16/24HRS
    run()
    time.sleep(14400) 
    # Run and Wait 4 Hours 20/24HRS
    run()
    time.sleep(14400)
    # Run Unfollow to unfollow
    unfollow()