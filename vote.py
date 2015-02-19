import datetime
@command("vote") 
def vote(nick, user, channel, message):
   say(channel, '{}: {}'.format(nick, message))
begin = datetime.time.min
end = datetime.time.max
if(begin != end): #Checks that time isn't closed yet

	input = message.lower().strip(" ") #Take input from user
	try:
        userSubmitted=open(filename,"r+")
        # The lambda expression filters out empty newlines/blank entries
        data=list(filter(lambda x:x,map(lambda x:x.strip("\n\r "),f.read().split("\n"))))
        f.close()
    except IOError:
        f=open(filename,"w")
        f.close()
        data=[]

	bool = FALSE

	if user in userSubmitted:
		bool = TRUE;
	elif user not in userSubmitted:
		userSubmitter.write(user)

	if(bool == FALSE):
   		if(input == "y"):
   			try:
        		yayFile=open(filename,"r+")
        		# The lambda expression filters out empty newlines/blank entries
        		data=list(filter(lambda x:x,map(lambda x:x.strip("\n\r "),f.read().split("\n"))))
        		f.close()
    		except IOError:
        		f=open(filename,"w")
        		f.close()
        		data=[] 
        	yayFile.write(nick, message)
   			say(channel, "Thank you for your submission.")
   		elif(input == "n"):
   			try:
        		nayFile=open(filename,"r+")
        		# The lambda expression filters out empty newlines/blank entries
        		data=list(filter(lambda x:x,map(lambda x:x.strip("\n\r "),f.read().split("\n"))))
        		f.close()
    		except IOError:
        		f=open(filename,"w")
        		f.close()
        		data=[]
        	nayFile.write(nick, message)	
   			say(channel, "Thank you for your submission.")
   		else: say(channel, "Error invalid character entered, try again.") # if not y or n, send error message 

	elif(bool == TRUE):
		say(channel, "You have already voted, we thank you for your submission.") #If nick has already voted, end /vote and output message

else: #need to change this still
	if(yay > nay): #checks for vote passing
		x = yay - nay
		say(channel, "Vote passes by " + x + " vote(s).")
	elif(yay == nay): #checks for vote being equal
		x = yay + nay
		say(channel, "Vote is even. " + x + " people voted.")
	else: #checks if vote was vetoed
		x = nay - yay
		say(channel, "Vote was vetoed by " + x + " vote(s).")
	say(channel, "No voting session is currently active") #If time is closed let user know
	sys.exit(0) #terminate program

