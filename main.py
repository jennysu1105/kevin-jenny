import discord
import os
import datetime
from dateutil.relativedelta import relativedelta
from discord.ext import commands, tasks
from typing import Optional
from keep_alive import keep_alive
from access_json import *
import shutil
from help import *
from PIL import Image

intents = discord.Intents.all()

client = commands.Bot(command_prefix="kj!", intents=intents)

client.remove_command("help")
# HELP
async def get_help_text(specs):
    if len(specs) == 0:
        em = await general_help()
        return em
    if specs[0].lower() == "c":
            em = await general_commands_help()
            return em
    elif specs[0].lower() == "mc":
            em = await minecraft_help()
            return em
    em = await general_help()
    return em
# HELP message command
@client.command(name="help")
async def help(ctx, *specs):
    em = await get_help_text(specs)
    await ctx.send(embed=em)
    return
# HELP slash command
@client.tree.command(
    name="help",
    description="learn about the commands!",
)
async def slash_help(ctx, specs: Optional[str]):
    if specs == None:
         em = await get_help_text([])
    else:
        em = await get_help_text([specs])
    await ctx.response.send_message(embed=em)
    return

# TIME
async def get_time():
    together = datetime.datetime(2024, 10, 20, 23, 31, 0)
    now = datetime.datetime.now()
    dif = relativedelta(now, together)

    string = str(dif.years) + " years " + str(dif.months) + " months " + str(
        dif.days) + " days " + str(dif.hours) + " hours " + str(
            dif.minutes) + " minutes " + str(dif.seconds) + " seconds "
    em = discord.Embed(title="Kevin ♥ Jenny")
    em.add_field(name="We have been together for:", value=string)
    return em
# TIME message command
@client.command(name="time")
async def time(ctx):
    em = await get_time()
    await ctx.send(embed=em)
    return
# TIME slash command
@client.tree.command(
          name="time",
          description="How long have we been together?"
)
async def time_slash(ctx):
    em = await get_time()
    await ctx.response.send_message(embed=em)
    return

# TIME automatic messaging system
time = datetime.time(hour=23, minute=31)
class DailyTimePing(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
        self.time_ping.start()
    
    @tasks.loop(time=time)
    async def time_ping(self) -> None:
        print("KEVIN AND JENNY DAYVERSARY")

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(
        name="learn about commands with kj!help"))
    await client.tree.sync()
    #await client.tree.sync(guild=discord.Object(id=788204563173867540))
    print("Ready!")

keep_alive()
client.run(os.environ['TOKEN'])