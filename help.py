import discord


async def general_help():
                   em = discord.Embed(
                       title="General Help",
                       description="kj!help <type> OR /help <type> for more indepth help.")
                   em.add_field(name="kj!help c OR /help c", value="General commands")
                   em.add_field(name="kj!help mc OR /help mc", value="Minecraft commands")
                   return em


async def general_commands_help():
                   em = discord.Embed(title="General Commands Help")
                   em.add_field(name="kj!time OR /time",
                                value="How long we have been together!")
                   return em


async def minecraft_help():
                   em = discord.Embed(title="Minecraft Commands Help",
                                      description="kj!mc <type>")
                   em.add_field(
                       name="kj!mc spt <name> <x> <y> <z>",
                       value="Save coordinate point of [type] at point: [<x> <y> <z>]")
                   em.add_field(name="kj!mc gpt",
                                value="View all coordinate points")
                   em.add_field(name="kj!mc gpt <type>",
                                value="View coordinate points of [type]")
                   return em
