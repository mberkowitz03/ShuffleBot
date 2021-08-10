from keep_alive import keep_alive
import discord
import os
import re
import random

client = discord.Client()
symbol = "-"
commandsList = "bruh... i shuffle and mock what more do you want"
startList = ["Prepare to be **annoyed!**", "Hey, did you guys miss me?", "Boy, am I funny! Right guys?", "Reality can be whatever ***I***  want."]
endList = ["Sorry, mom says it's dinnertime.", "Until we meet again.", "Fine... I'll stop.", "I think it's time to piss off, buckos."]
server_shuffles = {}
server_mocks = {}

def randomPhrase(phrases):
  return random.choice(phrases)

@client.event # waits until bot is loaded and prints message
async def on_ready():
  await client.wait_until_ready()
  await client.change_presence(activity=discord.Game(name=symbol+"help"))
  print("We have logged in as {0.user}".format(client))
  for g in client.guilds:
    server_shuffles[g.name] = False
    server_mocks[g.name] = False


@client.event
async def on_message(message):
  await client.wait_until_ready()
  if message.author == client.user: # don't react to own messages
    return 

  if message.content.startswith(symbol + "help"): # display all commands
    await message.channel.send(commandsList)
  
  elif message.content.startswith(symbol + "shuffle"):
    if server_shuffles[message.guild.name]:
      server_shuffles[message.guild.name] = False
      await message.channel.send(randomPhrase(endList))
    else:
      server_shuffles[message.guild.name] = True
      await message.channel.send(randomPhrase(startList))

  elif message.content.startswith(symbol + "mock"):
    if server_mocks[message.guild.name]:
      server_mocks[message.guild.name] = False
      await message.channel.send(randomPhrase(endList))
    else:
      server_mocks[message.guild.name] = True
      await message.channel.send(randomPhrase(startList))
    
  elif message.content.startswith(symbol + "adios"):
    server_mocks[message.guild.name] = False
    server_shuffles[message.guild.name] = False
    await message.channel.send(randomPhrase(endList))

  else:   
    msg = ""
    if server_mocks[message.guild.name] == True:
      for ch in message.content:
        if random.randint(0,1) == 0:
          newLetter = ch.swapcase()
        else:
          newLetter = ch
        msg += newLetter  

    if server_shuffles[message.guild.name] == True:
      if msg == "":
        wordList = message.content.split()
      else:
        wordList = msg.split()
        msg = ""

      sub = ""
      for word in wordList:
        if len(word) == 1:
          msg += word
        else:
          index = len(word)
          if re.search("\.|,|!|\?", word) != None:
            done = False
            while not done:
              checkWord = word[1 : index]
              if re.search("\.|,|!|\?", checkWord) != None:
                index -= 1
              else:
                done = True

          sub = word[1 : index - 1]
            
          subCharList = [char for char in sub]
          random.shuffle(subCharList)
          sub = ''.join(subCharList)
          
          msg += word[0] + sub + word[index - 1:len(word)]
        msg += ' '
      await message.delete()

    if server_shuffles[message.guild.name]:
      name = "**" + message.author.name + "**"
      await message.channel.send(name + ' - ' + msg)
    elif server_mocks[message.guild.name]:
      await message.channel.send('\"' + msg + '\"')

keep_alive()
client.run(os.getenv('TOKEN'))