white_list=("themind","flay","stringy","sphinx")
AGENDA_FILE="/opt/agenda.html"
NEW_ITEM_FORMAT="\n<li>%s</li>"

@command("agenda")
def agenda(nick, channel, message):
    if nick.lower() not in white_list:
        say(channel, "%s: Sorry, you're not authorized to use this feature."%nick)
        return

    if message.startswith("add"):
        f=open(AGENDA_FILE,"a")
        item=message.split(" ",1)[1].strip("\n \r")
        f.write(NEW_ITEM_FORMAT%item)
        f.close()
        say(channel,"Added: %s"%item)

    elif message.startswith("insert"):
        # Using this insert method will push all items >= index to a larger index
        f=open(AGENDA_FILE,"r")
        # The lambda expression filters out empty newlines/blank entries
        data=list(filter(lambda x:x.strip("\n\r "),f.read().split("\n")))
        f.close()
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
        f=open(AGENDA_FILE,"r")
        # The lambda expression filters out empty newlines/blank entries
        data=list(filter(lambda x:x.strip("\n\r "),f.read().split("\n")))
        f.close()
        
        to_remove=[]
        for item in message.split(" ")[1:]:
            # In the event we get multiple spcaes or something weird:
            if not item.strip(" "): continue 
            try:
                to_remove.append(int(item))
            except ValueError:
                #Stop trying to parse numbers 'cause we found a weird char
                break 
       
        # Sort the list in decending order so that removing doesn't mess up the index of     
        #  other items to be removed.
        to_remove.sort(reverse=True)

        removed_items=[]
        for i in to_remove:
            # [4:-5] grabs everything within <li></li> tags
            removed_items.append(data.pop(i)[4:-5])

        f=open(AGENDA_FILE,"w")
        f.write("\n".join(data))
        f.close()
        say(channel,"Deleted: %s"%(" | ".join(removed_items)))

    elif message.startswith("list"):
        f=open(AGENDA_FILE,"r")
        say(channel,"Listing current agenda:")
        for i,line in enumerate(f.readlines()):
            say(channel,"%d. %s"%(i,line[4:-5]))
        f.close()
