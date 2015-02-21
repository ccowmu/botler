@command("bitly")
def bitly(nick, user, channel, message):
    import commands.api
    import requests
    from urllib.parse import quote
    import json
    try:
        link = message.split()[0]
        if(link.startswith("http://") == False):
            link = "http://" + link
        params = {'longUrl': link, 'format': 'json', 'access_token': bitlykey}
        r = requests.get('https://api-ssl.bitly.com/v3/shorten', params=params)
        data = json.loads(r.content.decode('utf8'))
        shorturl = data['data']['url']
        say(channel, '{}: {}'.format(nick, shorturl))
    except ValueError:
        say(channel, '{}: Invalid URL given.'.format(nick))
    except TypeError:
        say(channel, '{}: Invalid URL given.'.format(nick))
    except IndexError:
        say(channel, '{}: Invalid URL given.'.format(nick))
    else:
        pass
