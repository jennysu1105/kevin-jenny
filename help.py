import discord


async def general_help():
                   em = discord.Embed(
                       title="General Help",
                       description="kj!h <type> for more indepth help.")
                   em.add_field(name="kj!h c", value="General commands")
                   return em


async def general_commands_help():
                   em = discord.Embed(title="General Commands Help")
                   em.add_field(name="kj!time",
                                value="How long we have been together!")
                   return em
