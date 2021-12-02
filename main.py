import discord
import os
import requests
import json
import random
import pdb
import logging
from replit import db

 

client = discord.Client()

up_trigger_words = ["whats up", "wats up", "was up", "whats up?", "wats up?","waz up", "wuz up", "whaz up","what is up", "what is up?", "wat is up"]
up_response = "It's a Pixar movie!"

sad_words = ["sad", "depressed", "unhappy", "angry", "miserable"]

what_response = "wha what?"
lame_response = ['ur mom', 'lame', 'wooow', 'k', ':bruh:']
starter_encouragements = [
  "Cheer up!",
  "Hang in there.",
  "You are a great person / bot!"
]

if "responding" not in db.keys():
  db["responding"] = True

def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]["q"] + " -" + json_data[0]["a"]
  return(quote)

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


@client.event
async def on_ready():
  print("We have logged in as {0.user}".format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return

  msg = message.content
  msg = msg.lower()

  if msg.startswith("$inspire"):
    quote = get_quote()
    await message.channel.send(quote)

  if db["responding"]:
    options = starter_encouragements
    # random lame_response
    some_number = random.randint(1,4)
    if some_number == 1: 
      await message.channel.send(random.choice(lame_response))
  
    if "encouragements" in db.keys():
      options = options + db["encouragements"].value

    if any(word in msg for word in sad_words):
      await message.channel.send(random.choice(options))
    
    # this is up pasta  
    if any(word in msg for word in up_trigger_words):
      await message.channel.send(up_response)
    if msg == 'what':
      await message.channel.send(what_response)
    if msg == 'bruh':
      await message.channel.send('bruh')

  if msg.startswith("$responding"):
    value = msg.split("$responding ",1)[1]

    if value.lower() == "true":
      db["responding"] = True
      await message.channel.send("Responding is on.")
    else:
      db["responding"] = False
      await message.channel.send("Responding is off.")

  if msg.startswith("$new"):
    encouraging_message = msg.split("$new ",1)[1]
    update_encouragements(encouraging_message)
    await message.channel.send("New encouraging message added.")

  if msg.startswith("$del"):
    encouragements = []
    if "encouragements" in db.keys():
      
      index = int(msg.split("$del",1)[1].strip())
      delete_encouragment(index)
      encouragements = db["encouragements"]
    await message.channel.send(encouragements)

  if msg.startswith("$list"):
    encouragements = []
    if "encouragements" in db.keys():
      encouragements = db["encouragements"]
      print(encouragements)
    await message.channel.send(encouragements)

my_secret = os.environ['TOKEN']
client.run(os.getenv("TOKEN"))

