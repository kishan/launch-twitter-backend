"""
Resources for generating tweets
"""
from typing import List
import os
import tweepy
import requests
import json
from dotenv import load_dotenv

# load environment variables from .env
load_dotenv()

CONSUMER_KEY=os.environ.get('consumer_key')
CONSUMER_SECRET=os.environ.get('consumer_secret')
ACCESS_KEY=os.environ.get('access_key')
ACCESS_SECRET=os.environ.get('access_secret')
OPEN_AI_API_KEY=os.environ.get('open_ai_api_key')

BANNED_WORDS = ['http', '@',]

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

def get_tweet_text(tweet_id):
    """
    Get the text of a tweet
    """
    return "This is a tweet with id: {}".format(tweet_id)


def get_twitter_user_id(twitter_user_name):
    """
    Get the id of a twitter user
    """
    return 1234567890

def filter_words(tweet) -> str:
    """
    Filter out words that are not useful
    """
    for word in tweet.split():
        for banned_word in BANNED_WORDS:
            if banned_word in word:
                tweet = tweet.replace(word, '')
    return tweet

def get_user_timeline(username) -> List[str]:
    """
    Generate a new tweet text
    """
    #todo error handling
    max_tokens = 500
    max_len = 2048
    tweets_to_fetch_count = 5
    newest_tweets = api.user_timeline(screen_name=username, count=tweets_to_fetch_count, tweet_mode="extended")
    
    tweet_string = ''
    for tweet in newest_tweets:
        if len(tweet_string) + len(tweet.full_text) <= max_len - max_tokens:
            tweet_string += tweet.full_text + '\n---\n'

    # TODO: Filter out links
    print("------------------------------------")
    print("Tweets")
    print("------------------------------------")
    print(tweet_string)
    # openai.api_key = OPEN_AI_API_KEY
    # response = openai.Completion.create(engine="davinci", prompt=tweet_string, max_tokens=max_tokens)

    url = 'https://api.openai.com/v1/engines/davinci/completions'
    params = {
        'Content-Type': 'application/json',
        'auth': 'Bearer {}'.format(OPEN_AI_API_KEY),
        'data': { 
            'prompt': tweet_string,
            'max_tokens': max_tokens
        }
    }
    data_param = json.dumps({ 
            'prompt': tweet_string,
            'max_tokens': max_tokens
        })
    headers = {
        "Authorization": f"Bearer {OPEN_AI_API_KEY}",
        'Content-Type':'application/json'
        }

    response = requests.post(url, headers=headers, data=data_param)
    print("------------------------------------")
    print("OPEN AI Response")
    print("------------------------------------")
    print(response.text)

    generated_tweets_array = json.loads(response.text)['choices'][0]['text'].split('\n---\n')
    generated_tweets_array.pop(0)

    filtered_tweets = [filter_words(tweet) for tweet in generated_tweets_array]
    
    return filtered_tweets




# Search min faves between date and date