import time

@command("date")
def date(nick, channel, message):
    say(channel, time.strftime("%A, %B %d, %Y.\r\n"))
