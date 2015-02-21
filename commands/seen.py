#Flays seen function
@command("seen")

def seen(nick,user,channel,message):
	with db as conn:	
		with conn.cursor() as cursor:
			cursor.execute("SELECT * from log where nick = '%s' order by time desc limit 1;" % message)
			msg = str(cursor.fetchone())
			msg = msg.split(',')
			print(msg)
			say(channel, (message.lstrip('!seen '), "was last seen on", msg[1:3], "saying" ,msg[9], "in", msg[10]))

