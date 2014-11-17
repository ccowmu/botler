@command("echo")
def echo(nick, channel, message):
    say(channel, '{}: {}'.format(nick, message))
