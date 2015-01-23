@command("bitly")
def bitly(nick, channel, message):
    import commands.api
    import json
    import urllib.request
    longurl = message
    try:
        bitlyurl = "https://api-ssl.bitly.com/v3/shorten?access_token=" + bitlykey + "&longUrl=" + longurl + "/"
        jsonread = urllib.request.urlopen(message)
        jsondata = jsonread.read()
        api = json.loads(jsondata.decode('utf8'))
        shorturl = api['data']['url']
        say(channel, '{}: {}'.format(nick, shorturl))
    except ValueError:
        say(channel, '{}: Invalid URL given.'.format(nick))
    except TypeError:
        say(channel, '{}: Invalid URL given.'.format(nick))
    else:
        pass
