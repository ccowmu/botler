#!/usr/bin/env python3

# botler: the CCoWMU IRC bot.

import socket
import logging
import sys
import glob
import datetime
import traceback

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

chatlog = open("chatlog", "r+")
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

def reload_commands():
    '''Reload all source files in commands directory.'''
    global commands
    commands = dict()
    # Globals dict for the command source.
    command_globals = dict(
        command=command,
        say=say,
    )
    for source in glob.glob('commands/*.py'):
        try:
            exec(compile(open(source).read(), source, 'exec'), command_globals)
        except Exception as e:
            log.error(traceback.format_exc())

def logwrite(data):
    chatlog.write(datetime.datetime.now().strftime("[%c] {0}").format(data))
    chatlog.write(data)
    chatlog.flush()

s = socket.socket()
log.info('Connecting to {}:{} as {}'.format(HOST, PORT, NICK))

s.connect((HOST, PORT))
send('NICK {}'.format(NICK))
send('USER {} {} bla :{}'.format(IDENT, HOST, REALNAME))
for channel in START_CHANNELS:
    send('JOIN {}'.format(channel))
    send("PRIVMSG {} :botler is now online and running...".format(channel))
log.info('Connected')

reload_commands()

while 1:
    data = recv()
    # TODO: parse message properly
    if data.find('PING') != -1:
        send('PONG {}'.format(data.split()[1])) 
    if data.find('PING') != 1:
        logwrite(data)
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
                channel = real_target

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
                    commands[command_]['method'](nick, channel, message)
                elif command_ == 'reload':
                    reload_commands()
                else:
                    say(channel, 'unknown command "{}"'.format(command_))

        else:
            log.warn('Invalid PRIVMSG detected with {} != 4 parts'.format(len(parts)))

# vim: ts=4:sw=4:et
