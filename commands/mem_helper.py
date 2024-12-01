import discord
import re
import datetime
from dateutil.relativedelta import relativedelta
from access_json import *
import shutil
from PIL import Image

async def mem_controller(specs):
    if specs[0] == "memstore":
        return
    if specs[0] == "watchsave":
        return