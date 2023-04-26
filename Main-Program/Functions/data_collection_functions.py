############# Data Collection #############

import pandas as pd
import requests
        
def create_Twitter_headers(bearer_token):
    headers = {"Authorization": "Bearer {}".format(bearer_token)}
    return headers        
        
def getTweetsByUserID(user_id, header, max_results = 50):
    tweets_url = f'https://api.twitter.com/2/users/{user_id}/tweets?max_results={max_results}'
    return connect_to_endpoint(tweets_url, header)
    
def getSingleTweetInfo(tweetID, header):
    tweets_url = f'https://api.twitter.com/2/tweets?tweet.fields=created_at,conversation_id,in_reply_to_user_id,author_id,referenced_tweets&ids={tweetID}'
    return connect_to_endpoint(tweets_url, header)
    
def getTwitterUserInfo(username, header):
    user_result = f'https://api.twitter.com/2/users/by?usernames={username}&user.fields=created_at&expansions=pinned_tweet_id&tweet.fields=author_id,created_at'
    return connect_to_endpoint(user_result, header)
    
def getTweetsLikedByUser(userID, header, max_results = 30):
    user_result = f'https://api.twitter.com/2/users/{userID}/liked_tweets?max_results={max_results}'
    return connect_to_endpoint(user_result, header)
    
def getUsersLikesForTweet(tweetID, header):
    tweet_result = f'https://api.twitter.com/2/tweets/{tweetID}/liking_users'
    return connect_to_endpoint(tweet_result, header)

def connect_to_endpoint(url, headers, next_token = None):    
    response = requests.request("GET", url, headers = headers)
        
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
        
    return response.json()