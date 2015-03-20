import threading
import time

@command("vote", man="Usage: '!echo <message>'")
def vote(nick, user, channel, message):
	class VoteStart(threading.Thread):
		def run(self):
			try:
				file = open("voteinfo.txt", "r")
				if "voteStatusTrue" in file.read():
					say(channel, "Vote already in progress.")
					pass
				else:
					temp = input[2]
					file = open("voteinfo.txt", "w")
					file.write("voteStatusTrue\n")
					i = 1
					while i < int(len(input))-1:
						toAdd = input[i]
						file.write(toAdd + "___" + "0\n")
						i = i+1
					file.write(input[i]+ "___" + "0")
					file.close()
					time.sleep(15)
					VoteEnd().start()
			except:
				say(channel, "Invalid input.")
	class VoteChoose(threading.Thread):
		def run(self):
			try:
				userSelection = input[1]
				file = open("voteinfo.txt", "r+")
				if "voteStatusTrue" in file.read():
					file.seek(0)
					voteData = file.read()
					voteData = voteData.split()
					i = 0
					options = []
					while i < len(voteData[1:]):
						options.append(voteData[1:][i])
						i = i+1
					i = 0
					while i < len(voteData[1:]):
						options[i] = options[i].split("___")
						i = i+1
					i = 0
					while i < len(voteData[1:]):
						if userSelection.lower() == options[i][0].lower():
							options[i][1] = int(options[i][1]) + 1
							options[i][1] = str(options[i][1])
							userList = open("voteuserlist.txt", "a")
							userList.write("\n" + user)
							userList.close()
							say(channel, nick + ": Your vote has been submitted.")
							break
						i = i+1
					i = 0
					while i < len(voteData[1:]):
						options[i] = "___".join(options[i])
						i = i+1
					options = "\n".join(options)
					file = open("voteinfo.txt", "w")
					file.write("voteStatusTrue\n" + options)
				else:
					say(channel, "There is not a vote in progress.")
					pass
				file.close()
			except:
				say(channel, "Invalid input.")
	class VoteEnd(threading.Thread):
		def run(self):
			file = open("voteinfo.txt", "r+")
			results = file.read()
			results = results.split()
			results = ", ".join(results[1:])
			say(channel, "Results: {}.".format(results.replace("___", " = ")))
			results = results.split(", ")
			i = 0
			while i < len(results):
				results[i] = results[i].split("___")
				i = i+1
			i = 0
			largest = []
			largest.append([0, 0])
			while i < len(results):
				if int(results[i][1]) > int(largest[0][1]):
					del largest[:]
					largest.append(results[i])
				elif int(results[i][1]) == int(largest[0][1]):
					largest.append(results[i])
				i = i + 1
			i = 0
			while i < len(largest):
				largest[i] = " = ".join(largest[i])
				i = i+1
			if len(largest) > 1:
				say(channel, "Winners: {}.".format(", ".join(largest)))
			else:
				say(channel, "Winner: {}.".format("".join(largest)))
			file = open("voteinfo.txt", "w")
			file.write("voteStatusFalse")
			file.close()
			userList = open("voteuserlist.txt", "w")
			userList.close()

	x = VoteStart()
	y = VoteChoose()
	input = message.split()
	if(input[0] == "start"):
		x.start()
	elif(input[0] == "choose"):
		userList = open("voteuserlist.txt", "r+")
		userListData = userList.read().split("\n")
		if user in userListData:
			say(channel, nick + ": You have already submitted a vote.")
		else:
			y.start()
		userList.close()