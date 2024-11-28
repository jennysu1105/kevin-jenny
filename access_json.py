import json


async def get_mc_coord():
  with open("data/mc_coord.json", 'r') as f:
    return json.load(f)


async def save_mc_coord(coords):
  with open("data/mc_coord.json", "w") as f:
    json.dump(coords, f)


async def create_new_mc_coord(coords, id, name, pt, type):
  coords[id]
  coords[id]["registered"] = datetime.datetime.now()
  coords[id]["name"] = name
  coords[id]["type"] = type
  coords[id]["pt"] = pt
  return id

async def update_mc_coord(name, pt, type):
  coords = await get_mc_coord()
  all_points = [coords[x]["pt"] for x in range(len(coords))]
  if pt in all_points:
    id = all_points.index(coord)
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