import discord
import re
import datetime
from dateutil.relativedelta import relativedelta
from access_json import *
import shutil
from PIL import Image

WATCHLIST = ["Kdrama", "English", "Anime"]

async def get_watchlist(em, type):
    mems = await get_memories()
    ids = []
    names = []
    types_dates = []
    for id in range(len(mems)):
        if (type == "" and mems[id]["type"] in WATCHLIST) or (type != "" and re.search(type.lower(), mems[id]["type"].lower())):
            ids.append(str(id))
            names.append(mems[id]["name"])
            types_dates.append(mems[id]["date"] + "\u3000" + mems[id]["type"])

    em.add_field(name="ID", value="\n".join(ids), inline=True)
    em.add_field(name="NAME", value="\n".join(names), inline=True)
    em.add_field(name="DATE           \u3000TYPE", value="\n".join(types_dates), inline=True)
    return em

async def get_memory(id):
    mems = await get_memories()
    if id < len(mems):
        return mems[id]
    else:
        return None

async def get_memory_list(em, type):
    mems = await get_memories()
    ids = []
    names = []
    types_dates = []
    for id in range(len(mems)):
        if (type == "" and mems[id]["type"] not in WATCHLIST) or (type != "" and re.search(type.lower(), mems[id]["type"].lower())):
            ids.append(str(id))
            names.append(mems[id]["name"])
            types_dates.append(mems[id]["date"] + "\u3000" + mems[id]["type"])

    em.add_field(name="ID", value="\n".join(ids), inline=True)
    em.add_field(name="NAME", value="\n".join(names), inline=True)
    em.add_field(name="DATE           \u3000TYPE", value="\n".join(types_dates), inline=True)
    return em

async def get_watch_embed(watch):
    em = discord.Embed(title=watch["name"])
    em.set_thumbnail(url=watch["img"])
    em.add_field(name="Type", value=watch["type"], inline=True)
    em.add_field(name="Date Finished", value=watch["date"], inline=True)
    em.add_field(name="\t", value="\t")
    if (watch["address"] != "N/A"):
        em.add_field(name="Watched at", value=watch["address"])
        em.add_field(name="\t", value="\t")
        em.add_field(name="\t", value="\t")
    em.add_field(name="Comments", value="Jenny: " + watch["details"]["Jenny"] + "\nKevin: " + watch["details"]["Kevin"])
    return em

async def get_memory_embed(memory):
    em = discord.Embed(title=memory["name"])
    em.set_thumbnail(url=memory["img"])
    em.add_field(name="Type", value=memory["type"], inline=True)
    em.add_field(name="Date", value=memory["date"], inline=True)
    em.add_field(name="\t", value="\t")
    if (memory["address"] != "N/A"):
        em.add_field(name="Address", value=memory["address"])
        em.add_field(name="\t", value="\t")
        em.add_field(name="\t", value="\t")
    em.add_field(name="Comments", value="Jenny: " + memory["details"]["Jenny"] + "\nKevin: " + memory["details"]["Kevin"])
    return em

async def mem_controller(specs):
    if specs[0] == "memstore":
        id, name, date, user, type, details, address, img = specs[1:]
        result = await update_mem(id, name.title(), date, user, type, details, address, img)
        em = discord.Embed(title="Success!", description=name+" has been saved in memory capsule.")
        for property in result.keys():
            em.add_field(name=property, value=result[property])
        return em

    if specs[0] == "viewmem":
        if specs[2] != "N/A":
            memory = await get_memory(specs[2])
            if memory == None:
                em = discord.Embed(title="Choose and ID from below:")
                em = await get_memory_list(em, "")
            else:
                em = await get_memory_embed(memory)
        else:
            if specs[1] == "N/A":
                specs[1] = ""
            em = discord.Embed(title="Results!")
            em = await get_memory_list(em, specs[1])
        return em

    if specs[0] == "watchsave":
        name, date, user, type, details, address, img = specs[1:]
        name = name.title()
        mems = await get_memories()
        all_names = [mems[x]["name"] for x in range(len(mems))]
        if name in all_names:
            em = discord.Embed(title="Success!", description=name+" has been updated in memory capsule.")
            id = all_names.index(name)
        else:
            em = discord.Embed(title="Success!", description=name+" has been saved in memory capsule.")
            id = "N/A"
        result = await update_mem(id, name, date, user, type, details, address, img)
        for property in result.keys():
            em.add_field(name=property.title(), value=result[property])
        return em
    
    if specs[0] == "watchlist":
        if specs[2] != "N/A":
            watch = await get_memory(specs[2])
            if watch == None:
                em = discord.Embed(title="Choose and ID from below:")
                em = await get_watchlist(em, "")
            else:
                em = await get_watch_embed(watch)
        else:
            if specs[1] == "N/A":
                specs[1] = ""
            em = discord.Embed(title="Results!")
            em = await get_watchlist(em, specs[1])

        return em