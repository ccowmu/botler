#Flays seen function
@command("seen")

def seen(nick,user,channel,message):
	print(db)	
	query = "SELECT * from log where nick = 'flay' order by time desc limit 1;"
	say(channel, '{}:'.format(nick) + "Searching for %s"  % nick)
	db.cusor().execute(query)
	

