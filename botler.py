#!/usr/bin/env python3

# botler: the CCoWMU IRC bot.

import socket
import logging
import sys
import glob
import time
import os.path

HOST = 'localhost'
PORT = 6667
NICK = 'botler'
IDENT = 'botler'
REALNAME = 'botler'
LEADER = '!'
START_CHANNELS = ['#hackathon']

log = logging.getLogger(__name__)
log.addHandler(logging.StreamHandler(sys.stderr))
log.setLevel(logging.DEBUG)

commands = dict()

def command(name, **options):
    '''Decorator for command functions.

    Example usage:

    @command("echo", option="value", ...)
    def echo(nick, channel, message):
        say(channel, '{}: {}'.fomat(nick, message))

    '''
    def decorator(f):
        options['method'] = f
        commands[name] = options
        return f
    return decorator

def send(message):
    # TODO: break message up based on maximum message size
    log.info('[>] {}'.format(message))
    s.send('{}\r\n'.format(message).encode('utf-8'))

def recv():
    # TODO: buffer until one line
    message = s.recv(2048).decode('utf-8')
    log.info('[<] {}'.format(message))
    return message

def say(channel, message):
    send('PRIVMSG {} :{}'.format(channel, message))

def isadmin(username):
    print('Checking to see if {} is an admin...'.format(username))
    adminlistfile = open('adminlist','r')
    for line in adminlistfile:
        currentname = line.rstrip('\n')
        if username == currentname:
            adminlistfile.close()
            return True
    adminlistfile.close()
    return False

def isop(username):
    print('Checking to see if {} is an op or admin'.format(username))
    if isadmin(username):
        return True
    else:
        oplistfile = open('oplist','r')
        for line in oplistfile:
            currentname = line.rstrip('\n')
            if username == currentname:
                oplistfile.close()
                return True
        oplistfile.close()
        return False
def getopstatus():
    if os.path.exists('commands/passfile'):
        passwordfile = open('commands/passfile')
        password = passwordfile.readline()
        password = password.rstrip('\n')
        send('PRIVMSG NickServ IDENTIFY {}'.format(password)) 
        passwordfile.close()
   
def reload_commands():
    '''Reload all source files in commands directory.'''
    global commands
    commands = dict()
    # Globals dict for the command source.
    command_globals = dict(
        command=command,
        say=say,
        send=send,
    )
    for source in glob.glob('commands/*.py'):
        exec(compile(open(source).read(), source, 'exec'), command_globals)

s = socket.socket()
log.info('Connecting to {}:{} as {}'.format(HOST, PORT, NICK))
s.connect((HOST, PORT))
send('NICK {}'.format(NICK))
send('USER {} {} bla :{}'.format(IDENT, HOST, REALNAME))
#getopstatus()
for channel in START_CHANNELS:
    send('JOIN {}'.format(channel))
    send("PRIVMSG {} :{} is now online and running...".format(channel,NICK))
    # send('PRIVMSG ChanServ OP {} {}'.format(channel,NICK))

log.info('Connected')

reload_commands()

while 1:
    data = recv()
    # TODO: parse message properly
    if data.find('PING') != -1:
        send('PONG {}'.format(data.split()[1])) 
    if data.find('PRIVMSG') != -1:
        parts = data.split(sep=' ', maxsplit=3)
        if len(parts) == 4:
            # Raw parts of the original message
            # source PRIVMSG target :message
            real_source = parts[0]
            real_target = parts[2]
            real_message = parts[3]

            # Extract source user nick
            # :nick!user@host
            nick = real_source.split('!')[0][1:]
            # If a user PRIVMSG's us we appear as the target
            if real_target == NICK:
                channel = nick
            else:
                channel = nick = real_target

            # Final parameter (message) is often prefixed with ':'
            if real_message.startswith(':'):
                message = real_message[1:]
            else:
                message = real_message

            # Check if we need to care about this message
            if message.startswith(LEADER):
                parts = message.split(maxsplit=1)
                command_ = parts[0][len(LEADER):]
                # Give a default value for message if none is provided.
                if len(parts) == 2:
                    message = parts[1]
                else:
                    message = ""
                # Invoke associated command or error
                if command_ in commands:
                    if commands[command_]['admin_only']:
                        if isadmin(nick):
                            commands[command_]['method'](nick, channel, message)
                        else:
                            say(channel, '{}: You are Not an Admin!!!'.format(nick))                        
                    else:
                        commands[command_]['method'](nick, channel, message)
                elif command == 'reload':
                    reload_commands()
                else:
                    say(channel, 'unknown command "{}"'.format(command_))

        else:
            log.warn('Invalid PRIVMSG detected with {} != 4 parts'.format(len(parts)))

# vim: ts=4:sw=4:et
