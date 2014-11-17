@commands("votekick")
def votekick(channel, nick, message):
  active_votes = {}
  class vote:
    def __init__(nick, message, channel):
      self.start_time = time.clock()
      self.first_voter = nick
      self.votes = 1
      self.judged = message
      self.kick_from = channel
    def voted(nick):
      #TODO: add logic to determine if current voter has voted
      # if they have send back a message telling them they can
      # only vote on a person once per vote
      if self.votes == 1:
        self.second_voter = nick
        self.votes++
      elif self.votes == 2:
        self.third_voter = nick
        self.votes++
      if self.votes==3:
        #kick them NOW and del the object
        say(self.kick_from, '{}&{}&{}~ {}{}'.format(self.first_voter, self.second_voter, self.third_voter, "Have kicked ", self.judged))
        del(self)
  if message != valid_user:# <- not real code just filler
    say(channel, '{}~ {}'.format(nick, "Sorry thats kickable target"))
  elif message in votes:
    #add a vote
    active_votes[message].voted()
  else:
    active_votes[message] = vote(nick, message, channel)
