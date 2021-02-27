import discord
import requests
import json
import random
from discord.ext import commands
from lxml import html

client = commands.Bot(command_prefix="!")

@client.event
async def on_ready():
    ch = client.get_channel(814802007088431126)
    print('We have logged in as {0.user}'.format(client))
    await ch.send('bau')

@client.event
async def on_message(message):
  await client.process_commands(message)
  if str(message.author) == "dormeo#4381":
    await message.channel.send('sex')

@client.command()
async def hello(ctx, *arg):
  await ctx.send("Hello!")

@client.command()
async def inspire(ctx, *arg):
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " -" + json_data[0]['a']
  await ctx.send(quote)

@client.command()
async def rhyme(ctx, cuvant, n):
  page = requests.get(f'https://www.rimeaza.ro/cuvinte-care-rimeaza-cu-{cuvant}.html')
  tree = html.fromstring(page.content)
  cuvinte = tree.xpath('/html/body/div[2]/div[@class = "container_rime"]/*/text()')
  await ctx.send("\n".join(cuvinte[:min(len(cuvinte), int(n))]))

client.run('ODE0ODAxMzAxMDQ1MTE2OTU4.YDjI2A.DuYz5NkUZVt9UXPC-DF62snkxN4')