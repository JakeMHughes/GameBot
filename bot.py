import os
import discord
import Levenshtein
import urllib.request
import json
import datetime

import warframe


#variables

TOKEN = os.getenv('DISCORD_TOKEN')
client = discord.Client()
overframe = warframe.Overframe()
warframeApi = 'http://content.warframe.com/dynamic/worldState.php'

#functions
def getPriceURL(item):
    line = 'https://api.warframe.market/v1/items/' + item.replace(' ', '_').lower() + '/statistics'
    return line

def getJson(url):
    request = urllib.request.Request(url)
    response = urllib.request.urlopen(request)
    jsonData = json.loads(response.read().decode('utf-8'))
    return jsonData



@client.event
async def on_ready():
        print('Logged in as')
        print(client.user.name)
        print(client.user.id)
        print('------')

@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    
    #bot will post the commands and descriptions
    if message.content.startswith('!help'):
        msg = '{0.author.mention} These are the commands:\n'
        msg += '!warframe !help : Gets all Warframe commands.\n'
        newmsg = msg.format(message)
        await message.channel.send(newmsg)
    elif message.content.startswith('!warframe'):
        splitMessage = message.content.split(' ',2)
        command = splitMessage[0]
        subCommand = splitMessage[1]
        length = len(splitMessage)

        #Get help information for warframe
        if subCommand.startswith('!help'):
            msg = '{0.author.mention} These are the Warframe commands:\n'
            msg += '!warframe !help : Gets all warframe commands.\n'
            msg += '!warframe !price (item): Pulls the median price from the market.)\n'
            msg += '!warframe !wiki (item): Gets the wiki page for a requested object.\n'
            msg += '!warframe !build (item): Gets the overframe.gg build page for a requested object.\n'
            msg += '!warframe !rank (item): Gets the overframe.gg rank info for a requested object. Use warframes,primary weapons, secondary weapons, or melee weapons for the entire group\n'
            newmsg = msg.format(message)
            await message.channel.send(newmsg)

        #gets median price of items from warframe market
        elif subCommand.startswith('!price'):
            print("Sub Command: {}\nLength: {}".format(subCommand, length))
            if length >= 3:
                request = splitMessage[2]
                jsonData = getJson(getPriceURL(request))
                newmsg = ''
                median = 0
                for item in jsonData['payload']['statistics_closed']['90days']:
                    median = item['median']
                newmsg = '{} has a median price of {}.'.format(request, median)
                await message.channel.send(newmsg)
        
        #gets wiki page for item
        elif subCommand.startswith('!wiki'):
            if length >= 3:
                base = 'https://warframe.fandom.com/wiki/'
                filepath = 'warframe_items.txt'
                request = splitMessage[2]

                #uses levenshtein distance to determine the closes item
                #still needs work
                minDist = 1000
                minPhrase = 'Error'
                with open(filepath) as fp:
                    line = fp.readline()
                    while line:
                        currDistance = Levenshtein.distance(request, line)
                        if currDistance < minDist :
                            minDist = currDistance
                            minPhrase = line
                        line = fp.readline()
                minPhrase = minPhrase.replace(' ', '_')
                newmsg = "{}".format(base+minPhrase)
                await message.channel.send(newmsg)

        elif subCommand.startswith('!rank'):
                msg = overframe.prettyPrint(splitMessage[2].strip())
                await message.channel.send(msg)
        elif subCommand.startswith('!build'):
                msg = overframe.getLink(splitMessage[2].strip())
                await message.channel.send(msg)
                   

client.run(TOKEN)
