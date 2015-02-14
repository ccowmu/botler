@command("reddit")
def reddit(nick, channel, message):
    # try:
    #     import json
    #     import requests
    #     subreddit = message.split()[0]
    #     ACCESS_TOKEN = "5936e225282f49fa0e3e20b386141c6ce141e0dc"
    #     apiurl = "http://www.reddit.com/r/" + subreddit + "/top/.json?sort=top&t=day&limit=1"
    #     jsonread = urllib.request.urlopen(apiurl)
    #     jsondata = jsonread.read()
    #     api = json.loads(jsondata.decode('utf8'))
    #     title = api['data']['children'][0]['data']['title']
    #     subreddit = api['data']['children'][0]['data']['subreddit']
    #     longurl = api['data']['children'][0]['data']['url']
    #     bitlyurl = "https://api-ssl.bitly.com/v3/shorten?access_token=" + ACCESS_TOKEN + "&longUrl=" + longurl
    #     jsonread = urllib.request.urlopen(bitlyurl)
    #     jsondata = jsonread.read()
    #     api = json.loads(jsondata.decode('utf8'))
    #     data = api['data']['url']
    #     foo = (title + " - " + data + " - (/r/" + subreddit + ")")
    #     say(channel, '{}: {}'.format(nick, foo))
    # except IndexError:
    #     import json
    #     import urllib.request
    #     ACCESS_TOKEN = "5936e225282f49fa0e3e20b386141c6ce141e0dc"
    #     apiurl = "http://www.reddit.com/top/.json?sort=top&t=day&limit=1"
    #     jsonread = urllib.request.urlopen(apiurl)
    #     jsondata = jsonread.read()
    #     api = json.loads(jsondata.decode('utf8'))
    #     title = api['data']['children'][0]['data']['title']
    #     subreddit = api['data']['children'][0]['data']['subreddit']
    #     longurl = api['data']['children'][0]['data']['url']
    #     bitlyurl = "https://api-ssl.bitly.com/v3/shorten?access_token=" + ACCESS_TOKEN + "&longUrl=" + longurl
    #     jsonread = urllib.request.urlopen(bitlyurl)
    #     jsondata = jsonread.read()
    #     api = json.loads(jsondata.decode('utf8'))
    #     data = api['data']['url']
    #     foo = (title + " - " + data + " - (/r/" + subreddit + ")")
    #     say(channel, '{}: {}'.format(nick, foo))
    # except urllib.error.HTTPError:
    #     say(channel, "Too many requests. Try again later.")
    # else:
    #     pass
    #

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
