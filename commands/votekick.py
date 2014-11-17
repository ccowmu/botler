@commands("votekick")
def votekick(nick, message):
  votes = {}
  class vote:
    def __init__(nick, message):
      self.start_time = time.clock()
      self.first_voter = nick
      self.votes = 1
      self.judged = message
    def voted(nick):
      #TODO: add logic to determine if current voter has voted
      # if they have send back a message telling them they can
      # only vote on a person once per vote
      if(self.votes==3):
      #kick them NOW and del the object
  if message != valid_user:# <- not real code just filler
    say(channel, '{}~ {}'.format("Sorry thats kickable target"))
  elif votes[message] == true:
    #add a vote
    votes[message].voted()
  else:
    votes[message] = vote(nick, message)
