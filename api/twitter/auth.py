import tweepy
import configparser

class Api:

    # Read configs
    config = configparser.ConfigParser()
    config.read('../../config/twitter_config.ini')

    # Authentication
    auth = tweepy.OAuthHandler(config['twitter']['api_key'],
                               config['twitter']['api_key_secret'])

    auth.set_access_token(config['twitter']['access_token'],
                          config['twitter']['access_token_secret'])

    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)