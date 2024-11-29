import discord
import os
import re
import datetime
from dateutil.relativedelta import relativedelta
from discord.ext import commands, tasks
from discord import app_commands
from typing import Optional, Literal
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
# VIEW function
async def view_mc_coords(type, name):
    coords = await get_mc_coord()
    if type != "" and name != "":
        em = discord.Embed(title="Search Results <" + name + " and " + type + "> :")
    elif name != "":
        em = discord.Embed(title="Search Results <" + name + "> :")
    elif type != "":
        em = discord.Embed(title="Search Results <" + type + "> :")
    else:
        em = discord.Embed(title="Search Results:")
    type = type.title()
    sorted_pts = {}
    for pt in coords:
        if re.search(type.lower(), pt["type"].lower()) and re.search(name.lower(), pt['name'].lower()):
            if pt["name"] not in sorted_pts.keys():
                sorted_pts[pt["name"]] = [pt["pt"]]
            else:
                sorted_pts[pt["name"]].append(pt["pt"])
    for name in sorted_pts.keys():
        em.add_field(name=name, value="\n".join(sorted_pts[name]))
    return em
# TIME function
async def get_mc_time():
    started_world = datetime.datetime(2024, 10, 26, 14, 50, 0)
    now = datetime.datetime.now()
    dif = relativedelta(now, started_world)

    string = str(dif.years) + " years " + str(dif.months) + " months " + str(
        dif.days) + " days " + str(dif.hours) + " hours " + str(
            dif.minutes) + " minutes " + str(dif.seconds) + " seconds "
    em = discord.Embed(title="Our Minecraft World")
    em.add_field(name="We have been working on it for:", value=string)
    return em

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
                status = await save_mc_coord_helper(specs[4], specs[1], specs[2], specs[3], specs[5].title())
            if status: 
                em = discord.Embed(title="SUCCESS", description= specs[4] + " [" + str(specs[1]) + " " + str(specs[2]) + " " + str(specs[3]) + "] as has updated" )
            else:
                em = discord.Embed(title="SUCCESS", description= specs[4] + " [" + str(specs[1]) + " " + str(specs[2]) + " " + str(specs[3]) + "] has saved" )
        else:
            em = discord.Embed(title="UNSUCCESSFUL", description= "Please check your input:")
            em.add_field(name="Message command", value="kj!mc spt <x> <y> <z> <name>")
            em.add_field(name="Slash command", value="/mcspt <x> <y> <z> <name> [type]")
        return em
    elif specs[0] == "vpt":
        if len(specs) == 1:
            em = await view_mc_coords("", "")
        elif len(specs) == 2:
            em = await view_mc_coords(specs[1], "")
        else:
            if specs[1].lower() not in ["biome", "structure", "build"]:
                specs = list(specs)
                specs[1] = ""
            em = await view_mc_coords( specs[1], specs[2])
        return em
    elif specs[0] == "time":
        em = await get_mc_time()
        return em

@client.command(name= "mc")
async def mc(ctx, *specs):
    if specs[0] == "spt":
        name = " ".join(specs[4:])
        specs = list(specs)[:4]
        specs.append(name)
    em = await mc_controller(specs)
    await ctx.send(embed=em)

# SAVE slash command
@client.tree.command(
        name="mcspt",
        description="save and update Minecraft coordinate",
        guilds=[discord.Object(id=788204563173867540), discord.Object(id=1299805872503132161)]
)
async def mc_save_slash(ctx, xyz: str, name: str, type: Optional[Literal["Biome", "Structure", "Build"]]):
    x, y, z = xyz.split(" ")
    if type == None:
        type = "N/A"
    specs = ["spt", x, y, z, name, type]
    em = await mc_controller(specs)
    await ctx.response.send_message(embed=em)

# VIEW slash command
@client.tree.command(
        name="mcvpt",
        description="view Minecraft coordinates",
        guilds=[discord.Object(id=788204563173867540), discord.Object(id=1299805872503132161)]
)
async def mc_view_slash(ctx, type: Optional[Literal["Biome", "Structure", "Build"]], name: Optional[str]):
    if type == None:
        type = ""
    if name == None:
        name = ""
    specs = ["vpt", type, name]
    em = await mc_controller(specs)
    await ctx.response.send_message(embed=em)

# TIME slash command
@client.tree.command(
        name="mctime",
        description="How old is our Minecraft world?",
        guilds=[discord.Object(id=788204563173867540), discord.Object(id=1299805872503132161)]
)
async def mc_time_slash(ctx):
    em = await mc_controller(["time"])
    await ctx.response.send_message(embed=em)

# MEMORY command

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(
        name="learn about commands with kj!help OR /help"))
    await client.tree.sync(guild=discord.Object(id=1299805872503132161))
    await client.tree.sync(guild=discord.Object(id=788204563173867540))
    print("Ready!")

keep_alive()
client.run(os.environ['TOKEN'])