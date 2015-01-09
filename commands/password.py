import os.path
import os
botname = 'botler'

@command("password", admin_only=True, op_only=False)
def password(nick, channel, message):
    if nick == channel:
        newpass = message.rstrip('\n')
        if os.path.exists('passfile'):
            pfile = open('passfile', 'r')
            password = pfile.readline()
            password = password.rstrip('\n')
            send('PRIVMSG NickServ RECOVER {} {}'.format(botname, password))
            send('PRIVMSG NickServ IDENTIFY {}'.format(password))
            send('PRIVMSG NickServ SET {} PASSWORD {} {}'.format(botname, password, newpass))
            pfile.close()
            pfile = open('passfile', 'w')
            pfile.write('{}\n'.format(newpass))
            pfile.close
        else:
            pfile = open('passfile', 'w')
            pfile.write('{}\n'.format(newpass))
            pfile.close()
            recover = os.urandom(7)
            recfile = open('recfile','w')
            recfile.write('{}\n'.format(recover))
            recfile.close()
            #print('Password:"{}"'.format(newpass))
            #print('Recovery:"{}"'.format(recover))
            send('PRIVMSG NickServ :REGISTER fuckyouasshole!')
    else:
        say(channel,'{}: This Can only Be Done From PM.'.format(nick))
        say(channel,'{}: Also, please use a different password now that everyone knows that one.'.format(nick))

