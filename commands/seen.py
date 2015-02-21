#Flays seen function
@command("seen")

def seen(nick,user,channel,message):
	with db as conn:	
		with conn.cursor() as cursor:
			return cursor.execute("SELECT * from log where nick = 'flay' order by time desc limit 1;")

	

