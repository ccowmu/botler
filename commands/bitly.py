@command("bitly")
def bitly(nick, user, channel, message):
    import commands.api
    import json
    import urllib.request
    try:
        bitlyurl = "https://api-ssl.bitly.com/v3/shorten?access_token=" + bitlykey + "&longUrl=" + message
        jsonread = urllib.request.urlopen(bitlyurl)
        jsondata = jsonread.read()
        api = json.loads(jsondata.decode('utf8'))
        shorturl = api['data']['url']
        say(channel, '{}: {}'.format(nick, shorturl))
    except TypeError:
        say(channel, '{}: Invalid URL given.'.format(nick))
    else:
        pass
