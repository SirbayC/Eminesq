import discord

from discord.ext import commands

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
