import discord
import asyncio
import os
import requests
import json
import random
import pdb
from replit import db
from discord.ext import commands
import builtins

from dotenv import load_dotenv

load_dotenv() 

intents = discord.Intents.default()
intents.members = True 
intents = discord.Intents().all()



#client = discord.Client()
bot = commands.Bot(command_prefix='.', intents=intents)
builtins.bot = bot

import kick

up_trigger_words = [
    "whats up", "wats up", "was up", "whats up?", "wats up?", "waz up",
    "wuz up", "whaz up", "what is up", "what is up?", "wat is up"
]
up_response = "It's a Pixar movie!"

sad_words = ["sad", "depressed", "unhappy", "angry", "miserable"]

what_response = "wha what?"
lame_response = ['ur mom', 'lame', 'wooow', 'k', ':bruh:']
starter_encouragements = [
    "Cheer up!", "Hang in there.", "You are a great person / bot!"
]

# if "responding" not in db.keys():
#     db["responding"] = True


def get_quote():
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = json_data[0]["q"] + " -" + json_data[0]["a"]
    return (quote)


# this code is broken as hell wtf
def update_encouragements(encouraging_message):
    if "encouragements" in db.keys():
        encouragements = db["encouragements"]
        encouragements.append(encouraging_message)
        db["encouragements"] = encouragements
    else:
        db["encouragements"] = [encouraging_message]


def delete_encouragment(index):
    encouragements = db["encouragements"]
    if len(encouragements) > index:
        del encouragements[index]
    db["encouragements"] = encouragements


@bot.event
async def on_ready():
    print("We have logged in as {0.user}".format(bot))


@bot.event
async def on_message(message):
    await bot.process_commands(message)
    if message.author == bot.user:
        return

    msg = message.content
    msg = msg.lower()

    if msg.startswith("$inspire"):
        quote = get_quote()
        await message.channel.send(quote)

    if db["responding"]:
        options = starter_encouragements
        # random lame_response
        some_number = random.randint(1, 4)
        if some_number == 1:
            await message.channel.send(random.choice(lame_response))

        if "encouragements" in db.keys():
            options = options + db["encouragements"].value

        # if any(word in msg for word in sad_words):
        #   await message.channel.send(random.choice(options))

        # this is up pasta
        if any(word in msg for word in up_trigger_words):
            await message.channel.send(up_response)
        if msg == 'what':
            await message.channel.send(what_response)
        if msg == 'bruh':
            await message.channel.send('bruh')

    if msg.startswith("$responding"):
        value = msg.split("$responding ", 1)[1]

        if value.lower() == "true":
            db["responding"] = True
            await message.channel.send("Responding is on.")
        else:
            db["responding"] = False
            await message.channel.send("Responding is off.")

    if msg.startswith("$new"):
        encouraging_message = msg.split("$new ", 1)[1]
        update_encouragements(encouraging_message)
        await message.channel.send("New encouraging message added.")

    if msg.startswith("$del"):
        encouragements = []
        if "encouragements" in db.keys():

            index = int(msg.split("$del", 1)[1].strip())
            delete_encouragment(index)
            encouragements = db["encouragements"]
        await message.channel.send(encouragements)

    if msg.startswith("$list"):
        encouragements = []
        if "encouragements" in db.keys():
            encouragements = db["encouragements"]
            print(encouragements)
        await message.channel.send(encouragements)


@bot.command()
async def test(ctx, arg):
    await ctx.send(arg)

@bot.command(aliases=['power'])
async def _power(context):
    await playSound(context, "./soundClips/power.mp3")

@bot.command(aliases=['bruh'])
async def _bruh(context):
    await playSound(context, "./soundClips/bruh.mp3")


@bot.command(aliases=['omg'])
async def _omg(context):
    await playSound(context, "./soundClips/omg.mp3")


# plays a specific sound in voice channel
async def playSound(context, soundFile):
    # grab the user who sent the command
    user = context.message.author
    channel = None
    # only play music if user is in a voice channel
    if user.voice != None:
        voice_channel = user.voice.channel

        # grab user's voice channel
        channel = voice_channel.name
        
        await context.send('User is in channel: ' + channel)
        # create StreamPlayer
        vc = await voice_channel.connect()
        vc.play(discord.FFmpegPCMAudio(soundFile),
                after=lambda e: print('done', e))
        while vc.is_playing():
            await asyncio.sleep(1)
        # disconnect after the player has finished
        vc.stop()
        await vc.disconnect()
    else:
        await context.send('User is not in a channel.')


my_secret = os.environ['dgsToken']
#bot.run(os.getenv("TOKEN"))
bot.run(my_secret)



#client.run(os.getenv("TOKEN"))
