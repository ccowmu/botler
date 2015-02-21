#Flays seen function
@command("seen")

def seen(nick,user,channel,message):
	with db as conn:	
		with conn.cursor() as cursor:
			cursor.execute("SELECT * from log where nick = '%s' order by time desc limit 1;" % message)
			msg = str(cursor.fetchone())
			msg = msg.split(',')
			print(msg)
			say(channel, ("%s was last seen on %s saying %s in %s" % (message.lstrip('!seen '), 'FIX TIME', msg[9], msg[10])))

# 3 (minutes ago) on 4, 1, 2 ,0 #
