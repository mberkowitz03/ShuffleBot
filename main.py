from keep_alive import keep_alive
import discord
import os
import re
import random

client = discord.Client()
symbol = "-"
commandsList = "bruh... the only command is shuffle"
startList = ["Prepare to be **annoyed!**", "Hey, did you guys miss me?", "Boy, am I funny! Right guys?", "Reality can be whatever ***I***  want."]
endList = ["Sorry, mom says it's dinnertime.", "Until we meet again.", "Fine... I'll stop.", "I think it's time to piss off, buckos."]
server_annoyances = {}

def randomPhrase(phrases):
  return random.choice(phrases)

@client.event # waits until bot is loaded and prints message
async def on_ready():
  await client.wait_until_ready()
  await client.change_presence(activity=discord.Game(name=symbol+"help"))
  print("We have logged in as {0.user}".format(client))
  for g in client.guilds:
    server_annoyances[g.name] = False


@client.event
async def on_message(message):
  await client.wait_until_ready()
  if message.author == client.user: # don't react to own messages
    return

  if message.content.startswith(symbol + "help"): # display all commands
    await message.channel.send(commandsList)
  
  elif message.content.startswith(symbol + "shuffle"):
    global server_annoyances
    if server_annoyances[message.guild.name] == True:
      server_annoyances[message.guild.name] = False
      await message.channel.send(randomPhrase(endList))
    else:
      server_annoyances[message.guild.name] = True
      await message.channel.send(randomPhrase(startList))
  
  elif server_annoyances[message.guild.name] == True:
    msg = ""
    sub = ""
    wordList = message.content.split()
    for word in wordList:
      index = len(word) - 1
      if re.search("\.|,|!|\?", word) != None:
        done = False
        while done != True:
          checkWord = word[1 : index]
          if re.search("\.|,|!|\?", checkWord) != None:
            index = index - 1
          else:
            done = True
        sub = word[1 : index]
      else:
        sub = word[1 : len(word) - 1]
        
      subList = [char for char in sub]
      random.shuffle(subList)
      sub = ''.join(subList)
      #potential if statement here if the following line fails when index == length
      if len(word) == 1:
        msg += word + ' '
      else:
        msg += word[0] + sub + word[index:len(word)] + ' '
    name = "**" + message.author.name + "**"
    await message.delete()
    await message.channel.send(name + ' - ' + msg)

keep_alive()
client.run(os.getenv('TOKEN'))