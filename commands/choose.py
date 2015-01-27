import random

@command("choose")
def choose(nick, channel, message):
    choices = message.split(sep = ",")
    #this line rids of empty choices caused by consecutive commas
    choices = [i for i in choices if i != '']
    choice = random.sample(choices, 1)
    #this line cleans up the winner, removing leading spaces and brackets
    winner = "".join(choice).strip()

    say(channel, "{}: {}".format(nick, winner))
