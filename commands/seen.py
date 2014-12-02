#Flays seen function
@command("seen")

#set function to calculate time away. "Attentiveness"
#def timeago():	

def seen(log, nick, channel):
    say(channel, '{}: {}'.format(nick, "was last seen in",channel,timeago))
