import time

@command("time")
def echo(nick, channel, message):
    say(channel, time.strftime("%I:%M %p.\r\n"))
