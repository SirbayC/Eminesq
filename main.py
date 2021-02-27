import discord
import requests
import json
import random
from replit import db
from keep_alive import keep_alive
from lxml import html
from discord.ext import commands

client = discord.Client()

sad_words = ["sad", "depressed", "unhappy", "angry", "miserable"]

starter_encouragements = [
  "Cheer up!",
  "Hang in there.",
  "You are a great person / bot!",
  "Ia sa auzi o gluma de Chitisor, mori de ras!"
]

if "responding" not in db.keys():
  db["responding"] = True

def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " -" + json_data[0]['a']
  return(quote)

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

client = commands.Bot(command_prefix="$")

@client.event
async def on_ready():
  ch = client.get_channel(814802007088431126)
  print('We have logged in as {0.user}'.format(client))
  await ch.send('bau')

@client.event
async def on_message(message):
  if message.author == client.user:
    return

  if str(message.author) == "dormeo#4381":
    await message.channel.send('sex')

  msg = message.content

  if message.content.lower().startswith('$hello'):
        await message.channel.send('Hello!')

  if message.content.lower().startswith('$inspire'):
    quote = get_quote()
    await message.channel.send(quote)

  if db["responding"]:
    options = starter_encouragements
    if "encouragements" in db.keys():
      options = options + db["encouragements"]

    if any(word in message.content for word in sad_words):
      await message.channel.send(random.choice(options))

  if msg.startswith("$new"):
    encouraging_message = msg.split("$new ",1)[1]
    update_encouragements(encouraging_message)
    await message.channel.send("New encouraging message added.")

  if msg.startswith("$del"):
    encouragements = []
    if "encouragements" in db.keys():
      index = int(msg.split("$del",1)[1])
      delete_encouragment(index)
      encouragements = db["encouragements"]
    await message.channel.send(encouragements)
  
  if msg.startswith("$list"):
    encouragements = []
    if "encouragements" in db.keys():
      encouragements = db["encouragements"]
    await message.channel.send(encouragements)

  if msg.startswith("$responding"):
    value = msg.split("$responding ",1)[1]

    if value.lower() == "true":
      db["responding"] = True
      await message.channel.send("Responding is on.")
    else:
      db["responding"] = False
      await message.channel.send("Responding is off.")

  if msg.startswith("$rhyme"):
    cuvant, n = msg.split("$rhyme ",1)[1].split()
    page = requests.get(f'https://www.rimeaza.ro/cuvinte-care-rimeaza-cu-{cuvant}.html')
    tree = html.fromstring(page.content)
    cuvinte = tree.xpath('/html/body/div[2]/div[@class = "container_rime"]/*/text()')
    await message.channel.send("\n".join(cuvinte[:min(len(cuvinte),int(n))]))

client.run('ODE0ODAxMzAxMDQ1MTE2OTU4.YDjI2A.DuYz5NkUZVt9UXPC-DF62snkxN4')