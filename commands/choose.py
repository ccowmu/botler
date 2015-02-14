import random

@command("choose")
def choose(nick, user, channel, message):
    choices = message.split(sep = ",")
    #this line rids of empty choices caused by consecutive commas
    choices = [i for i in choices if i != '']
    if len(choices) > 0:
        choice = random.sample(choices, 1)
        #this line cleans up the winner, removing leading spaces and brackets
        winner = "".join(choice).strip()

        say(channel, "{}: {}".format(nick, winner))

    else:
        say(channel, "{}: Please give me things to choose from!".format(nick));
