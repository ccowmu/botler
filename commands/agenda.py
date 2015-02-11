white_list=("themind","flay","stringy","sphinx")
@command("agenda")
def agenda(nick, channel, message):
    if nick not in white_list:
        say("%s: Sorry, you're not authorized to use this feature."%nick)
