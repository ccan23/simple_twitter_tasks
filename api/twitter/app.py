#!/usr/bin/env python3

# import urlparse to check given twitter url is valid
from urllib.parse import urlparse

# get api and its authentication credentials
from auth import Api


# twitter url parser. this function is validator
# TwitterTasks class needs variables returned by twitter_url_parser function
def twitter_url_parser(url: str) -> dict:
    """Check the Twitter URL and parse if the URL is valid

    Args:
        url (str): Twitter URL

    Returns:
        dict: Extract the username and tweet id from the given URL and store it,
                it also includes whether the URL belongs to twitter.com
                and the error message if an error occured              
    """

    # parse the url and declare variables
    parsed = urlparse(url)
    tweet_id, screen_name, error_message = str(), str(), str()

    # check if website domain is twitter
    if parsed.netloc == 'twitter.com':
        is_twitter = True

        # parse the url path and store it in the path_list variable
        path_list = parsed.path.split('/')

        # if path_list variable is not equal to 4, the url is not as requested
        #! this part of script isn't going to work as expected if the user puts '/' to the end of the url
        if len(path_list) == 4:

            # get twitter username and tweet id
            screen_name, status, tweet_id = path_list[1], path_list[2], path_list[3]

            # try to find '/status/' in twitter url to check url is as requested
            if status != 'status':
                error_message = ''  # TODO: status is not as requested (error message 001)

        else:
            error_message = ''  # TODO: url length error message (error message 002)

    else:
        is_twitter = False
        error_message = ''  # TODO: given url is not twitter its something else (error message 003)

    return {
        'is_twitter': is_twitter,
        'error_message': error_message,
        'screen_name': screen_name,
        'tweet_id': tweet_id
    }

#* TwitterTasks class .. this class must be execute after twitter_url_parser function
class TwitterTasks:

    # constructor
    def __init__(self, api: 'tweepy.api.API', screen_name: str, tweet_id: str):
        self.api = api
        self.screen_name = screen_name
        self.tweet_id = tweet_id
        self.tweet = self.api.get_status(self.tweet_id, tweet_mode='extended')

    # TODO: Tasks: mention 2 nft friends, retweet and like the selected post by team and follow

    #* task 01
    # check if posted tweet mentions at least 2 users
    # we don't need to check if the mentioned user is real or not because if the user is not real,
    # twitter api doesn't return any value about it
    #! but we need to check if the accounts are suspended or not because twitter api shows suspended accounts anyway !
    def task_mention(self, min_user_count: int) -> dict:
        """Check if the user mentioned enough amount of users in his/her post

        Args:
            min_user_count (int): Mentioned user minimum limit

        Returns:
            dict: Includes user mentions, the task is complete or not and an error message if any error has occurred
        """

        # declare variables
        error_message = str()

        # get the user mentions
        user_mentions = [
            mention['screen_name']
            for mention in self.tweet.entities['user_mentions']
        ]

        # if mentioned user count is equals or greater than min_user_count, the task is done
        if len(user_mentions) >= min_user_count:
            task_complete = True

        else:
            task_complete = False
            error_message = ''  # TODO: mentioned users is not enough (error message 004)

        return {
            'task_complete': task_complete,
            'error_message': error_message,
            'user_mentions': user_mentions
        }

    #* task 02
    # check if the tweet post has posted selected hashtag
    def task_hashtag(self, hashtag: str) -> dict:
        """Check if user posted required hashtag.

        Args:
            hashtag (str): Hashtags on Twitter

        Returns:
            dict: Includes hashtags, the task is complete or not and an error message if any error has occurred
        """

        # declare variable (error message)
        error_message = str()

        # hashtag could be more than one but one of them must be required hashtag
        # get the hashtags and store it in list
        hashtags = [
            _hashtag['text'].lower()
            for _hashtag in self.tweet.entities['hashtags']
        ]

        # check if the desired hashtag is in the list
        if hashtag.lower() in hashtags:
            task_complete = True

        else:
            task_complete = False
            error_message = ''  # TODO: hashtag can't found in tweet (error message 005)

        return {
            'task_complete': task_complete,
            'error_message': error_message,
            'hashtags': hashtags
        }

    #* task 03
    # check if the tweet post has required retweet
    def task_retweet(self, main_account: str, quoted_status_id_str: str) -> dict:

        error_message = str()

        #? couldn't get quoted_status without converting tweepy object to json object
        #? I don't have time to figure it out right now but it works anyway
        quoted_status = self.tweet._json.get('quoted_status')

        # check if quoted status exist and not None
        if quoted_status:

            # get quoted user and quoted status id from tweet
            quoted_user = quoted_status['user']['screen_name']
            quoted_id = quoted_status['quoted_status_id_str']

            # check if quoted user and quoted status id are correct
            if quoted_user == main_account and quoted_id == quoted_status_id_str:
                task_complete = True

            else:
                task_complete = False
                error_message = '' # TODO: wrong tweet has retweeted (error message 006)

        else:
            task_complete = False
            error_message = ''  # TODO: retweet can't found in tweet (error message 007)

        return {
            'task_complete': task_complete,
            'error_message': error_message,
            'quoted_user': quoted_user,
            'quoted_id': quoted_id
        }

    def task_follow(self) -> dict:
        """Check if user following you

        Returns:
            dict: Includes task status and error message (if any)
        """

        error_message = str()

        if self.tweet._json['user']['following']:
            task_complete = True

        else:
            task_complete = False
            error_message = '' # TODO: user is not following you (error message 008)

        return {
            'task_complete': task_complete,
            'error_message': error_message
        }