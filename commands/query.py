#*Flays sql query function
@command("query")
def query(nick,user,channel,message):
    try:
        os.mkdir("results/")
    except FileExistsError:
        pass
    with open('results/results.txt', mode = 'w') as resultsfile:
        if db == None:
            return
        with db as conn:
            with conn.cursor() as cursor:
                    cursor.execute("{}".format(message))
                    result = cursor.fetchall()
                    if result == None:
                        say(channel, "ERROR FROM : {}".format(message))
                    else:
                        #resultsfile.write(str(result))
                        say(channel, "Results written to file")
                        #fix with gist shit from m00se
