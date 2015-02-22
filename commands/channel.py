@command("channel", man="Usage is '!channel <join / leave> <channel>'. Protected command.", adminonly=True)
def channel(nick, user, channel, message):
    if message.startswith("join"):
        chan = message.split(" ",1)[1].strip("\n \r")
        join(chan)
    elif message.startswith("leave"):
        chan = message.split(" ",1)[1].strip("\n \r")
        leave(chan)
    else:
        say(channel, "{}: Usage is '!channel <join / leave> <channel>'.".format(nick))
