import configparser

@command("admin", man="Usage: '!admin <add / remove> <nick>'. This is a protected command.", adminonly=True)
def admin(nick, user, channel, message):
    if message.startswith("add"):    
        name = message.split(" ",1)[1].strip("\n \r").replace(" ", "")
        config = configparser.ConfigParser()
        config.read("config.ini")
        config['botler']['admins'] = config['botler']['admins'] + "," + name
        with open('config.ini', 'w') as configfile:
            config.write(configfile)
        say(channel, "{}: Admin added.".format(nick))
        reload_admins()

    elif message.startswith("remove"):
        name = message.split(" ",1)[1].strip("\n \r").replace(" ", "")
        config = configparser.ConfigParser()
        config.read("config.ini")
        admins = list(config['botler']['admins'].split(','))
        if name in admins:
            admins.remove(name)
            config['botler']['admins'] = ",".join(admins)
            with open('config.ini', 'w') as configfile:
                config.write(configfile)
            say(channel, "{}: Admin removed.".format(nick))
            reload_admins()
        else:
            say(channel, "{}: {} is not an admin.".format(nick, name))
    
    else:
        say(channel, "{}: Usage is '!admin <add / remove> <nick>'.".format(nick))

@command("whitelist", man="Usage: '!whitelist <add / remove> <nick>'. This is a protected command.", whitelist=True)
def whitelist(nick, user, channel, message):
    if message.startswith("add"):
        name = message.split(" ",1)[1].strip("\n \r").replace(" ", "")
        config = configparser.ConfigParser()
        config.read("config.ini")
        config['botler']['whitelist'] = config['botler']['whitelist'] + "," + name
        with open('config.ini', 'w') as configfile:
            config.write(configfile)
        say(channel, "{}: Whitelisted user added.".format(nick))
        reload_admins()

    elif message.startswith("remove"):
        name = message.split(" ",1)[1].strip("\n \r").replace(" ", "")
        config = configparser.ConfigParser()
        config.read("config.ini")
        whitelist = list(config['botler']['whitelist'].split(','))
        if name in whitelist:
            whitelist.remove(name)
            config['botler']['whitelist'] = ",".join(whitelist)
            with open('config.ini', 'w') as configfile:
                config.write(configfile)
            say(channel, "{}: Whitelisted user removed.".format(nick))
            reload_admins()
        else:
            say(channel, "{}: {} is not on the whitelist.".format(nick, name))

    else:
        say(channel, "{}: Usage is 'whitelist <add / remove> <nick>'.".format(nick))
