import json
import datetime
from helpers.addressbook import *

WATCHLIST = ["Kdrama", "English", "Anime"]
# MINECRAFT json access
async def get_mc_coord():
  with open("data/mc_coords.json", 'r') as f:
    return json.load(f)
async def save_mc_coord(coords):
  with open("data/mc_coords.json", "w") as f:
    json.dump(coords, f)
async def create_new_mc_coord(coords, id, name, pt, type):
  coords.append({})
  date = datetime.datetime.now()
  coords[id]["registered"] = date.strftime('%m-%d-%Y')
  coords[id]["name"] = name
  coords[id]["type"] = type
  coords[id]["pt"] = pt
  return coords
async def update_mc_coord(name, pt, type):
  coords = await get_mc_coord()
  all_points = [coords[x]["pt"] for x in range(len(coords))]
  if pt in all_points:
    id = all_points.index(pt)
    coords[id]["name"] = name
    coords[id]["pt"] = pt
    if type != "N/A":
      coords[id]["type"] = type
    await save_mc_coord(coords)
    return True

  else:
    id = len(coords)
    coords = await create_new_mc_coord(coords, id, name, pt, type)

  await save_mc_coord(coords)
  return False

async def get_memories():
  with open("data/memories.json", 'r') as f:
    return json.load(f)
async def save_memory(mems):
  with open("data/memories.json", "w") as f:
    json.dump(mems, f)
async def create_new_memory(mems, id, date, name, user, type, details, logo, img, address):
  adds = await get_addresses()
  mems.append({})
  if date == "N/A":
    date = datetime.datetime.now().strftime('%m-%d-%Y')
  mems[id]["date"] = date
  mems[id]["name"] = name
  mems[id]["type"] = type
  mems[id]["details"] = {"Jenny": "N/A", "Kevin": "N/A"}
  if(user == "N/A"):
    mems[id]["details"] = details
  else:
    mems[id]["details"][user] = details
  mems[id]["img"] = img
  mems[id]["address"] = await update_addressbook(address, logo)
  if mems[id]["address"] == "N/A":
    mems[id]["logo"] = logo
  else:
    mems[id]["logo"] = adds[mems[id]["address"]]["logo"]

  return mems

async def sort_memories(mems):
  mems_sorted = sorted(mems, key=lambda x: datetime.datetime.strptime(x["date"], "%m-%d-%Y"))
  return mems_sorted

async def update_mem(id, name, date, user, type, details, address, logo, img):
  mems = await get_memories()
  adds = await get_addresses()
  all_names = [mems[x]["name"] for x in range(len(mems))]
  if (id != "N/A" and id < len(mems)):
    if name != "N/A":
      mems[id]["name"] = name
    if date != "N/A":
      mems[id]["date"] = date
    if type != "N/A":
      mems[id]["type"] = type
    if details != "N/A":
      mems[id]["details"][user] = details
    if img != "N/A":
      mems[id]["img"] = img
    if address != "N/A":
      mems[id]["address"] = await update_addressbook(address, logo)
    if logo != "N/A":
      if mems[id]["address"] != "N/A":
        adds[mems[id]["address"]]["logo"] = logo
      mems[id]["logo"] = logo

  else:
    id = len(mems)
    mems = await create_new_memory(mems, id, date, name, user, type, details, logo, img, address)

  if mems[id]["type"] in WATCHLIST:
      mems[id]["logo"] = await update_watch(mems[id]["name"], mems[id]["type"], mems[id]["logo"])

  result = mems[id]
  mems = await sort_memories(mems)
  await save_memory(mems)
  return result

async def get_watchlist():
  with open("data/watchlist.json", 'r') as f:
    return json.load(f)
async def save_watchlist(watchlist):
  with open("data/watchlist.json", "w") as f:
    json.dump(watchlist, f)

async def create_new_watch(name, type, cover):
  watch = {}
  watch["name"] = name
  watch["type"] = type
  watch["cover"] = cover
  return watch

async def update_watch(name, type, logo):
  watchlist = await get_watchlist()
  for i in range(len(watchlist)):
    if (name.lower() == watchlist[i]["name"].lower() and type == watchlist[i]["type"]):
      if name != "N/A":
        watchlist[i]["name"] = name
      if type != "N/A":
        watchlist[i]["type"] = type
      if logo != "N/A":
        watchlist[i]["cover"] = logo
      await save_watchlist(watchlist)
      return watchlist[i]["cover"]

  else:
    watchlist.append(await create_new_watch(name, type, logo))

  await save_watchlist(watchlist)
  return logo
  