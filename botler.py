#!/usr/bin/env python3

# botler: the CCoWMU IRC bot.

import socket

HOST = 'localhost'
PORT = 6667
NICK = "botler"
IDENT = 'botler'
REALNAME = 'botler'
LEADER = '%'
START_CHANNELS = ['#hackathon']

def send(message):
    # TODO: break message up based on maximum message size
    s.send('{}\r\n'.format(message))

def recv():
    # TODO: buffer until one line
    return s.recv(2048)

def say(channel, message):
    send('PRIVMSG {} :{}'.format(channel, message))

s = socket.socket()
print('Connecting to {}:{} as {}'.format(HOST, PORT, NICK))

s.connect((HOST, PORT))
send('NICK {}'.format(NICK))
send('USER {} {} bla :{}'.format(IDENT, HOST, REALNAME))
for channel in START_CHANNELS:
    send('JOIN {}'.format(channel))
    send("PRIVMSG {} :Botler is Now Online and Running...".format(channel))
print('Connected')

while 1:
    data = recv()
    # TODO: parse message properly
    if data.find('PING') != -1:
        send('PONG {}'.format(data.split()[1])) 
    if data.find("hello") != -1:
        log("Hello! May I invite you to bite my shiny virtual ass?")

# vim: ts=4:sw=4:et
