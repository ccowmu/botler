@command("quit", admin_only=True)
def echo(nick, channel, message):
    say('{} has commanded me to quit. Adios Asshats!'.format(nick))   
    time.sleep(7) 
    sys.exit(0)
