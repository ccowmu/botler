import os.path
@command("ptopic", admin_only=False, op_only=True)
def ptopic(nick, channel, message):
    # print('"{}"'.format(message)) 
    topic = message.rstrip('\n')
    oldtopic = ''
    if os.path.exists('topicfile'):
        topicfile = open('topicfile', 'r+')
    #for line in topicfile: 
    send('TOPIC {} :{}'.format(channel,topic))
# vim: ts=4:sw=4:et

