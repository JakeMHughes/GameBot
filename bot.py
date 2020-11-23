import os
import discord

from warframe import warframe


#variables

TOKEN = os.getenv('DISCORD_TOKEN')
client = discord.Client()
warframeObj = warframe.Warframe()





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
        await message.channel.send(warframeObj.handleMessageWrapper(message.content,'{0.author.mention}'.format(message)))


client.run(TOKEN)
