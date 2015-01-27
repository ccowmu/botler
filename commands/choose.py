import random

@command("choose")
def choose(nick, channel, message):
    choices = message.split(sep = ",")
    choices = [i for i in choices if i != '']
    choice = random.sample(choices, 1)
    winner = "".join(choice).strip()

    say(channel, "{}: {}".format(nick, winner))
