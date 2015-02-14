@command("echo", man="Usage: '!echo <message>'")
def echo(nick, user, channel, message):
    say(channel, '{}: {}'.format(nick, message))
