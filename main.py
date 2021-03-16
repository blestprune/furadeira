import discord
import random
import os
import motos
import requests
from replit import db
from servidor import servidor

client = discord.Client()

filetypes = [".JPG", ".jpg", ".PNG", ".png"]

if "responding" not in db.keys():
    db["responding"] = True


def random_bike():
    bike = random.choice(motos.modelos)
    embed_msg = discord.Embed(title=bike['modelo'], description=bike['info'], color=0xff6600)
    # embed_msg.add_field(name="Descrição", value=bike['info'], inline=False)
    embed_msg.set_image(url=bike['img_url'])
    return embed_msg


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


def list_images():
    images = db["images"]
    lista = ""
    for i in range(len(images)):
        response = requests.get(images[i])
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError:
            lista += f"\n{i}: {images[i]}"
    lista = "```Imagens bugadas\n" + lista + "```"
    return lista


def nota_aleatoria(aluno, cadeira):
    nota = random.randint(0, 100) / 10
    resultado = f"{aluno}, sua nota em {cadeira} será {round(nota, 1)}"
    return resultado
    

@client.event
async def on_ready():
    print(f'Eu sou a {client.user} e estou online.')


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

    if message.content.startswith("!list"):
        if "images" in db.keys():
            images = list_images()
        await message.channel.send(images)

    if message.content.startswith("!harley"):
        msg = f'{message.author.mention}, sua Harley-Davidson é:'
        await message.channel.send(msg, embed=random_bike())

    if message.content.startswith("!fraude"):
        msg = random.choice(motos.fraudes)
        await message.channel.send(msg)

    if message.content.startswith("!fome"):
        msg = random.choice(motos.fome)
        await message.channel.send(msg)

    if message.content.startswith("K"):
        msg = random.choice(motos.risadas)
        await message.channel.send(msg)
    
    if message.content.startswith("!nota"):
        aluno = message.author.mention
        cadeira = message.content.split("!nota ")[1]
        await message.channel.send(nota_aleatoria(aluno, cadeira))

    if message.content.startswith("!add") and message.attachments:
        for filetype in filetypes:
            if filetype in message.attachments[0].url:
                update_images(message.attachments[0].url)
                await message.channel.send("Imagem adicionada.")

    if message.content.startswith("!del"):
        images = []
        if "images" in db.keys():
            index = int(message.content.split("!del", 1)[1])
            delete_image(index)
            images = db["images"]
        await message.channel.send("Imagem removida.")


servidor()
client.run(os.getenv('TOKEN'))
