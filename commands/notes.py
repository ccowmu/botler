import os

@command("notes", man="Usage: '!notes', '!notes add <note>', '!notes remove <line>', '!notes clear'.")
def notes(nick, user, channel, message):
    filename = "files/notes/" + user + ".txt"

    if message.startswith("add"):
        try:
            f = open(filename, "a")
            f.write(message[4:] + "\n")
            f.close()
            say(channel, "{}: Note added.".format(nick))
        except IOError:
            say(channel, "{}: Unable to open file.".format(nick))
    elif message.startswith("remove"):
        try:
            place = int(message[7:])
            f = open(filename, "r")
            i = 0
            notes = ""
            for line in f:
                if i == place:
                    say(channel, "{}: Note removed.".format(nick)) 
                else:
                    notes += line
                i += 1
            f.close()
            f = open(filename, "w")
            f.write(notes)
            f.close()
        except ValueError:
            say(channel, "{}: Please specify a line.".format(nick))
        except IOError: 
            say(channel, "{}: Unable to open file.".format(nick))
    elif message.startswith("clear"):
        os.remove(filename)
        say(channel, "{}: Notes cleared.".format(nick))
    else:
        try:
            f = open(filename, "r")
            notes = ""
            for line in f:
                notes += line.rstrip('\n') + ' | '
            if notes == "":
                say(channel, "{}: No notes.".format(nick))
            else:
                notes = notes[:-3]
                say(channel, "{}: {}".format(nick, notes))
            f.close()
        except IOError:
            f = open(filename, "w")
            f.close()
            say(channel, "{}: No notes.".format(nick))
