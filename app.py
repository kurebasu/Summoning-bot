import discord
import sqlite3
import random
import os

global main_table; main_table = "summoning_table"

client = discord.Client()

#funct to print help message so users can find out how it works
async def instructions(message):
    await message.channel.send("This bot will call people for you with a message\n"
                         "Note you'll never have to write the <> symbols it's just to make the command clearer\n"
                         "=add @name <message>\n"
                         "Adds @name to the list or overwrite the entry with the following command:\n"
                         "=summon <@name>\n"
                         "Calls a user with their recorded message"
                         )

#funct to check if user is in database
def in_database(user):
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    query = 'SELECT * FROM ' + main_table + ' WHERE user = ?;'
    cursor.execute(query, (user, ))
    if len(cursor.fetchall()) > 0:
        connection.close()
        return True
    else:
        connection.close()
        return False

#funct run at start?
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


#Funct to react to messages
@client.event
async def on_message(message):
    if message.author == client.user:
        return

#----------------------------------------------------------------------------------
    if message.content.startswith("=help"):
        await instructions(message)


# ----------------------------------------------------------------------------------
    elif message.content.startswith("=add "):
        m_container = message.content.split(' ')
        user = m_container[1]
        summoning_ritual = ""
        i = 0
        for element in m_container:
            if i > 1:
                summoning_ritual += element + " "
            i+=1

        if summoning_ritual == "":
            summoning_ritual = user

        if in_database(user):
            #if user is in database, remove this entry before adding to database
            connection = sqlite3.connect('database.db')
            cursor = connection.cursor()
            cursor.execute("DELETE FROM " + main_table + " WHERE user = ?" , (user, ))
            connection.commit()
            cursor.close()

        #add to database
        await message.channel.send("user will be added or changed")
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        cursor.execute("INSERT INTO " + main_table + "(user, message) VALUES (?, ?)", (user, summoning_ritual))
        connection.commit()
        cursor.close()
        await message.delete()

# ----------------------------------------------------------------------------------
    elif message.content.startswith("=logout"):
        await client.close()

# ----------------------------------------------------------------------------------
    #  -summon shiet
    elif message.content.startswith('=summon '):
        # await message.channel.send("@" + message.name + " you are summoned!!! jij geile poepert!")
        # message.content

        randomlist = message.content.split(' ')
        user = ""
        i = 0
        for element in randomlist:
            if i > 0:
                user += element
            i += 1

        if in_database(user):
            pass
            connection = sqlite3.connect('database.db')
            cursor = connection.cursor()
            query = 'SELECT message FROM ' + main_table + ' WHERE user = ?;'
            cursor.execute(query, (user,))
            summonings = cursor.fetchone()[0]
            await message.channel.send(summonings)
            num_magic_circles = len(os.listdir("images/circles"))
            if num_magic_circles > 0:
                random_number = random.randint(1, num_magic_circles)
                await message.channel.send(file=discord.File("images/circles/magic circle " + str(random_number) + ".gif"))
            await message.delete()

        else:
            await message.channel.send("user not in database")


    else:
        list = os.listdir("./images/specific")
        for it in list:
            #[0:-4:1] trims off the ".gif" at the end
            if it[0:-4:1] in message.content.lower():
                image = "images/specific/" + it
                file = discord.File(image, filename = image)
                await message.channel.send(it[0:-4:1] +"!!!", file = file)
                return

        probably_the_best_platypus = "perry"
        if probably_the_best_platypus in message.content.lower():
            probably_the_best_platypus = "perry"
            num_perry = len(os.listdir("images/perry"))
            if num_perry > 0:
                random_number = random.randint(1, num_perry)
                image = "images/perry/perry" + str(random_number) + ".gif"
                file = discord.File(image, filename = image)
                await message.channel.send("You summoned a wild Perry the Platypus!", file = file)



connection = sqlite3.connect('database.db')
cursor = connection.cursor()
command = "SELECT name FROM sqlite_master WHERE type='table' AND name='" + main_table + "';"
cursor.execute(command)




if len(cursor.fetchall()) > 0:
    print("database ok")
else:
    print("creating database")
    command = "CREATE TABLE " + main_table + "(user, message)"
    print("database ok")
    cursor.execute(command)

connection.close()

global num_magic_circles
num_magic_circles = len(os.listdir("images/circles"))
print (str(num_magic_circles) + " magic circles found in images/circles")
global num_perry
num_perry = len(os.listdir("images/perry"))
print (str(num_perry) + " perry gifs found in images/perry")


client.run("YOUR TOKEN HERE")
