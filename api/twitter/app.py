#!/usr/bin/env python3

# import urlparse to check given twitter url is valid
from urllib.parse import urlparse

# get api and its authentication credentials
from auth import Api


# twitter url parser. this function is validator
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