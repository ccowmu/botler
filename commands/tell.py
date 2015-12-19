@command("tell")
def tell(nick, user, channel, message):
    channel = message.split(' ')[0]
    print(message)
    say(channel, "{}: {}".format(channel, message))

  
