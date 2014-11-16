#Botler.py
import os
import sys
import socket
import string
import datetime
import smtplib

HOST = "dot"
PORT = 6667
NICK = "Botler"
IDENT = 'Botler'
REALNAME = 'Botler'
readbuffer = ""
mainchannel = "#hackathon"
readbuffer = ''
s = socket.socket()
print "Connecting to Dot..."

s.connect((HOST, PORT))
s.send("NICK %s\r\n" % NICK)
s.send("USER %s %s bla :%s\r\n" % (IDENT, HOST, REALNAME))
s.send("JOIN "+mainchannel+"\r\n")
s.send("PRIVMSG %s :Botler is Now Online and Running...\r\n" % mainchannel)
print "Server Running"

def log(message):
		s.send('PRIVMSG ' +mainchannel+' :'+message+'\r\n')

while 1:
		data = s.recv(2048)
		if data.find ('PING') !=-1:
				s.send('PONG' + data.split()[1]+'\r\n') 
		if data.find("hello") !=-1:
				log("Hello! May I invite you to bite my shiny virtual ass?")
							


