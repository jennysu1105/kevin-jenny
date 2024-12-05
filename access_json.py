import json
import datetime

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
async def create_new_memory(mems, id, date, name, user, type, details, img, address):
  mems.append({})
  if date == "N/A":
    date = datetime.datetime.now().strftime('%m-%d-%Y')
  mems[id]["date"] = date
  mems[id]["name"] = name
  mems[id]["type"] = type
  mems[id]["details"] = {"Jenny": "N/A", "Kevin": "N/A"}
  mems[id]["details"][user] = details
  mems[id]["img"] = img
  mems[id]["address"] = address
  return mems

async def update_mem(id, name, date, user, type, details, address, img):
  mems = await get_memories()
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
      mems[id]["address"] = address

  else:
    id = len(mems)
    mems = await create_new_memory(mems, id, date, name, user, type, details, img, address)

  await save_memory(mems)
  return mems[id]