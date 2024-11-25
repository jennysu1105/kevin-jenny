import discord
import os
import datetime
from dateutil.relativedelta import relativedelta
from discord.ext import commands
from keep_alive import keep_alive
from access_json import *
import requests
import shutil
from help import *
from PIL import Image

intents = discord.Intents.all()

client = commands.Bot(command_prefix="kj!", intents=intents)


@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(
        name="get commands with kj!h"))
    print("Ready!")


# HELP
@client.command(name="h")
async def help(ctx, *specs):
    if len(specs) == 0:
        em = await general_help()
        await ctx.send(embed=em)
        return
    else:
        if specs[0].lower() == "c":
            em = await general_commands_help()
            await ctx.send(embed=em)
            return

    return


# Time command
@client.command(name="time")
async def time(ctx):
    together = datetime.datetime(2024, 10, 20, 4, 31, 0)
    now = datetime.datetime.now()
    dif = relativedelta(now, together)

    string = str(dif.years) + " years " + str(dif.months) + " months " + str(
        dif.days) + " days " + str(dif.hours) + " hours " + str(
            dif.minutes) + " minutes " + str(dif.seconds) + " seconds "
    em = discord.Embed(title="Kevin ♥ Jenny")
    em.add_field(name="We have been together for:", value=string)

    await ctx.send(embed=em)
    return


keep_alive()
client.run(os.environ['TOKEN'])
