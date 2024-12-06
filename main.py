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

from commands.mc_helper import mc_controller
from commands.general_helper import get_help_text, get_time, fix_specs
from commands.mem_helper import mem_controller

intents = discord.Intents.all()

client = commands.Bot(command_prefix="kj!", intents=intents)

client.remove_command("help")
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

# MC_COORD commands
# MC message commands
@client.command(name= "mc")
async def mc(ctx, *specs):
    if specs[0] == "spt":
        name = " ".join(specs[4:])
        specs = list(specs)[:4]
        specs.append(name)
    em = await mc_controller(specs)
    await ctx.send(embed=em)
# MC slash commands
# SAVE slash command
@client.tree.command(
        name="mcspt",
        description="save and update Minecraft coordinate",
        guilds=[discord.Object(id=788204563173867540), discord.Object(id=1299805872503132161)]
)
async def mc_save_slash(ctx, xyz: str, name: str, type: Optional[Literal["Biome", "Structure", "Build"]]):
    x, y, z = xyz.split(" ")
    specs = await fix_specs(["spt", x, y, z, name, type])
    em = await mc_controller(specs)
    await ctx.response.send_message(embed=em)
# VIEW slash command
@client.tree.command(
        name="mcvpt",
        description="view Minecraft coordinates",
        guilds=[discord.Object(id=788204563173867540), discord.Object(id=1299805872503132161)]
)
async def mc_view_slash(ctx, type: Optional[Literal["Biome", "Structure", "Build"]], name: Optional[str]):
    specs = await fix_specs(["vpt", type, name])
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

# MEMORY CAPSULE command
# STORE MEMORY command
@client.tree.command(
    name="memstore", 
    description="Save memories here!/nDates in mm-dd-yyyy format please OR blank for today!",
    guilds=[discord.Object(id=788204563173867540), discord.Object(id=1299805872503132161)]
)
async def mem_store_slash(ctx, id: Optional[int], name: str, user: Literal["Jenny", "Kevin"], date: Optional[str], type: Literal["Food", "Activity", "Work", "Home"], details: Optional[str], address: str, img: Optional[str]):
    specs = await fix_specs(["memstore", id, name, date, user, type, details, address, img])
    em = await mem_controller(specs)
    await ctx.response.send_message(embed=em)

# STORE WATCH command
@client.tree.command(
    name="watchsave",
    description="Save what we have watched together <3/nDates in mm-dd-yyyy format please!",
    guilds=[discord.Object(id=788204563173867540), discord.Object(id=1299805872503132161)]
)
async def watch_save_slash(ctx, name: str, user: Literal["Jenny", "Kevin"], date: Optional[str], type: Literal["Kdrama", "English", "Anime"], details: Optional[str], img: Optional[str]):
    specs = await fix_specs(["watchsave", name, date, user, type, details, "N/A", img])
    em = await mem_controller(specs)
    await ctx.response.send_message(embed=em)

# GET WATCHLIST command
@client.tree.command(
    name="watchlist",
    description="View what we've watched together! <3",
    guilds=[discord.Object(id=788204563173867540), discord.Object(id=1299805872503132161)]
)
async def watchlist_slash(ctx, type: Optional[Literal["Kdrama", "English", "Anime"]], id: Optional[int]):
    specs = await fix_specs(["watchlist", type, id])
    em = await mem_controller(specs)
    await ctx.response.send_message(embed=em)

# GET MEMORY command
@client.tree.command(
    name="viewmem",
    description="Retrieve one of out memories in our memory capsule!",
    guilds=[discord.Object(id=788204563173867540), discord.Object(id=1299805872503132161)]
)
async def viewmem_slash(ctx, type: Optional[Literal["Food", "Activity", "Work", "Home"]], id: Optional[int]):
    specs = await fix_specs(["viewmem", type, id])
    em = await mem_controller(specs)
    await ctx.response.send_message(embed=em)
    
@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(
        name="learn about commands with kj!help OR /help"))
    await client.tree.sync(guild=discord.Object(id=1299805872503132161))
    await client.tree.sync(guild=discord.Object(id=788204563173867540))
    print("Ready!")

keep_alive()
client.run(os.environ['TOKEN'])