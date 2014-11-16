#!/usr/bin/env python3

# botler: the CCoWMU IRC bot.

import socket
import logging
import sys

HOST = 'localhost'
PORT = 6667
NICK = 'botler'
IDENT = 'botler'
REALNAME = 'botler'
LEADER = '%'
START_CHANNELS = ['#hackathon']

log = logging.getLogger(__name__)
log.addHandler(logging.StreamHandler(sys.stderr))
log.setLevel(logging.DEBUG)

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

s = socket.socket()
log.info('Connecting to {}:{} as {}'.format(HOST, PORT, NICK))

s.connect((HOST, PORT))
send('NICK {}'.format(NICK))
send('USER {} {} bla :{}'.format(IDENT, HOST, REALNAME))
for channel in START_CHANNELS:
    send('JOIN {}'.format(channel))
    send("PRIVMSG {} :botler is now online and running...".format(channel))
log.info('Connected')

while 1:
    data = recv()
    # TODO: parse message properly
    if data.find('PING') != -1:
        send('PONG {}'.format(data.split()[1])) 
    if data.find('PRIVMSG') != -1:
        parts = data.split(sep=' ', maxsplit=4)
        if len(parts) == 4:
            # Raw parts of the original message
            real_source = parts[0]
            real_target = parts[2]
            real_message = parts[3]

            # Final parameter (message) is often prefixed with ':'
            if real_message.startswith(':'):
                message = real_message[1:]
            else:
                message = real_message

            # If a user PRIVMSG's us we appear as the target
            if real_target == NICK:
                channel = real_source
            else:
                channel = real_target

            # Echo
            say(channel, message)
        else:
            log.warn('Invalid PRIVMSG detected with {} != 4 parts'.format(len(parts)))

# vim: ts=4:sw=4:et
