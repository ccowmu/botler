@command("tweet")
def tweet(nick, channel, message):
    CONSUMER_KEY = "jpAHE5alGs9jx44dFZwXeq1Qh"
    CONSUMER_SECRET = "occSPW1TPd5yZxr9EfB4r1lsCADk6wqQaEmdRJLgJeRjxG5jYy"
    ACCESS_KEY = "172595184-zE9JlBmyoaULNrNBeNpvBSINLKcfYd7EG1lD7fAx"
    ACCESS_SECRET = "gO2BastCjP0W5MjVDSCebwjNVMjiwyGRNkH0SvT0AVgvk"
    apiurl = "http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&user=" +  message.split()[0] +"&api_key=" + apikey + "&format=json"
        jsonread = urllib.request.urlopen(apiurl)
        jsondata = jsonread.read()
        api = json.loads(jsondata.decode('utf8'))
