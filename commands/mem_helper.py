import discord
import re
import datetime
from dateutil.relativedelta import relativedelta
from access_json import *
import shutil
from PIL import Image
from helpers.addressbook import *

from components.pagination import Pagination

L = 20
WATCHLIST = ["Kdrama", "English", "Anime"]

async def get_watchlist(type):
    mems = await get_memories()
    mem_list = []
    for id in range(len(mems)):
        if (type == "" and mems[id]["type"] in WATCHLIST) or (type != "" and re.search(type.lower(), mems[id]["type"].lower())):
            mem_list.append({"id": str(id), "name": mems[id]["name"], "types_date": mems[id]["date"] + "\u3000" + mems[id]["type"]})

    return mem_list

async def get_memory(id):
    mems = await get_memories()
    if id < len(mems):
        return mems[id]
    else:
        return None

async def get_memory_list(type):
    mems = await get_memories()
    mem_list = []
    for id in range(len(mems)):
        if (type == "") or (type != "" and re.search(type.lower(), mems[id]["type"].lower())):
            mem_list.append({"id": str(id), "name": mems[id]["name"], "types_date": mems[id]["date"] + "\u3000" + mems[id]["type"]})

    return mem_list

async def get_memory_embed(memory):
    em = discord.Embed(title=memory["name"])
    adds = await get_addresses()
    if memory["logo"] != "N/A":
        em.set_thumbnail(url=memory["logo"])
    em.add_field(name="Type", value=memory["type"], inline=True)
    em.add_field(name="Date", value=memory["date"], inline=True)
    em.add_field(name="\t", value="\t")
    if (memory["address"] != "N/A"):
        em.add_field(name="Address", value=adds[memory["address"]]["address"])
        em.add_field(name="\t", value="\t")
        em.add_field(name="\t", value="\t")
    em.add_field(name="Comments", value="Jenny: " + memory["details"]["Jenny"] + "\nKevin: " + memory["details"]["Kevin"])
    if memory["img"] != "N/A":
        em.set_image(url=memory["img"])
    return em

async def mem_controller(specs):
    if specs[0] == "memstore":
        id, name, date, user, type, details, address, logo, img = specs[1:]
        result = await update_mem(id, name, date, user, type, details, address, logo, img)
        em = discord.Embed(title="Success!", description=name+" has been saved in memory capsule.")
        for property in result.keys():
            em.add_field(name=property, value=result[property])
        return em

    if specs[0] == "viewmem":
        if specs[2] != "N/A":
            memory = await get_memory(specs[2])
            if memory == None:
                mems = await get_memory_list("")
                async def get_page(page: int):
                    em = discord.Embed(title="Choose an ID from below:")
                    offset = (page-1)*L
                    ids=[]
                    names=[]
                    types_dates = []
                    for mem in mems[offset:offset+L]:
                        ids.append(mem["id"])
                        names.append(mem["name"])
                        types_dates.append(mem["types_date"])
                    
                    em.add_field(name="ID", value="\n".join(ids), inline=True)
                    em.add_field(name="NAME", value="\n".join(names), inline=True)
                    em.add_field(name="DATE           \u3000TYPE", value="\n".join(types_dates), inline=True)

                    n = Pagination.compute_total_pages(len(mems), L)
                    em.set_footer(text=f"Page {page} from {n}")
                    return em, n
                
                await Pagination(specs[3], get_page).navegate()

            else:
                em = await get_memory_embed(memory)
                await specs[3].response.send_message(embed=em)
        else:
            if specs[1] == "N/A":
                specs[1] = ""
            mems = await get_memory_list(specs[1])
            async def get_page(page: int):
                em = discord.Embed(title="Results!")
                offset = (page-1)*L
                ids=[]
                names=[]
                types_dates = []
                for mem in mems[offset:offset+L]:
                    ids.append(mem["id"])
                    names.append(mem["name"])
                    types_dates.append(mem["types_date"])
                
                em.add_field(name="ID", value="\n".join(ids), inline=True)
                em.add_field(name="NAME", value="\n".join(names), inline=True)
                em.add_field(name="DATE           \u3000TYPE", value="\n".join(types_dates), inline=True)

                n = Pagination.compute_total_pages(len(mems), L)
                em.set_footer(text=f"Page {page} from {n}")
                return em, n
                
            await Pagination(specs[3], get_page).navegate()

    if specs[0] == "watchsave":
        name, date, user, type, details, address, logo, img = specs[1:]
        name = name.title()
        mems = await get_memories()
        all_names = [mems[x]["name"] for x in range(len(mems))]
        if name in all_names:
            em = discord.Embed(title="Success!", description=name+" has been updated in memory capsule.")
            id = all_names.index(name)
        else:
            em = discord.Embed(title="Success!", description=name+" has been saved in memory capsule.")
            id = "N/A"
        result = await update_mem(id, name, date, user, type, details, address, logo, img)
        for property in result.keys():
            em.add_field(name=property.title(), value=result[property])
        return em
    
    if specs[0] == "watchlist":
        if specs[2] != "N/A":
            watch = await get_memory(specs[2])
            if watch == None:
                mems = await get_watchlist("")
                async def get_page(page: int):
                    em = discord.Embed(title="Choose an ID from below:")
                    offset = (page-1)*L
                    ids=[]
                    names=[]
                    types_dates = []
                    for mem in mems[offset:offset+L]:
                        ids.append(mem["id"])
                        names.append(mem["name"])
                        types_dates.append(mem["types_date"])
                    
                    em.add_field(name="ID", value="\n".join(ids), inline=True)
                    em.add_field(name="NAME", value="\n".join(names), inline=True)
                    em.add_field(name="DATE           \u3000TYPE", value="\n".join(types_dates), inline=True)

                    n = Pagination.compute_total_pages(len(mems), L)
                    em.set_footer(text=f"Page {page} from {n}")
                    return em, n
                
                await Pagination(specs[3], get_page).navegate()
            else:
                em = await get_memory_embed(watch)
                await specs[3].response.send_message(embed=em)
        else:
            if specs[1] == "N/A":
                specs[1] = ""
            mems = await get_watchlist(specs[1])
            async def get_page(page: int):
                    em = discord.Embed(title="Results!")
                    offset = (page-1)*L
                    ids=[]
                    names=[]
                    types_dates = []
                    for mem in mems[offset:offset+L]:
                        ids.append(mem["id"])
                        names.append(mem["name"])
                        types_dates.append(mem["types_date"])
                    
                    em.add_field(name="ID", value="\n".join(ids), inline=True)
                    em.add_field(name="NAME", value="\n".join(names), inline=True)
                    em.add_field(name="DATE           \u3000TYPE", value="\n".join(types_dates), inline=True)

                    n = Pagination.compute_total_pages(len(mems), L)
                    em.set_footer(text=f"Page {page} from {n}")
                    return em, n
                
            await Pagination(specs[3], get_page).navegate()
    
    if specs[0] == "updatemem":
        id, name, date, user, type, details, address, logo, img = specs[1:]
        result = await update_mem(id, name, date, user, type, details, address, logo, img)
        em = discord.Embed(title="Success!", description=name+" has been updated in memory capsule.")
        for property in result.keys():
            em.add_field(name=property, value=result[property])
        return em
    
    if specs[0] == "comment":
        id, user, comment = specs[1:]
        memory = await get_memory(id)
        if memory == None:
            em = discord.Embed("No memory found")
        else:
            result = await update_mem(id, "N/A", "N/A", user, "N/A", comment, "N/A", "N/A", "N/A")
            memory = await get_memory(id)
            em = await get_memory_embed(memory)
        return em