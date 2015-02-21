#Flays seen function
@command("seen")

def seen(nick,user,channel,message):
	with db as conn:	
		with conn.cursor() as cursor:
			print(cursor.execute("SELECT * from log where nick = 'stringy' order by time desc limit 1;"))
	print("Done")

	

