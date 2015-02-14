@command("laws")
def echo(nick, user, channel, message):
    argv = message.split(maxsplit=1)
    
    if len(argv) == 0:
        try:
            f = open('files/laws.txt', 'r')
            for i,line in enumerate(f):
                say(channel, '{}. {}'.format(i+1, line))
            f.close()    
        except IOError:
            say(channel,"Error: Coulh not open laws.txt!")

    elif argv[0] == 'reset':
        f = open('files/laws.txt', 'w')
        f.write("A robot may not injure a human being or, through inaction, allow a human being to come to harm.\nA robot must obey the orders given it by human beings, except where such orders would conflict with the First Law.\nA robot must protect its own existence as long as such protection does not conflict with the First or Second Law.\n")
        f.close()
        say(channel, '{}: Laws updated.'.format(nick))

    elif argv[0] == 'add' and len(argv) == 2:
        f = open('files/laws.txt', 'a')
        f.write("{}\n".format(argv[1]))
        f.close()
        say(channel, '{}: Laws updated.'.format(nick))
