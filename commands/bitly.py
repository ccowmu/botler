@command("bitly")
def bitly(nick, channel, message):
    import json
    import urllib.request
    try:
        ACCESS_TOKEN = "5936e225282f49fa0e3e20b386141c6ce141e0dc"
        bitlyurl = "https://api-ssl.bitly.com/v3/shorten?access_token=" + ACCESS_TOKEN + "&longUrl=" + message
        jsonread = urllib.request.urlopen(bitlyurl)
        jsondata = jsonread.read()
        api = json.loads(jsondata.decode('utf8'))
        shorturl = api['data']['url']
        say(channel, '{}: {}'.format(nick, shorturl))
    except TypeError:
        say(channel, '{}: Invalid URL given.'.format(nick))
    else:
        pass
