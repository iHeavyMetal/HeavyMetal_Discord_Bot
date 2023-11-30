from discord.ext import commands

class BotCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        guild = member.guild
        guildname = guild.name
        dmchannel = await member.create_dm()
        await dmchannel.send(f"Witamy na discordzie {guildname}!")  # set a welcome DM message

async def setup(bot):
    await bot.add_cog(BotCog(bot))