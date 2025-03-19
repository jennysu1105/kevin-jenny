import asyncio
import access_json
import helpers.addressbook

# Separating addresses from memory
async def split_mem_address(mem):
    new_mem = {}
    new_mem["date"] = mem["date"]
    new_mem["name"] = mem["name"]
    if (mem["address"] != "N/A"):
        new_mem["address"] = await helpers.addressbook.update_addressbook(mem["address"], mem["logo"])
    else:
        new_mem["address"] = "N/A"
    new_mem["type"] = mem["type"]
    new_mem["details"] = mem["details"]
    new_mem["img"] = mem["img"]

    return new_mem
async def update_mems_addressbook():
    mems = await access_json.get_memories()
    new_mems = []

    for mem in mems:
        new_mems.append(await split_mem_address(mem))
    
    await access_json.save_memory(new_mems)
#asyncio.run(update_mems_addressbook())

# Adding logo and fixing logo fields
async def add_logos():
    mems = await access_json.get_memories()
    adds = await helpers.addressbook.get_addresses()
    new_mems = []

    for i in range(len(mems)):
        if(mems[i]["address"] != "N/A"):
            new_mems = await access_json.create_new_memory(new_mems, i, mems[i]["date"], mems[i]["name"], "N/A", mems[i]["type"],mems[i]["details"],"N/A", mems[i]["img"],adds[mems[i]["address"]]["address"])

        else:
            new_mems = await access_json.create_new_memory(new_mems, i, mems[i]["date"], mems[i]["name"], "N/A", mems[i]["type"],mems[i]["details"],"N/A", mems[i]["img"], "N/A")
    await access_json.save_memory(new_mems)
#asyncio.run(add_logos())