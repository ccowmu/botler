@command("reddit")
def reddit(nick, user, channel, message):
    import requests
    import json
    import commands.api
    try:
        redditurl = "http://www.reddit.com/r/" + message.split()[0] + "/top.json"
    except IndexError:
        redditurl = "http://www.reddit.com/r/all/top.json"
    except KeyError:
        redditurl = "http://www.reddit.com/r/all/top.json"
    else:
        redditurl = "http://www.reddit.com/r/all/top.json"
    headers = {'User-Agent': 'botler', 'top': 'day', 'limit': 1}
    params = {'top': 'day', 'limit': 1}
    r = requests.get(redditurl, headers=headers, params=params)
    data = json.loads(r.content.decode('utf8'))
    title = data['data']['children'][0]['data']['title']
    subreddit = data['data']['children'][0]['data']['subreddit']
    longurl = data['data']['children'][0]['data']['url']
    params2 = {'longUrl': longurl, 'format': 'json', 'access_token': bitlykey}
    r2 = requests.get('https://api-ssl.bitly.com/v3/shorten', params=params2)
    data = json.loads(r2.content.decode('utf8'))
    shorturl = data['data']['url']
    foo = (title + " - " + shorturl + " - (/r/" + subreddit + ")")
    say(channel, '{}: {}'.format(nick, foo))
