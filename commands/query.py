#*Flays arbitrary sql query function
import datetime
@command("query", man= "Usage is !query SQL QUERY GOES HERE")
def query(nick,user,channel,message):
    try:
        os.mkdir("results/")
    except FileExistsError:
        pass
    with open('../www/SQL_queries/results: '+ str(user) + datetime.datetime.now().strftime("-%Y-%m-%d-%S"), mode ='a+', encoding='utf-8') as resultsfile:
        if db == None:
            return
        with db as conn:
            with conn.cursor() as cursor:
                    cursor.execute("{}".format(message))
                    result = cursor.fetchall()
                    if result == None:
                        say(channel, "ERROR FROM : {}".format(message))
                    else:
                        #resultsfile.write(str(message)
                        for row in result:
                            resultsfile.write(str(row)+ '\n')
                        say(channel, "Results written to file : ~/flay/SQL_queries/result.txt")
                        resultsfile.close()
                            #fix with gist shit from m00se
                        #Consider an aliasing function, to allow users to create aliased queries, sparing themselves from rewriting the entire query every time.
# Create some sugar to pull out 
