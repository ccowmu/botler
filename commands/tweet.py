@command("tweet")
def tweet(nick, user, channel, message):
    import commands.api
    apiurl = "http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&user=" +  message.split()[0] +"&api_key=" + apikey + "&format=json"
        jsonread = urllib.request.urlopen(apiurl)
        jsondata = jsonread.read()
        api = json.loads(jsondata.decode('utf8'))
