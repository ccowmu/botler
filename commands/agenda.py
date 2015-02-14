from time import sleep

white_list=("themind","flay","stringy","sphinx")
AGENDA_FILE="/opt/agenda.html"
NEW_ITEM_FORMAT="\n<li>%s</li>"

def ReadAgendaData(filename):
    try:
        f=open(filename,"r")
        # The lambda expression filters out empty newlines/blank entries
        data=list(filter(lambda x:x,map(lambda x:x.strip("\n\r "),f.read().split("\n"))))
        f.close()
    except IOError:
        f=open(filename,"w")
        f.close()
        data=[]

    return data

@command("agenda")
def agenda(nick, user, channel, message):
    if nick.lower() not in white_list:
        say(channel, "%s: Sorry, you're not authorized to use this feature."%nick)
        return

    if message.startswith("add"):
        try:
            f=open(AGENDA_FILE,"a")
            item=message.split(" ",1)[1].strip("\n \r")
            f.write(NEW_ITEM_FORMAT%item)
            f.close()
            say(channel,"Added: %s"%item)
        except IOError: # Probably permission denied on the file
            say(channel,"Error: couldn't add to agenda. Botler running with correct permissions?")

    elif message.startswith("in"):
        # Using this insert method will push all items >= index to a larger index
        data=ReadAgendaData(AGENDA_FILE)
        message=message.split(" ",2)
        try:
            item=message[2].strip("\n \r")
            index=int(message[1])
            data.insert(index,NEW_ITEM_FORMAT%item)
            f=open(AGENDA_FILE,"w")
            f.write("\n".join(data))
            f.close()
            say(channel,"Inserted @ %d: %s"%(index,item))

        except ValueError:
            pass
        except IndexError:
            pass

    elif message.startswith("rm"):
        data=ReadAgendaData(AGENDA_FILE)
        
        to_remove=[]
        for item in message.split(" ")[1:]:
            # In the event we get multiple spcaes or something weird:
            if not item.strip(" "): continue 
            try:
                to_remove.append(int(item))
            except ValueError:
                # Just ignore the item and keep looking for more indicies
                pass
       
        # Sort the list in decending order so that removing doesn't mess up the index of     
        #  other items to be removed.
        to_remove.sort(reverse=True)

        removed_items=[]
        for i in to_remove:
            # [4:-5] grabs everything within <li></li> tags
            removed_items.append(data.pop(i)[4:-5])
        try:
            f=open(AGENDA_FILE,"w")
            f.write("\n".join(data))
            f.close()
            say(channel,"Deleted: %s"%(" | ".join(removed_items)))
        except IOError:
            say(channel,"Error: could not delete items. Botler running with correct permissions?")

    elif message.startswith("list"):
        data=ReadAgendaData(AGENDA_FILE)
        say(channel,"Listing current agenda:")
        for i,line in enumerate(data):
            say(channel,"%d. %s"%(i,line[4:-5]))
            sleep(0.2) # Sleep between each line (irc rate limiting?)
        say(channel,"Done.")

    elif message.startswith("help"):
        say(channel,"Avaliable commands: add (append a new item to the agenda) | in (insert an item at a specific index. e.g.: !agenda in 2 Vote on SomeTopic.) | rm (remove agenda items based on a list of indicies.) | list (list current agenda items) Note: all indicies are 0 based.")

    else:
        say(channel,"Error: Incorrect usage. Try !agenda help")
