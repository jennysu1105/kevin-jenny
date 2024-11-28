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

# TIME slash command
@client.tree.command(
          name="time",
          description="How long have we been together?"
)
async def time_slash(ctx):
    em = await get_time()
    await ctx.response.send_message(embed=em)

# TIME automatic messaging system
time = datetime.time(hour=23, minute=31)
class DailyTimePing(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
        self.time_ping.start()
    
    @tasks.loop(time=time)
    async def time_ping(self) -> None:
        print("KEVIN AND JENNY DAYVERSARY")

# MC_COORD commands
# Helper functions
# SAVE function
async def save_mc_coord_helper(name, x, y, z, type):
    pt = str(x) + " " + str(y) + " " + str(z)
    return await update_mc_coord(name.title(), pt, type)

# MC command controller
async def mc_controller(specs):
    if len(specs) == 0:
        em = await minecraft_help()
        return em
    if specs[0] == "spt":
        if len(specs) > 4:
            if len(specs) == 5:
                status = await save_mc_coord_helper(specs[4], specs[1], specs[2], specs[3], "N/A")
            else: 
                status = await save_mc_coord_helper(specs[4], specs[1], specs[2], specs[3], specs[5])
            if status: 
                em = discord.Embed(title="SUCCESS", description= name + " [" + str(x) + " " + str(y) + " " + str(z) + "] as has updated" )
            else:
                em = discord.Embed(title="SUCCESS", description= name + " [" + str(x) + " " + str(y) + " " + str(z) + "] has saved" )
        else:
            em = discord.Embed(title="UNSUCCESSFUL", description= "Please check your input:")
            em.add_field(name="Message command", value="kj!mc spt <x> <y> <z> <name>")
            em.add_field(name="Slash command", value="/mc spt <x> <y> <z> <name> [type]")
        return em

@client.command(name= "kj!mc")
async def mc(ctx, *specs):
    name = " ".join(specs[4:])
    em = await mc_controller(specs[:4].append(name))
    await ctx.send(embed=em)

# MEMORY command

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(
        name="learn about commands with kj!help OR /help"))
    await client.tree.sync()
    #await client.tree.sync(guild=discord.Object(id=788204563173867540))
    print("Ready!")

keep_alive()
client.run(os.environ['TOKEN'])