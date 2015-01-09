@command("nts", admin_only=False, op_only=False)
def nts(nick, channel, message):
    send('TOPIC {} {}'.format(channel,message))
