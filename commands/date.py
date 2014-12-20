import time

@command("date")
def echo(nick, channel, message):
    say(channel, time.strftime("%A, %B %d, %Y.\r\n"))
