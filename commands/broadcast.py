@command("broadcast", man="Usage is '!broadcast <message>'. This is an admin protected command.", adminonly=True)
def broadcast(nick, user, channel, message):
    bcast(nick, channel, message)
