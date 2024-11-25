import json


async def get_t_codes():
  with open("data/t_codes.json", 'r') as f:
    return json.load(f)


async def save_t_codes(t_codes):
  with open("data/t_codes.json", "w") as f:
    json.dump(t_codes, f)


async def open_t_code(code):
  codes = await get_t_codes()
  if code in codes:
    return False

  else:
    codes[code] = {}
    codes[code]["date"] = "TBD"
    codes[code]["decks"] = "TBD"
    codes[code]["web"] = "N/A"

  await save_t_codes(codes)

  return True
