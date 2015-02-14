@command("echo")
def echo(nick, user, channel, message):
    say(channel, '{}: {}'.format(nick, message))
