import discord


async def general_help():
    em = discord.Embed(
        title="General Help",
        description="kj!help <type> OR /help <type> for more indepth help.")
    em.add_field(name="kj!help c OR /help c", value="General commands")
    em.add_field(name="kj!help mc OR /help mc", value="Minecraft commands")
    em.add_field(name="/help mem", value="Memory capsule commands")
    return em


async def general_commands_help():
    em = discord.Embed(title="General Commands Help")
    em.add_field(name="kj!time OR /time",
                value="How long we have been together!")
    return em


async def minecraft_help():
    em = discord.Embed(title="Minecraft Commands Help",
                        description="kj!mc <type> OR /mc<type>")
    em.add_field(name="kj!mc time OR /mctime",
        value="How old is our Minecraft world")
    em.add_field(
        name="kj!mc spt <x> <y> <z> <name> OR /mcspt <xyz> <name> [type]",
        value="Save and update coordinate point of <name> at point: [<x> <y> <z>]")
    em.add_field(name="kj!mc vpt [type] [name] OR /mcvpt [type] [name]",
                value="View coordinate points of [type] and/or [name].\n NOTE: for message command, if you only want to search for name, fill type with character")
    return em

async def memory_help():
    em = discord.Embed(title="Memory Capsule Command Help",
                        description="All our memories together! <3")
    em.add_field(name="/memstore <name> <type> <user> <address> [date] [details] [logo] [photo] ",
                value = "All the places we went together!")
    em.add_field(name="/watchsave <name> <type> <user> [date] [detail] [cover] [photo]",
                value = "Save what we have watched together <3")
    em.add_field(name="/watchlist [type] [id]",
                value="View what we've watched together!")
    em.add_field(name="/viewmem [type] [id]",
                value= "Browse what we have watched together!")
    em.add_field(name="updatemem <id> <user> [name] [date] [details] [address] [type] [logo] [photo]",
                value="Change information linked to a memory")

    return em