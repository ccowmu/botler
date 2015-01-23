@command("lastfm")
def lastfm(nick, channel, message):
    import commands.api
    import json
    import urllib.request
    apiurl = "http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&user=" +  message.split()[0] +"&api_key=" + lastfmkey + "&format=json"
    jsonread = urllib.request.urlopen(apiurl)
    jsondata = jsonread.read()
    api = json.loads(jsondata.decode('utf8'))
    try:
        nowplaycheck = api['recenttracks']['track'][0]['@attr']['nowplaying']
    except KeyError:
        nowplaycheck = "false"
    else:
        pass
    if nowplaycheck == "true":
        try:
            song = api['recenttracks']['track'][0]['name']
            artist = api['recenttracks']['track'][0]['artist']['#text']
            album = api['recenttracks']['track'][0]['album']['#text']
            data = "Now Playing for " + message.split()[0] + ": " + song + " by " + artist + " on " + album + "."
            say(channel, data)
        except KeyError:
            say(channel, '{}: Invalid username given.'.format(nick))
        except IndexError:
            say(channel, '{}: Invalid username given.'.format(nick))
        else:
            pass
    else:
        try:
            song = api['recenttracks']['track'][0]['name']
            artist = api['recenttracks']['track'][0]['artist']['#text']
            album = api['recenttracks']['track'][0]['album']['#text']
            date = api['recenttracks']['track'][0]['date']['#text']
            data = "Recent track for " + message.split()[0] + " (Played on " + date + ")" ": " + song + " by " + artist + " on " + album + "."
            say(channel, data)
        except KeyError:
            say(channel, '{}: Invalid username given.'.format(nick))
        except IndexError:
            say(channel, '{}: Invalid username given.'.format(nick))
        else:
            pass
