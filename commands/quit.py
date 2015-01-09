import sys

@command("quit", admin_only=True, op_only=False)
def quit(nick, channel, message):
    say(channel,'{} has commanded me to quit. Adios Asshats!'.format(nick))   
    sys.exit(0)
