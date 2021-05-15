import random
import os
import listas
import requests
import database as db
import discord
from discord import Intents
from discord.ext import commands
from discord_slash import SlashCommand
from discord_slash.utils.manage_commands import create_option

FILETYPES = [".JPG", ".jpg", ".PNG", ".png"]

intents = Intents.all()
bot = commands.Bot(command_prefix="!",
                   description='Furadeira',
                   intents=intents)

slash = SlashCommand(bot, sync_commands=True)


# ----- Utils -----------------------------------------------------------------

def random_moto():
    moto = random.choice(listas.motos)
    embed_msg = discord.Embed(title=moto['modelo'],
                              description=moto['info'],
                              color=0xff6600)
    embed_msg.set_image(url=moto['img_url'])
    return embed_msg


def print_urls():
    frases = db.todas_frases()
    for imagem in frases:
        print(f"{imagem.id} - {imagem.url}")


def deletar_bugadas():
    frases = db.todas_frases()
    msg = ""
    for imagem in frases:
        response = requests.get(imagem.url)
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError:
            msg += f"\n{imagem.id}: {imagem.url}"
            db.deletar_frase(imagem)
    if msg != "":
        msg = "```Imagens bugadas removidas:\n" + msg + "```"
    else:
        msg = "Não encontrei nenhuma imagem bugada!"
    return msg


def nota_aleatoria(aluno, cadeira):
    valor = random.randint(0, 100) / 10
    resultado = f"{aluno}, sua nota em {cadeira} será {round(valor, 1)}"
    return resultado


# ----- Bot Events ------------------------------------------------------------

@bot.event
async def on_ready():
    print(f'{bot.user} online.')


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.lower().startswith("kkk"):
        await message.channel.send(random.choice(listas.risadas))

    if message.content.lower().startswith("bom dia"):
        await message.channel.send("grande dia")

    await bot.process_commands(message)


# ----- Bot Slash Commands ----------------------------------------------------

@slash.slash(name="frase",
             description="Escolho uma frase icônica aleatória bem legal")
async def frase(ctx):
    img = db.frase_aleatoria()
    await ctx.send(content=img.url)


@slash.slash(name="harley",
             description="Escolho a Harley-Davidson que você terá daqui a 10 anos")
async def harley(ctx):
    msg = f'{ctx.author.mention}, sua Harley-Davidson é:'
    await ctx.send(content=msg, embed=random_moto())


@slash.slash(name="fraude",
             description="Escolho uma fraude aleatória")
async def fraude(ctx):
    await ctx.send(content=random.choice(listas.fraudes))


@slash.slash(name="fome",
             description="Hora do lanche")
async def fome(ctx):
    await ctx.send(content=random.choice(listas.fome))


@slash.slash(name="nota",
             description="Diga uma cadeira e eu digo qual será sua nota",
             options=[
                 create_option(
                     name="cadeira",
                     description="Qual a cadeira?",
                     option_type=3,
                     required=True
                 )
             ])
async def nota(ctx, cadeira: str):
    aluno = ctx.author.mention
    await ctx.send(content=nota_aleatoria(aluno, cadeira))


@slash.slash(name="zdeletar",
             description="Deletar uma imagem com base no index. Cuidado!",
             options=[
                 create_option(
                     name="index",
                     description="Id da imagem",
                     option_type=3,
                     required=True
                 )
             ])
async def zdeletar(ctx, index: int):
    db.deletar_frase(index)
    await ctx.send(f"Imagem #{index} deletada.")


# ----- Bot Prefix Commands ---------------------------------------------------

@bot.command(brief='Pinga')
async def ping(ctx):
    """Ping the server to verify that it\'s listening for commands"""
    await ctx.send('Pong!')


@bot.command(brief='Adiciona imagem')
async def add(ctx):
    for filetype in FILETYPES:
        if filetype in ctx.message.attachments[0].url:
            db.inserir_frase(ctx.message.attachments[0].url)
            await ctx.send(f"Imagem adicionada.")


@bot.command(brief='Deleta imagens bugadas')
async def bugadas(ctx):
    await ctx.send(deletar_bugadas())


@bot.command(brief='Lista imagens')
async def listar(ctx):
    print_urls()
    await ctx.send("Cheque o app log")

# ----- Run -------------------------------------------------------------------

if __name__ == '__main__':
    bot.run(os.getenv('TOKEN'))
