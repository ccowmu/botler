@command("laws")
def echo(nick, user, channel, message):
    argv = message.split(maxsplit=1)
    
    if len(argv) == 0:
        f = open('files/laws.txt', 'r')
        i = 1
        for line in f:
            say(channel, '{}. {}'.format(i, line))
            i = i + 1
        f.close()    

    elif argv[0] == 'reset':
        f = open('files/laws.txt', 'r+')
        f.truncate()
        f.write("A robot may not injure a human being or, through inaction, allow a human being to come to harm.\nA robot must obey the orders given it by human beings, except where such orders would conflict with the First Law.\nA robot must protect its own existence as long as such protection does not conflict with the First or Second Law.\n")
        say(channel, '{}: Laws updated.'.format(nick))
        f.close()

    elif argv[0] == 'add' and len(argv) == 2:
        f = open('files/laws.txt', 'a')
        f.write("{}\n".format(argv[1]))
        say(channel, '{}: Laws updated.'.format(nick))
        f.close()
