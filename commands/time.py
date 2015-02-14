import time

@command("time")
def time(nick, user, channel, message):
    say(channel, time.strftime("%I:%M %p.\r\n"))
