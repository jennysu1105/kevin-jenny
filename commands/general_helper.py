import discord
import re
import datetime
from dateutil.relativedelta import relativedelta
from access_json import *
import shutil
from PIL import Image
from components.calender import Calendar

from help import *

# Fix specs
async def fix_specs(specs):
    fixed = []
    for specs in specs:
        if specs == None:
            fixed.append("N/A")
        else:
            fixed.append(specs)
    return fixed

# HELP command
async def get_help_text(specs):
    if len(specs) == 0:
        em = await general_help()
        return em
    if specs[0].lower() == "c":
            em = await general_commands_help()
            return em
    elif specs[0].lower() == "mc":
            em = await minecraft_help()
            return em
    em = await general_help()
    return em

# TIME command
async def get_time():
    calendar = Calendar()
    dif = calendar.time_since(2024, 10, 19, 23, 31, 0)

    string = str(dif["Y"]) + " years " + str(dif["M"]) + " months " + str(
        dif["D"]) + " days " + str(dif["h"]) + " hours " + str(
            dif["m"]) + " minutes " + str(dif["s"]) + " seconds "
    em = discord.Embed(title="Kevin ♥ Jenny")
    em.add_field(name="We have been together for:", value=string)
    return em