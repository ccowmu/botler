@command("tweet")
def tweet(nick, user, channel, message):
    import commands.api
    import requests
    from requests_oauthlib import OAuth1
    from urllib.parse import quote
    message = quote(message)
    approved_users = {'mobyte', 'flay', 'cpg', 'sphinx'}
    def query(apiurl):
        oauth = OAuth1(twitter_consumer_key, twitter_consumer_secret, twitter_access_key, twitter_access_secret, signature_type = 'auth_header')
        return requests.post(apiurl, auth = oauth)
    if nick not in approved_users:
        say(channel, '{} is not in the approved users list.'.format(nick))
    elif message == '':
        say(channel, '{}: to tweet, use the format !tweet <tweet>.'.format(nick))
    else:
        query('https://api.twitter.com/1.1/statuses/update.json?status=' + message)
        message = "Success."
        say(channel, '{}: {}'.format(nick, message))
