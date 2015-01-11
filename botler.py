#!/usr/bin/env python3

# botler: the CCoWMU IRC bot.

import socket
import logging
import sys
import glob
import datetime
import traceback
import psycopg2 #Postgresql
import os
import re

HOST = 'localhost'
PORT = 6667
NICK = 'botler'
IDENT = 'botler'
REALNAME = 'botler'
LEADER = '!'
START_CHANNELS = ['#hackathon']
DB_DB = 'botler'
DB_USER = 'botler'
DB_HOST = 'localhost'
DB_PASS = os.environ.get('DB_PASS', input('DB_PASS? '))

# from http://news.anarchy46.net/2012/01/irc-message-regex.html
IRC_RE = re.compile(r'^(:(?P<prefix>\S+) )?(?P<command>\S+)( (?!:)(?P<params>.+?))?( :(?P<trail>.+))?\r$')

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

# Parse a raw IRC message and return a tuple containing:
# (prefix, command, params, trail)
# with all elements being either a string if present or None if absent
def parse(data):
    """ Parse a raw IRC message and return a tuple of its parts.

    The returned tuple is of the form:
    (prefix, command, params, trail)
    where all elements will be either a string or None
    """
    match = IRC_RE.match(data)
    if match:
        return (match.group('prefix'), match.group('command'),
                match.group('params'), match.group('trail'))
    else:
        return (None, None, None, None)

def db_logwrite(nick, ircuser, command, message, channel):
    query = """INSERT INTO log (time, nick, ircuser, command, message, channel)
               VALUES (%s, %s, %s, %s, %s, %s);"""
    now = str(datetime.datetime.now()).split('.')[0]
    with db as conn:
        with conn.cursor() as cursor:
            cursor.execute(query, (now, nick, ircuser, command[:4], message, channel))

log = logging.getLogger(__name__)
log.addHandler(logging.StreamHandler(sys.stderr))
log.setLevel(logging.DEBUG)

db = psycopg2.connect(dbname=DB_DB, user=DB_USER, host=DB_HOST, password=DB_PASS)
log.info('Established connection to database {} as user {}@{}'.format(DB_DB, DB_USER, DB_HOST))

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
    prefix, command, params, trail = parse(data)
    if command == 'PING':
        send('PONG {}'.format(data.split()[1])) 
    if command == 'PRIVMSG':
        # prefix looks like
        # nick!user@host
        bang_splits = prefix.split('!')
        at_splits = bang_splits[1].split('@')

        nick = bang_splits[0]
        ircuser = at_splits[0]
        # only param should be target of PRIVMSG
        target = params
        # the rest is the body of the message
        message = trail

        # If a user PRIVMSG's us we appear as the target remember to respond
        # directly to them, not to ourselves
        if target == NICK:
            channel = nick
        else:
            channel = target

        # Log all messages
        db_logwrite(nick, ircuser, command, message, target)
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

# vim: ts=4:sw=4:et
