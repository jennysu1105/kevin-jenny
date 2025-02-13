import discord
import re
import datetime
from dateutil.relativedelta import relativedelta
from access_json import *
import shutil
from PIL import Image

from help import minecraft_help

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
        specs = ["" if x=="N/A" else x for x in specs]
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