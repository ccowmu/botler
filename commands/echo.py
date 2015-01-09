@command("echo", admin_only=False, op_only=False)
def echo(nick, channel, message):
    say(channel, '{}: {}'.format(nick, message))
