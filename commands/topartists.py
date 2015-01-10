@command("topartists")
def topartists(nick, channel, message):
    import json
    import urllib.request
    try:
        apikey = "ac54cee27cfcc900bf83d7b2ce82b2ca"
        apiurl = "http://ws.audioscrobbler.com/2.0/?method=user.gettopartists&user=" + message.split()[0] + "&period=overall&api_key=ac54cee27cfcc900bf83d7b2ce82b2ca&format=json"
        jsonread = urllib.request.urlopen(apiurl)
        jsondata = jsonread.read()
        api = json.loads(jsondata.decode('utf8'))
        artist1 = api['topartists']['artist'][0]['name']
        artist2 = api['topartists']['artist'][1]['name']
        artist3 = api['topartists']['artist'][2]['name']
        artist4 = api['topartists']['artist'][3]['name']
        artist5 = api['topartists']['artist'][4]['name']
        data = "Top 5 Artists for " + message.split()[0] + ": " + artist1 + ", " + artist2 + ", " + artist3 + ", " + artist4 + ", " + artist5 + "."
        say(channel, data)
    except KeyError:
        say(channel, '{}: Invalid username given.'.format(nick))
    else:
        pass
