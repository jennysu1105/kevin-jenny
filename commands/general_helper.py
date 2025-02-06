import discord
import re
import datetime
from dateutil.relativedelta import relativedelta
from access_json import *
import shutil
from PIL import Image

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
    together = datetime.datetime(2024, 10, 20, 23, 31, 0)
    now = datetime.datetime.now()
    dif = relativedelta(now, together)

    string = str(dif.years) + " years " + str(dif.months) + " months " + str(
        dif.days) + " days " + str(dif.hours) + " hours " + str(
            dif.minutes) + " minutes " + str(dif.seconds) + " seconds "
    em = discord.Embed(title="Kevin ♥ Jenny")
    em.add_field(name="We have been together for:", value=string)
    return em