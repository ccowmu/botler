@command("status", man="Usage: !status")
def status(nick, user, channel, message):
    import requests
    r = requests.get("http://unallocatedspace.org/status")
    say(channel, r.text)
