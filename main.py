import discord
import random
import os
from replit import db

client = discord.Client()

filetypes = [".JPG", ".jpg", ".PNG", ".png"]

if "responding" not in db.keys():
  db["responding"] = True

def update_images(img_url):
  if "images" in db.keys():
    images = db["images"]
    images.append(img_url)
    db["images"] = images
  else:
    db["images"] = [img_url]

def delete_image(index):
  images = db["images"]
  if len(images) > index:
    del images[index]
  db["images"] = images

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if db["responding"]:
        options = []
        if "images" in db.keys():
            options = options + db["images"]
        if message.content.startswith('!frase'):
            await message.channel.send(random.choice(options))
    
    if message.content.startswith("$del"):
        images = []
        if "images" in db.keys():
            index = int(message.content.split("$del", 1)[1])
            delete_image(index)
            images = db["images"]
        await message.channel.send(images)
    
    if message.content.startswith("$list"):
        images = []
        if "images" in db.keys():
          images = db["images"]
        await message.channel.send(images)

    if message.attachments:
        for filetype in filetypes:
            if filetype in message.attachments[0].url:
                update_images(message.attachments[0].url)
                await message.channel.send("Imagem adicionada")

client.run(os.getenv('TOKEN'))
