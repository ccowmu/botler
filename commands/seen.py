#Flays seen function
@command("seen")

def seen(nick,user,channel,message):
	if db == None:
		return print("working") 
		query = "SELECT * from log where nick = 'flay' order by time desc limit 1;"
		print(channel, '{}:'.format(nick) + "Searching for 'stringy'")
		return print(db.cusor().execute(query))
		print('hi')

	

