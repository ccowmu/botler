#!/usr/bin/env python3

# botler: the CCoWMU IRC bot.

import socket
import logging
import sys
import glob
import datetime
import traceback
try:
    import psycopg2 #Postgresql
except ImportError:
    pass
import os
import re
import configparser

config = configparser.ConfigParser()
config.read("config.ini")

HOST = config['botler']['HOST']
PORT = int(config['botler']['PORT'])
NICK = config['botler']['NICK']
IDENT = config['botler']['IDENT']
REALNAME = config['botler']['REALNAME']
LEADER = config['botler']['LEADER']
START_CHANNELS = list(config['botler']['START_CHANNELS'].split(','))
DB_DB = config['botlerdb']['DB_DB']
DB_USER = config['botlerdb']['DB_USER']
DB_HOST = config['botlerdb']['DB_HOST']
DB_PASS = os.environ.get('DB_PASS')
DB_LOGGING = config['botlerdb']['DB_LOGGING'].lower() == 'true'

channels = []

# from http://news.anarchy46.net/2012/01/irc-message-regex.html
IRC_RE = re.compile(r'^(:(?P<prefix>\S+) )?(?P<command>\S+)( (?!:)(?P<params>.+?))?( :(?P<trail>.+))?\r$')

def command(name, **options):
    '''Decorator for command functions.

    Example usage:

    @command("echo", option="value", ...)
    def echo(nick, channel, message):
        say(channel, '{}: {}'.format(nick, message))

    To add a man message: man="<message>"
    To restrict to botler admins: adminonly=True
    To restrict to botler admins and whitelisted users: whitelist:True

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
        db=db,
        join=join,
        leave=leave,
        send=send,
        reload_admins=reload_admins,
        bcast=bcast,
    )
    for source in glob.glob('commands/*.py'):
        try:
            exec(compile(open(source).read(), source, 'exec'), command_globals)
        except Exception as e:
            log.error(traceback.format_exc())

def reload_admins():
    '''Reload all admins and whitelisted users.'''
    global ADMINS
    global WHITELIST
    config = configparser.ConfigParser()
    config.read("config.ini")
    ADMINS = list(config['botler']['ADMINS'].split(','))
    WHITELIST = list(config['botler']['WHITELIST'].split(','))

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

def db_logwrite(nick, ircuser, command_, message, channel):
    if db == None or not DB_LOGGING: return
    query = """INSERT INTO log (time, nick, ircuser, command, message, channel)
               VALUES (%s, %s, %s, %s, %s, %s);"""
    now = str(datetime.datetime.now()).split('.')[0]
    with db as conn:
        with conn.cursor() as cursor:
            cursor.execute(query, (now, nick, ircuser, command_[:4], message, channel))

def join(channel):
    global channels
    send('JOIN {}'.format(channel))
    send("PRIVMSG {} :{} is now online and running...".format(channel, NICK))
    channels.append(channel)

def leave(channel):
    global channels
    send('PART {}'.format(channel))
    if channel in channels:
        channels.remove(channel)

def bcast(nick, original, message):
    global channels
    for channel in channels:
        say(channel, "{} announces from {}: {}".format(nick, original, message))

log = logging.getLogger(__name__)
log.addHandler(logging.StreamHandler(sys.stderr))
log.setLevel(logging.DEBUG)

db = None
try:
    db = psycopg2.connect(dbname=DB_DB, user=DB_USER, host=DB_HOST, password=DB_PASS)
    log.info('Established connection to database {} as user {}@{}'.format(DB_DB, DB_USER, DB_HOST))
except NameError:
    pass

s = socket.socket()
log.info('Connecting to {}:{} as {}'.format(HOST, PORT, NICK))

s.connect((HOST, PORT))
send('NICK {}'.format(NICK))
send('USER {} {} bla :{}'.format(IDENT, HOST, REALNAME))
for channel in START_CHANNELS:
    join(channel)
log.info('Connected')

reload_commands()
reload_admins()

while 1:
    data = recv()
    prefix, command_, params, trail = parse(data)
    if command_ == 'PING':
        send('PONG {}'.format(data.split()[1]))
    if command_ == 'KICK':
        params = params.split(' ')
        print(params[1])
        if params[1] == NICK:
            channels.remove(params[0])
    if command_ == 'PRIVMSG':
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
        db_logwrite(nick, ircuser, command_, message, target)
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
                try:
                    if "adminonly" in commands[command_] and commands[command_]["adminonly"] == True:
                        if ircuser in ADMINS:
                            commands[command_]['method'](nick, ircuser, channel, message)
                        else:
                            say(channel, "{}: You are not authorised to use this command.".format(nick))
                    elif "whitelist" in commands[command_] and commands[command_]["whitelist"] == True:
                        if ircuser in ADMINS or ircuser in WHITELIST:
                            commands[command_]['method'](nick, ircuser, channel, message)
                        else:
                            say(channel, "{}: You are not authorised to use this command.".format(nick))
                    else:
                        commands[command_]['method'](nick, ircuser, channel, message)
                except Exception as e:
                    log.error("command {} failed: {}".format(command_, e))
                    say(channel, "{}: command failed".format(command_))
            elif command_ == 'reload':
                reload_commands()
            elif command_ == 'man':
                man_parts = message.split()
                if man_parts == []:
                    #lists all commands if there's none specified
                    list_commands = ""
                    if ircuser in ADMINS:
                        for i in commands:
                            list_commands += i + ", "
                    elif ircuser in WHITELIST:
                        for i in commands:
                            if not "adminonly" in commands[i]:
                                list_commands += i + ", "
                    else:
                        for i in commands:
                            if not "adminonly" in commands[i] and not "whitelist" in commands[i]: 
                                list_commands += i + ", "
                    list_commands = list_commands[:-2]
                    say(channel, "{}: Available commands - {}".format(nick, list_commands))
                elif man_parts[0] in commands:
                    if "man" in commands[man_parts[0]]:
                        say(channel, "{}: {}".format(nick, commands[man_parts[0]]["man"]))
                    else:
                        say(channel, "{}: None available for command".format(nick))
                else:
                    say(channel, '{}: unknown command "{}"'.format(nick, man_parts[0]))
            else:
                say(channel, 'unknown command "{}"'.format(command_))

# vim: ts=4:sw=4:et
