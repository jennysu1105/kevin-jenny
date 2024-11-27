import json


async def get_mc_coord():
  with open("data/mc_coord.json", 'r') as f:
    return json.load(f)


async def save_mc_coord(coords):
  with open("data/mc_coord.json", "w") as f:
    json.dump(coords, f)


async def create_new_mc_coord(coords, id):
  coords[id]
  coords[id]["registered"] = None
  coords[id]["name"] = "N/A"
  coords[id]["type"] = "N/A"
  coords[id]["x"] = 0
  coords[id]["y"] = 0
  coords[id]["z"] = 0
  return id

async def open_mc_coord(coord):
  coords = await get_mc_coord()
  if coord["id"] < len(coords):
    return False

  else:
    id = len(coords)
    coords = await create_new_mc_coord(coords, id)

  await save_mc_coord(coords)

  return True

async def get_memories():
  with open("data/memories.json", 'r') as f:
    return json.load(f)


async def save_memory(mems):
  with open("data/memories.json", "w") as f:
    json.dump(mems, f)

async def create_new_memory(mems, id):
  mems[id]
  mems[id]["date"] = None
  mems[id]["name"] = "N/A"
  mems[id]["type"] = "N/A"
  mems[id]["description"] = "N/A"
  mems[id]["img"] = "N/A"

async def open_mc_coord(mem):
  mems = await get_memories()
  if mems["id"] < len(mems):
    return False

  else:
    id = len(mem)
    mems = await create_new_memory(mems, id)

  await save_memory(mems)

  return True