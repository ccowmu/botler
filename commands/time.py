import time

@command("time")
def time(nick, channel, message):
    say(channel, time.strftime("%I:%M %p.\r\n"))
