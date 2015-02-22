#*Flays seen function
@command("seen")

def seen(nick,user,channel,message):
	if db == None: return
	with db as conn:	
		with conn.cursor() as cursor:
			cursor.execute("SELECT time, nick, message, channel from log where nick = %s order by time desc limit 1;", (message,))
			row = cursor.fetchone()
			if row == None:
				say(channel, "No record of {}".format(message))
			else:
				time = row[0]
				nick = row[1]
				msg = row[2]
				chan = row[3]
				say(channel, '{} was last seen on {} saying "{}" in {}'.format(nick, time, msg, chan))

# 3 (minutes ago) on 4, 1, 2 ,0 #
